"""
Per-sample YUV -> packed RGB24.
in0 Y (0..255), in1 U (~+/-0.2), in2 V (~+/-0.2)
out: uint8, 3 bytes per Y sample (R,G,B)
"""

import numpy as np
from gnuradio import gr


class blk(gr.interp_block):
    def __init__(self, u_gain=500.0, v_gain=500.0):
        gr.interp_block.__init__(
            self, name='yuv_to_rgb',
            in_sig=[np.float32, np.float32, np.float32],
            out_sig=[np.uint8],
            interp=3)
        self.u_gain = float(u_gain)
        self.v_gain = float(v_gain)
        # 832*576*3 = 1437696 output bytes per frame
        self.set_output_multiple(832 * 576 * 3)

    def work(self, input_items, output_items):
        y = input_items[0]
        u = input_items[1] * self.u_gain
        v = input_items[2] * self.v_gain
        out = output_items[0]
        n = len(y)

        r = y + 1.140 * v
        g = y - 0.395 * u - 0.581 * v
        b = y + 2.032 * u

        rgb = np.empty(n * 3, dtype=np.uint8)
        rgb[0::3] = np.clip(r, 0, 255).astype(np.uint8)
        rgb[1::3] = np.clip(g, 0, 255).astype(np.uint8)
        rgb[2::3] = np.clip(b, 0, 255).astype(np.uint8)
        out[:n * 3] = rgb
        return n * 3