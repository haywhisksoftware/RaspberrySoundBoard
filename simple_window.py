#!/usr/bin/python
# -*- coding: utf-8 -*-

import module_locator

import logging
import os.path
import subprocess
import sys
#from PyQt4 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton


my_path = module_locator.module_path()

logger = logging.getLogger('RaspberrySoundBoard')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler(os.path.join(my_path, 'swt.log'))
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

#our stuff
import noises

def my_global_function():
    logger.info("in my_global_function")
    path_to_open = os.path.join(my_path, "introduction_Dun-dun-dun-sound-effect-brass.mp3")
    noises.play_from_path(path_to_open)

def global_stop_function():
    noises.stop()

window_width = 320
window_height = 230
    
class SimpleButtonTest(QWidget):
    def __init__(self):
        super(SimpleButtonTest, self).__init__()

        self.initUI()

    def initUI(self):
        btn = QPushButton('Make a noise', self)
        btn.resize(btn.sizeHint())
        btn.move(0, 0)
        btn.clicked.connect(lambda: self.play_noise('introduction_Dun-dun-dun-sound-effect-brass.mp3'))

        im_button = QPushButton('Play IM', self)
        im_button.resize(40, 40)
        im_button.move(40, 40)
        im_button.clicked.connect(lambda: self.play_noise('IM-SF.mp3'))

        stop_button = QPushButton('Stop!', self)
        stop_button.resize(50, 50)
        stop_button.move(window_width-50, window_height-50)
        stop_button.clicked.connect(lambda: self.stop_noise())

        self.setGeometry(0,0, window_width,window_height)
        self.setWindowTitle("Simple Button Test")
        self.show()

    def play_noise(self, filename):
        noises.play_from_path(os.path.join(my_path, filename))

    def stop_noise(self):
        noises.stop()

def main():
    app = QApplication(sys.argv)
    sbt = SimpleButtonTest()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
