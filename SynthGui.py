#!/usr/bin/python
import sys, os, SynthCore
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread
from multiprocessing import Process
import time


class Timer(QThread):
    def __init__(self, event_receiver):
        QThread.__init__(self)
        self.event_receiver = event_receiver
        self.time = 0

    def run(self):
        while True:
            self.time += 1
            QApplication.postEvent(self.event_receiver, MyEvent(self.time))
            self.sleep(1)


class ScrollLayout(QtGui.QWidget):
    def updateVolumes(self):
        volumes = []
        for i in range(0, self.overtones + 1):
            volumes.append(self.sldWave[i].value() / 100.0)
        self.vol = volumes


    def __init__(self, parent=None, overtones=10):
        QtGui.QWidget.__init__(self, parent)
        self.overtones = overtones
        self.vol = [1]
        for i in range(1, overtones + 1):
            self.vol.append(0)
        l = QtGui.QHBoxLayout(self)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(0)
        s = QtGui.QScrollArea()
        l.addWidget(s)
        w = QtGui.QWidget(self)
        hbox = QtGui.QHBoxLayout(w)
        self.sldWave = []
        for i in range(0, overtones + 1):
            _l = QtGui.QVBoxLayout()
            self.sldWave.append(QtGui.QSlider(QtCore.Qt.Vertical, self))
            _l.addWidget(self.sldWave[i])
            self.sldWave[i].setFocusPolicy(QtCore.Qt.NoFocus)
            self.sldWave[i].setValue(self.vol[i] * 100)
            _l.addWidget(QtGui.QLabel("%d" % i, self))
            hbox.addLayout(_l)
        s.setWidget(w)

#Just another GUI class
class SynthGui(QtGui.QMainWindow):
    sliderval = 0

    def __init__(self):
        super(SynthGui, self).__init__()
        self.btn_x, self.btn_y = 11, 155
        self.btn_w, self.btn_h = 120, 30
        self.btn_d = 120
        self.play_file = "playthis"
        self.preset_file = ""
        self.vol = [1, 0.4, 0.3, 0.2, 0.1]
        self.overtones = 50
        self.block = False
        self.initUI()

        def timerEvent(self, event):
            if isinstance(event, MyEvent):
                self.append('time = %i' % event.data)

    def btnOpenFileClick(self):
        self.play_file = QtGui.QFileDialog.getOpenFileName(self, 'Open file')

    def playThis(self):
        self.vol = self.sa.updateVolumes()
        if (self.block == False):
            self.block = True
            pl = SynthCore.Player(self.overtones, self.sa.vol)
            try:
                pl.Play(self.play_file)
            except:
                pass

    def btnPlayClick(self):
        self.pr = Process(target=self.playThis)
        self.pr.start()


    def btnStopClick(self):
        self.pr.terminate()


    def btnShowWaveClick(self):
        self.vol = self.sa.updateVolumes()
        p = SynthCore.Player(self.overtones, self.sa.vol)
        p.showWaveform()


    def initUI(self):

        self.btnPlay = QtGui.QPushButton('Play', self)
        self.btnPlay.clicked.connect(self.btnPlayClick)
        self.btnPlay.setToolTip('<b>Play</b> button')
        self.btnPlay.setGeometry(self.btn_x, self.btn_y, self.btn_w, self.btn_h)

        btnStop = QtGui.QPushButton('Stop', self)
        btnStop.clicked.connect(self.btnStopClick)
        btnStop.setGeometry(self.btn_x + self.btn_d, self.btn_y, self.btn_w, self.btn_h)

        btnOpenFile = QtGui.QPushButton('Open file', self)
        btnOpenFile.clicked.connect(self.btnOpenFileClick)
        btnOpenFile.setGeometry(self.btn_x + self.btn_d * 2, self.btn_y, self.btn_w, self.btn_h)

        btnShowWave = QtGui.QPushButton('Show waveform', self)
        btnShowWave.clicked.connect(self.btnShowWaveClick)
        btnShowWave.setGeometry(self.btn_x + self.btn_d * 3, self.btn_y, self.btn_w, self.btn_h)

        self.sa = ScrollLayout(self, self.overtones)
        self.sa.setGeometry(5, 0, 490, 150)

        self.setFixedSize(500, 190)
        self.setWindowTitle('Synth')
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = SynthGui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
