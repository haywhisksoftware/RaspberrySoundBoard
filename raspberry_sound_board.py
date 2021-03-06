#!/usr/bin/python
# -*- coding: utf-8 -*-

import module_locator

from csv import DictReader
import logging
import os.path
import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QListWidget, QWidget, QPushButton, QTextEdit
from PyQt5.QtCore import Qt


my_path = module_locator.module_path()

logger = logging.getLogger('RaspberrySoundBoard')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler(os.path.join(my_path, 'rsb.log'))
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
            if 'track' not in d.keys() or d['track'] is None or len(d['track'].strip()) == 0 or not os.path.isfile(os.path.join(my_path, 'noises', d['track'])):
                if not error_on_missing_track:
                    logger.warn('No file found for sketch {}, cue {}, track {}'.format(d['sketch'], d['cue'], d['track']))
                    d['track'] = default_track
                else:
                    raise ValueError('no track for sketch {} and cue {}'.format(d['sketch'], d['cue']))
            else:
                #this is getting wonky.
                #TODO: standardize file loading so that we consistently load from my_path/...
                d['track'] = os.path.join(my_path, 'noises', d['track'])
            if d['fade_out_time'] is None or d['fade_out_time'] == "":
                d['fade_out_time'] = None
            else:
                d['fade_out_time'] = float(d['fade_out_time'])
            cues.append(d)
    return cues

#our stuff
import noises
                
window_width = 320
window_height = 215

noises_to_play = load_cues('cue_list.csv')
    
class RaspberrySoundBoard(QWidget):
    def __init__(self):
        super(RaspberrySoundBoard, self).__init__()

        self.initUI()

    def initUI(self):
        play_button = QPushButton('Play next cue', self)
        play_button.resize(135, 65)
        play_button.move(window_width-135, 0)
        play_button.clicked.connect(lambda: self.start_noise())

        stop_button = QPushButton('Stop!', self)
        stop_button.resize(65, 50)
        stop_button.move(window_width-55, window_height-50)
        stop_button.clicked.connect(lambda: self.stop_noise())

        now_playing_label = QLabel(self)
        now_playing_label.setText("Now:")
        now_playing_label.move(window_width-155, window_height-105)
        now_playing = QTextEdit(self)
        now_playing.setReadOnly(True)
        now_playing.resize(125, 25)
        now_playing.move(window_width-125, window_height-105)
        up_next_label = QLabel(self)
        up_next_label.setText("Next:")
        up_next_label.move(window_width-155, window_height-70)
        up_next = QTextEdit(self)
        up_next.setReadOnly(True)
        up_next.resize(125, 25)
        up_next.move(window_width-125, window_height-70)

        prev_button = QPushButton('^', self)
        prev_button.resize(45, 45)
        prev_button.move(window_width - 135, window_height - 150)
        prev_button.clicked.connect(self.prev_cue)
        next_button = QPushButton('V', self)
        next_button.resize(45, 45)
        next_button.move(window_width - 50, window_height - 150)
        next_button.clicked.connect(self.next_cue)

        sound_list = QListWidget(self)
        for i in noises_to_play:
            sound_list.addItem(i['cue'])
        sound_list.resize(150, window_height)
        sound_list.move(0, 0)

        self._queued_index = 0

        up_next.setText(self.get_queued_cue()['cue'])

        self.up_next = up_next
        self.now_playing = now_playing
        self.sound_list = sound_list

        self._now_playing_cue = None

        self.setGeometry(0,0, window_width,window_height)
        self.setWindowTitle("Raspberry Sound Board")
        self.setFocusPolicy(Qt.StrongFocus)
        self.show()

    def get_queued_cue(self):
        return noises_to_play[self._queued_index]

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            #don't exit
            pass
        elif key == Qt.Key_Down:
            self.next_cue()
        elif key == Qt.Key_Up:
            self.prev_cue()
        elif key == Qt.Key_Right:
            self.start_noise()
        elif key == Qt.Key_Left:
            self.stop_noise()
        elif key == Qt.Key_1:
            self.next_cue()
        else:
            #super(QWidget, self).keyPressEvent(event)
            pass

    def play_noise(self, cue):
        noises.play_from_path(os.path.join(my_path, cue['track']))
        self._now_playing_cue = cue

    def prev_cue(self):
        self._queued_index -= 1
        if self._queued_index < 0:
            self._queued_index = len(noises_to_play)-1
        self.sound_list.setCurrentRow(self._queued_index)
        self.up_next.setText(noises_to_play[self._queued_index]['cue'])

    def next_cue(self):
        self._queued_index += 1
        if self._queued_index >= len(noises_to_play):
            self._queued_index = 0
        self.sound_list.setCurrentRow(self._queued_index)
        self.up_next.setText(noises_to_play[self._queued_index]['cue'])

    def start_noise(self):
        self.stop_noise()
        now_playing_cue = self.get_queued_cue()
        self.now_playing.setText(now_playing_cue['cue'])
        self.play_noise(now_playing_cue)
        self.sound_list.setCurrentRow(self._queued_index)
        self.next_cue()

    def stop_noise(self):
        self.now_playing.setText('')
        if self._now_playing_cue is not None:
            noises.stop(self._now_playing_cue['fade_out_time'])

def main():
    app = QApplication(sys.argv)
    rsb = RaspberrySoundBoard()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
