import numpy as np
from gnuradio import gr

class blk(gr.basic_block):
    LINE_LEN        = 1024
    LINES_PER_FIELD = 312
    ACTIVE_LINES    = 288
    ACTIVE_LEN      = 832
    ACTIVE_START    = 180
    VBI_TOP_LINES   = 20

    BROAD_MIN_WIDTH = 300
    HSYNC_MIN_WIDTH = 50
    HSYNC_MAX_WIDTH = 120

    FRAME_SIZE = 2 * ACTIVE_LINES * ACTIVE_LEN

    def __init__(self, threshold=-60.0):
        gr.basic_block.__init__(
            self, name="pal_sync_color",
            in_sig=[np.float32, np.complex64],  # Changed to 2 inputs (Y float, Chroma complex)
            out_sig=[np.float32, np.float32, np.float32])
        self.threshold = float(threshold)
        self._held = None
        self._held_parity = None
        self._min_input = (self.LINES_PER_FIELD + 3) * self.LINE_LEN
        self.set_output_multiple(self.FRAME_SIZE)

    def forecast(self, noutput_items, ninput_items_required):
        n_frames = max(1, noutput_items // self.FRAME_SIZE)
        n_needed = n_frames * self._min_input
        try:
            for i in range(2): # Changed for 2 inputs
                ninput_items_required[i] = n_needed
            return
        except TypeError:
            return [n_needed, n_needed]

    def _find_pulses(self, sig):
        below = (sig < self.threshold).astype(np.int8)
        edges = np.diff(below)
        falls = np.where(edges ==  1)[0] + 1
        rises = np.where(edges == -1)[0] + 1
        if falls.size == 0 or rises.size == 0:
            return np.empty(0, np.int32), np.empty(0, np.int32)
        rises = rises[rises > falls[0]]
        n = min(falls.size, rises.size)
        return falls[:n].astype(np.int32), (rises[:n] - falls[:n]).astype(np.int32)

    def _find_vsync_block(self, starts, widths):
        broad = np.where(widths >= self.BROAD_MIN_WIDTH)[0]
        if broad.size < 2:
            return -1, np.empty(0, np.int32)
        i = 0
        while i < broad.size:
            j = i
            while (j + 1 < broad.size and
                   starts[broad[j + 1]] - starts[broad[j]] < 2 * self.LINE_LEN):
                j += 1
            if j > i:
                cluster = broad[i:j+1]
                vs_end = int(starts[broad[j]] + widths[broad[j]])
                return vs_end, starts[cluster]
            i = j + 1
        return -1, np.empty(0, np.int32)

    def _detect_parity(self, broad_starts, h0):
        if broad_starts.size == 0:
            return 0
        delta = (h0 - int(broad_starts[0])) % self.LINE_LEN
        aligned = min(delta, self.LINE_LEN - delta)
        offset  = abs(delta - self.LINE_LEN // 2)
        return 0 if aligned < offset else 1

    def general_work(self, input_items, output_items):
        y, c = input_items[0], input_items[1]
        y_o, u_o, v_o = output_items[0], output_items[1], output_items[2]

        n_min = min(y.size, c.size)
        out_min = min(y_o.size, u_o.size, v_o.size)
        if n_min < self._min_input or out_min < self.FRAME_SIZE:
            return 0

        fallback = self.LINES_PER_FIELD * self.LINE_LEN

        starts, widths = self._find_pulses(y)
        if starts.size < 5:
            self._held = None
            for i in range(2): self.consume(i, fallback)
            return 0

        vs_end, broad_starts = self._find_vsync_block(starts, widths)
        if vs_end < 0:
            self._held = None
            for i in range(2): self.consume(i, fallback)
            return 0

        is_hsync = ((widths >= self.HSYNC_MIN_WIDTH) &
                    (widths <= self.HSYNC_MAX_WIDTH) &
                    (starts >= vs_end + 3 * self.LINE_LEN))
        idx = np.where(is_hsync)[0]
        if idx.size == 0:
            self._held = None
            for i in range(2): self.consume(i, fallback)
            return 0

        h0 = int(starts[idx[0]])
        parity = self._detect_parity(broad_starts, h0)

        first_line = h0 + (self.VBI_TOP_LINES - 1) * self.LINE_LEN
        last_line  = first_line + (self.ACTIVE_LINES - 1) * self.LINE_LEN
        end_y = last_line + self.ACTIVE_START + self.ACTIVE_LEN
        if end_y > n_min:
            return 0

        hs_all = starts[(widths >= self.HSYNC_MIN_WIDTH) &
                        (widths <= self.HSYNC_MAX_WIDTH)]
        tol = self.LINE_LEN // 8
        line_starts = first_line + np.arange(self.ACTIVE_LINES) * self.LINE_LEN
        if hs_all.size:
            for k in range(self.ACTIVE_LINES):
                est = line_starts[k]
                cand = hs_all[(hs_all >= est - tol) & (hs_all <= est + tol)]
                if cand.size:
                    line_starts[k] = cand[np.argmin(np.abs(cand - est))]

        # --- BURST PHASE ESTIMATOR & PAL COMB FILTER ---
        # 1. Extract the Color burst for every line
        burst_idx = np.clip(line_starts[:, None] + np.arange(int(5.5 * 16), int(7.8 * 16)), 0, n_min - 1)
        bursts = np.mean(c[burst_idx], axis=1)

        # 2. Add the previous line's burst to the current line. 
        # PAL bursts swing +45 and -45 degrees. Adding them cancels the swing, revealing the absolute phase!
        bursts_prev = np.roll(bursts, 1)
        bursts_prev[0] = bursts[0] 
        
        # Calculate mathematical phase error for the line
        phase_corr = np.angle(bursts + bursts_prev) - np.pi
        
        # 3. Rotate burst to determine if this is a +V or -V line (PAL switch)
        rotated_bursts = bursts * np.exp(-1j * phase_corr)
        v_mult = np.where(np.imag(rotated_bursts) > 0, 1.0, -1.0)

        # 4. Extract active video data
        s_y = line_starts + self.ACTIVE_START
        col = np.arange(self.ACTIVE_LEN)
        idx2d = s_y[:, None] + col[None, :]

        y_f = y[idx2d]
        c_f = c[idx2d]

        # 5. Apply the perfect phase correction to the entire active line
        c_f_corrected = c_f * np.exp(-1j * phase_corr[:, None])
        
        # Split complex data cleanly into U and V
        u_f = np.real(c_f_corrected)
        v_f = np.imag(c_f_corrected) * v_mult[:, None]

        consumed = min(h0 + (self.LINES_PER_FIELD - 6) * self.LINE_LEN, n_min)

        if self._held is None:
            self._held = (y_f, u_f, v_f)
            self._held_parity = parity
            for i in range(2): self.consume(i, consumed)
            return 0

        cur = (y_f, u_f, v_f)
        if self._held_parity == 0:
            field_a, field_b = self._held, cur
        else:
            field_a, field_b = cur, self._held

        for fa, fb, out in zip(field_a, field_b, (y_o, u_o, v_o)):
            frame = np.empty((2 * self.ACTIVE_LINES, self.ACTIVE_LEN), dtype=np.float32)
            frame[0::2] = fa
            frame[1::2] = fb
            out[:frame.size] = frame.ravel()

        self._held = None
        self._held_parity = None
        for i in range(2): self.consume(i, consumed)
        return self.FRAME_SIZE