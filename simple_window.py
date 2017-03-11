#!/usr/bin/python
# -*- coding: utf-8 -*-

import module_locator

from csv import DictReader
import logging
import os.path
import subprocess
import sys
#from PyQt4 import QtGui
from PyQt5.QtWidgets import QApplication, QListWidget, QWidget, QPushButton, QTextEdit


my_path = module_locator.module_path()

logger = logging.getLogger('RaspberrySoundBoard')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler(os.path.join(my_path, 'swt.log'))
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


def load_cues(filename, error_on_missing_track=False, default_track=os.path.join(my_path, 'noises','default_track.mp3')):
    cues = []
    with open(os.path.join(my_path, filename), 'r') as cues_csv:
        dr = DictReader(cues_csv)
        for d in dr:
            if 'track' not in d.keys() or d['track'] is None or len(d['track'].strip()) == 0 or not os.path.isfile(os.path.join(my_path, filename)):
                if not error_on_missing_track:
                    logger.warn('No file found for sketch {}, cue {}, track {}'.format(d['sketch'], d['cue'], d['track']))
                    d['track'] = default_track
                else:
                    raise ValueError('no track for sketch {} and cue {}'.format(d['sketch'], d['cue']))
            else:
                #this is getting wonky.
                #TODO: standardize file loading so that we consistently load from my_path/...
                d['track'] = os.path.join(my_path, 'noises', d['track'])
            cues.append(d)
    return cues

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

noises_to_play = load_cues('cue_list.csv')
    
class SimpleButtonTest(QWidget):
    def __init__(self):
        super(SimpleButtonTest, self).__init__()

        self.initUI()

    def initUI(self):
        play_button = QPushButton('Play next cue', self)
        play_button.resize(125, 50)
        play_button.move(window_width-130, 0)
        play_button.clicked.connect(lambda: self.start_noise())

        stop_button = QPushButton('Stop!', self)
        stop_button.resize(55, 50)
        stop_button.move(window_width-55, window_height-50)
        stop_button.clicked.connect(lambda: self.stop_noise())

        now_playing = QTextEdit(self)
        now_playing.setReadOnly(True)
        now_playing.resize(125, 25)
        now_playing.move(window_width-125, window_height-125)
        up_next = QTextEdit(self)
        up_next.setReadOnly(True)
        up_next.resize(125, 25)
        up_next.move(window_width-125, window_height-75)

        prev_button = QPushButton('^', self)
        prev_button.resize(25, 25)
        prev_button.move(window_width - 125, window_height - 175)
        prev_button.clicked.connect(self.prev_cue)
        next_button = QPushButton('V', self)
        next_button.resize(25, 25)
        next_button.move(window_width - 75, window_height - 175)
        next_button.clicked.connect(self.next_cue)

        sound_list = QListWidget(self)
        for i in noises_to_play:
            sound_list.addItem(i['cue'])
        sound_list.resize(150, window_height)
        sound_list.move(0, 0)

        self.queued_index = 0

        up_next.setText(noises_to_play[self.queued_index]['cue'])

        self.up_next = up_next
        self.now_playing = now_playing
        self.sound_list = sound_list

        self.setGeometry(0,0, window_width,window_height)
        self.setWindowTitle("Raspberry Sound Board")
        self.show()

    def play_noise(self, filename):
        noises.play_from_path(os.path.join(my_path, filename))

    def prev_cue(self):
        self.queued_index -= 1
        if self.queued_index < 0:
            self.queued_index = len(noises_to_play)-1
        self.sound_list.setCurrentRow(self.queued_index)
        self.up_next.setText(noises_to_play[self.queued_index]['cue'])

    def next_cue(self):
        self.queued_index += 1
        if self.queued_index >= len(noises_to_play):
            self.queued_index = 0
        self.sound_list.setCurrentRow(self.queued_index)
        self.up_next.setText(noises_to_play[self.queued_index]['cue'])

    def start_noise(self):
        self.stop_noise()
        self.now_playing.setText(noises_to_play[self.queued_index]['cue'])
        noises.play_from_path(os.path.join("noises", noises_to_play[self.queued_index]['track']))
        self.sound_list.setCurrentRow(self.queued_index)
        self.queued_index += 1
        if self.queued_index >= len(noises_to_play):
            self.queued_index = 0
        self.up_next.setText(noises_to_play[self.queued_index]['cue'])

    def stop_noise(self):
        self.now_playing.setText('')
        noises.stop()

def main():
    app = QApplication(sys.argv)
    sbt = SimpleButtonTest()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
