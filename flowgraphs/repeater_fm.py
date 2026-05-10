#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SDR Radio
# Author: Ian Henry, G0LFT
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import soapy
import os
import sip
import threading



class repeater_fm(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "SDR Radio", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("SDR Radio")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "repeater_fm")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.freq_khz = freq_khz = 145750
        self.samp_rate = samp_rate = 1000000
        self.record_toggle = record_toggle = 0
        self.freqcor = freqcor = 0
        self.filename_input = filename_input = 'repeater_fm_capture.iq'
        self.center_freq = center_freq = freq_khz * 1e3

        ##################################################
        # Blocks
        ##################################################

        self._record_toggle_choices = {'Pressed': 1, 'Released': 0}

        _record_toggle_toggle_button = qtgui.ToggleButton(self.set_record_toggle, 'Capture IQ', self._record_toggle_choices, False, 'value')
        _record_toggle_toggle_button.setColors("default", "default", "red", "default")
        self.record_toggle = _record_toggle_toggle_button

        self.top_grid_layout.addWidget(_record_toggle_toggle_button, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freqcor_range = qtgui.Range(-5, 5, 0.001, 0, 200)
        self._freqcor_win = qtgui.RangeWidget(self._freqcor_range, self.set_freqcor, "Frequency Correction Offset", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freqcor_win)
        self._filename_input_tool_bar = Qt.QToolBar(self)
        self._filename_input_tool_bar.addWidget(Qt.QLabel("Filename" + ": "))
        self._filename_input_line_edit = Qt.QLineEdit(str(self.filename_input))
        self._filename_input_tool_bar.addWidget(self._filename_input_line_edit)
        self._filename_input_line_edit.editingFinished.connect(
            lambda: self.set_filename_input(str(str(self._filename_input_line_edit.text()))))
        self.top_grid_layout.addWidget(self._filename_input_tool_bar, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.soapy_sdrplay_source_0 = None
        _agc_setpoint = int((-10))
        _agc_setpoint = max(min(_agc_setpoint, -20), -70)

        dev = 'driver=sdrplay'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        def _set_soapy_sdrplay_source_0_gain_mode(channel, agc):
            self.soapy_sdrplay_source_0.set_gain_mode(channel, agc)
            if not agc:
                self.set_soapy_sdrplay_source_0_gain(channel, self._soapy_sdrplay_source_0_gain_value)
        self.set_soapy_sdrplay_source_0_gain_mode = _set_soapy_sdrplay_source_0_gain_mode
        self._soapy_sdrplay_source_0_gain_value = 30

        def _set_soapy_sdrplay_source_0_gain(channel, gain):
            self._soapy_sdrplay_source_0_gain_value = gain
            if not self.soapy_sdrplay_source_0.get_gain_mode(channel):
                self.soapy_sdrplay_source_0.set_gain(channel, 'IFGR', min(max(59 - gain, 20), 59))
        self.set_soapy_sdrplay_source_0_gain = _set_soapy_sdrplay_source_0_gain

        def _set_soapy_sdrplay_source_0_lna_state(channel, lna_state):
                self.soapy_sdrplay_source_0.set_gain(channel, 'RFGR', min(max(lna_state, 0), 9))
        self.set_soapy_sdrplay_source_0_lna_state = _set_soapy_sdrplay_source_0_lna_state

        self.soapy_sdrplay_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_sdrplay_source_0.set_sample_rate(0, samp_rate)
        self.soapy_sdrplay_source_0.set_bandwidth(0, 0.0)
        self.soapy_sdrplay_source_0.set_antenna(0, 'A')
        self.soapy_sdrplay_source_0.set_frequency(0, center_freq)
        self.soapy_sdrplay_source_0.set_frequency_correction(0, freqcor)
        # biasT_ctrl is not always available and leaving it blank avoids errors
        if '' != '':
            self.soapy_sdrplay_source_0.write_setting('biasT_ctrl', )
        self.soapy_sdrplay_source_0.write_setting('agc_setpoint', (-10))
        self.set_soapy_sdrplay_source_0_gain_mode(0, True)
        self.set_soapy_sdrplay_source_0_gain(0, 30)
        self.set_soapy_sdrplay_source_0_lna_state(0, 0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=50,
                taps=[],
                fractional_bw=0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['In-Phase (I)', 'Quadrature (Q)', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            8192, #size
            'SDR Radio IQ Plot', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.002)
        self.qtgui_const_sink_x_0.set_y_axis((-0.4), 0.4)
        self.qtgui_const_sink_x_0.set_x_axis((-0.4), 0.4)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)

        self.qtgui_const_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [0, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win, 1, 2, 2, 1)
        for r in range(1, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(10, firdes.low_pass(1, samp_rate, 40e3, 20e3), 0, samp_rate)
        self._freq_khz_tool_bar = Qt.QToolBar(self)
        self._freq_khz_tool_bar.addWidget(Qt.QLabel("Frequency (kHz)" + ": "))
        self._freq_khz_line_edit = Qt.QLineEdit(str(self.freq_khz))
        self._freq_khz_tool_bar.addWidget(self._freq_khz_line_edit)
        self._freq_khz_line_edit.editingFinished.connect(
            lambda: self.set_freq_khz(eng_notation.str_to_num(str(self._freq_khz_line_edit.text()))))
        self.top_grid_layout.addWidget(self._freq_khz_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, os.path.join("..", "data", filename_input) if record_toggle == 1 else os.devnull, False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.audio_sink_0_0 = audio.sink(48000, '', True)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=50000,
        	quad_rate=100000,
        	tau=(75e-6),
        	max_dev=5e3,
          )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.soapy_sdrplay_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.soapy_sdrplay_source_0, 0), (self.qtgui_freq_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "repeater_fm")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_freq_khz(self):
        return self.freq_khz

    def set_freq_khz(self, freq_khz):
        self.freq_khz = freq_khz
        self.set_center_freq(self.freq_khz * 1e3)
        Qt.QMetaObject.invokeMethod(self._freq_khz_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq_khz)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1, self.samp_rate, 40e3, 20e3))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.soapy_sdrplay_source_0.set_sample_rate(0, self.samp_rate)

    def get_record_toggle(self):
        return self.record_toggle

    def set_record_toggle(self, record_toggle):
        self.record_toggle = record_toggle
        self.blocks_file_sink_0.open(os.path.join("..", "data", self.filename_input) if self.record_toggle == 1 else os.devnull)

    def get_freqcor(self):
        return self.freqcor

    def set_freqcor(self, freqcor):
        self.freqcor = freqcor
        self.soapy_sdrplay_source_0.set_frequency_correction(0, self.freqcor)

    def get_filename_input(self):
        return self.filename_input

    def set_filename_input(self, filename_input):
        self.filename_input = filename_input
        Qt.QMetaObject.invokeMethod(self._filename_input_line_edit, "setText", Qt.Q_ARG("QString", str(self.filename_input)))
        self.blocks_file_sink_0.open(os.path.join("..", "data", self.filename_input) if self.record_toggle == 1 else os.devnull)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.soapy_sdrplay_source_0.set_frequency(0, self.center_freq)




def main(top_block_cls=repeater_fm, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

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
