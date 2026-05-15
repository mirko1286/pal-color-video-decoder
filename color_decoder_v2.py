#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
from gnuradio import uhd
import time
import cmath
import color_decoder_v2_epy_block_0 as epy_block_0  # embedded python block
import color_decoder_v2_epy_block_0_0 as epy_block_0_0  # embedded python block


def snipfcn_snippet_0(self):
    import time
    import threading
    import subprocess  # <--- Added this line

    def launch_ffplay():
        time.sleep(2) # let GR's TCP server come up first
        cmd = [
            "ffplay",
            "-f", "rawvideo",
            "-pixel_format", "rgb24",
            "-video_size", "832x576",
            "-framerate", "25",
            "-i", "tcp://127.0.0.1:2000",
        ]
        try:
            # Removed the Windows-only creationflags argument
            subprocess.Popen(cmd)
        except Exception as e:
            print(f"ERROR: {e}")

    threading.Thread(target=launch_ffplay, daemon=True).start()


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)

class color_decoder_v2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "color_decoder_v2")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.threshhold = threshhold = -60
        self.samp_rate = samp_rate = 40000000
        self.rangee = rangee = 1
        self.rangedb = rangedb = 20
        self.offset = offset = 0
        self.line_length = line_length = 1024
        self.hue = hue = 0
        self.filter_frequency = filter_frequency = 1e6
        self.color_Strength = color_Strength = 500
        self.broj = broj = 0

        ##################################################
        # Blocks
        ##################################################

        self._threshhold_range = qtgui.Range(-300, -30, 0.05, -60, 200)
        self._threshhold_win = qtgui.RangeWidget(self._threshhold_range, self.set_threshhold, "threshold", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._threshhold_win)
        self._rangee_range = qtgui.Range(-5, 5, 0.01, 1, 200)
        self._rangee_win = qtgui.RangeWidget(self._rangee_range, self.set_rangee, "contrast", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rangee_win)
        self._rangedb_range = qtgui.Range(0, 120, 0.05, 20, 200)
        self._rangedb_win = qtgui.RangeWidget(self._rangedb_range, self.set_rangedb, "rangedb", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rangedb_win)
        self._filter_frequency_range = qtgui.Range(5e5, 3e6, 1, 1e6, 200)
        self._filter_frequency_win = qtgui.RangeWidget(self._filter_frequency_range, self.set_filter_frequency, "'filter_frequency'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._filter_frequency_win)
        self._color_Strength_range = qtgui.Range(100, 3000, 1, 500, 200)
        self._color_Strength_win = qtgui.RangeWidget(self._color_Strength_range, self.set_color_Strength, "'color_Strength'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._color_Strength_win)
        self._broj_range = qtgui.Range(-300, 300, 1, 0, 200)
        self._broj_win = qtgui.RangeWidget(self._broj_range, self.set_broj, "'broj'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._broj_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(('type=b200', '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(16000000)
        # No synchronization enforced.

        self.uhd_usrp_source_0.set_center_freq(5.917e9, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_gain(rangedb, 0)
        self.uhd_usrp_source_0.set_auto_dc_offset(True, 0)
        self.uhd_usrp_source_0.set_auto_iq_balance(True, 0)
        self._offset_range = qtgui.Range(0, 100, 0.01, 0, 200)
        self._offset_win = qtgui.RangeWidget(self._offset_range, self.set_offset, "'offset'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._offset_win)
        self.network_tcp_sink_0 = network.tcp_sink(gr.sizeof_char, 1, '127.0.0.1', 2000,2)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                (samp_rate*0.4),
                filter_frequency,
                400e3,
                window.WIN_HAMMING,
                6.76))
        self._hue_range = qtgui.Range(-3.14, 3.14, 0.05, 0, 200)
        self._hue_win = qtgui.RangeWidget(self._hue_range, self.set_hue, "hue", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._hue_win)
        self.epy_block_0_0 = epy_block_0_0.blk(u_gain=color_Strength, v_gain=color_Strength)
        self.epy_block_0 = epy_block_0.blk(threshold=threshhold)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(180)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, 'C:\\Users\\mirko\\Downloads\\test_file_output', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_const_vxx_1 = blocks.add_const_ff(broj)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(0.3)
        self.band_reject_filter_0 = filter.fir_filter_fff(
            1,
            firdes.band_reject(
                1,
                (samp_rate*0.4),
                4.1e6,
                4.8e6,
                2e5,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_1 = filter.interp_fir_filter_fcc(
            1,
            firdes.complex_band_pass(
                1,
                (samp_rate*0.4),
                3.5e6,
                5e6,
                5e5,
                window.WIN_HAMMING,
                6.76))
        self.analog_sig_source_x_0 = analog.sig_source_c((samp_rate*0.4), analog.GR_COS_WAVE, (-4.433618e6), 1, 0, 0)
        self.analog_rail_ff_0 = analog.rail_ff((-1), 1)
        self.analog_quadrature_demod_cf_0_0 = analog.quadrature_demod_cf(rangee)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0_0, 0), (self.band_pass_filter_1, 0))
        self.connect((self.analog_quadrature_demod_cf_0_0, 0), (self.band_reject_filter_0, 0))
        self.connect((self.analog_rail_ff_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.band_pass_filter_1, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.band_reject_filter_0, 0), (self.analog_rail_ff_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.epy_block_0, 0), (self.epy_block_0_0, 0))
        self.connect((self.epy_block_0, 1), (self.epy_block_0_0, 1))
        self.connect((self.epy_block_0, 2), (self.epy_block_0_0, 2))
        self.connect((self.epy_block_0_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.epy_block_0_0, 0), (self.network_tcp_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.epy_block_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.analog_quadrature_demod_cf_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "color_decoder_v2")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_threshhold(self):
        return self.threshhold

    def set_threshhold(self, threshhold):
        self.threshhold = threshhold
        self.epy_block_0.threshold = self.threshhold

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq((self.samp_rate*0.4))
        self.band_pass_filter_1.set_taps(firdes.complex_band_pass(1, (self.samp_rate*0.4), 3.5e6, 5e6, 5e5, window.WIN_HAMMING, 6.76))
        self.band_reject_filter_0.set_taps(firdes.band_reject(1, (self.samp_rate*0.4), 4.1e6, 4.8e6, 2e5, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, (self.samp_rate*0.4), self.filter_frequency, 400e3, window.WIN_HAMMING, 6.76))

    def get_rangee(self):
        return self.rangee

    def set_rangee(self, rangee):
        self.rangee = rangee
        self.analog_quadrature_demod_cf_0_0.set_gain(self.rangee)

    def get_rangedb(self):
        return self.rangedb

    def set_rangedb(self, rangedb):
        self.rangedb = rangedb
        self.uhd_usrp_source_0.set_gain(self.rangedb, 0)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset

    def get_line_length(self):
        return self.line_length

    def set_line_length(self, line_length):
        self.line_length = line_length

    def get_hue(self):
        return self.hue

    def set_hue(self, hue):
        self.hue = hue

    def get_filter_frequency(self):
        return self.filter_frequency

    def set_filter_frequency(self, filter_frequency):
        self.filter_frequency = filter_frequency
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, (self.samp_rate*0.4), self.filter_frequency, 400e3, window.WIN_HAMMING, 6.76))

    def get_color_Strength(self):
        return self.color_Strength

    def set_color_Strength(self, color_Strength):
        self.color_Strength = color_Strength
        self.epy_block_0_0.u_gain = self.color_Strength
        self.epy_block_0_0.v_gain = self.color_Strength

    def get_broj(self):
        return self.broj

    def set_broj(self, broj):
        self.broj = broj
        self.blocks_add_const_vxx_1.set_k(self.broj)




def main(top_block_cls=color_decoder_v2, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    snippets_main_after_init(tb)
    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
