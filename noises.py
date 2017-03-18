"""Module for managing sound effects."""

import subprocess
from subprocess import Popen
import logging
import os
import time

logger = logging.getLogger("RaspberrySoundBoard.noises")
#remove these when integrated
#logger.setLevel(logging.DEBUG)
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#ch.setFormatter(formatter)
#logger.addHandler(ch)

active_noise = None
#configuration
initial_volume = 40
#time_to_fade = 0.5
#maybe have a variable fade, based on the position of the track in the sketch?
time_to_fade = 1.25
fade_out_steps = 10
seconds_per_fade_step = time_to_fade / fade_out_steps
volume_steps_per_fade = initial_volume / fade_out_steps

#compute what media player we will use
which_ffplay = subprocess.call(["which", "ffplay"])
if which_ffplay == 0:
    media_player = "ffplay"
which_afplay = subprocess.call(["which", "afplay"])
if which_afplay == 0:
    media_player = "afplay"
which_mpg123 = subprocess.call(["which", "mpg123"])
if which_mpg123 == 0: 
    media_player = "mpg123"
logger.info("Media player is " + media_player)

def volume_osx(new_volume):
    subprocess.call(['osascript', '-e', "set volume output volume " + str(new_volume)])
def volume_rpi(new_volume):
    modded_volume = (new_volume / 2.0) + 50
    logger.debug('setting volume from raw {} to modded {}'.format(new_volume, modded_volume))
    subprocess.call(['amixer', 'cset', '-q', 'numid=1', str(modded_volume)+'%'])


#compute what media player we will use
which_osascript = subprocess.call(["which", "osascript"])
if which_osascript == 0:
    set_volume = volume_osx
which_amixer = subprocess.call(["which", "amixer"])
if which_amixer == 0:
    set_volume = volume_rpi
    #the pi needs it loud(er than my MBP)?
    initial_volume = 100

logger.info("Our volume control is: {}".format(set_volume))


def fade_out(fade_out_seconds=time_to_fade):
    current_volume = initial_volume
    fade_out_steps = 10
    seconds_per_fade_step = fade_out_seconds / fade_out_steps
    volume_steps_per_fade = current_volume / fade_out_steps
    while current_volume >= 0:
        set_volume(current_volume)
        time.sleep(seconds_per_fade_step)
        current_volume -= volume_steps_per_fade

def play_from_path(path):
    global active_noise
    path_to_open = path
    set_volume(initial_volume)
    logger.info("About to play {}".format(path_to_open))
    active_noise = Popen([media_player, path_to_open])
    if active_noise is None:
        logger.warn("got none back from Popen")

def stop(seconds_to_fade_out=time_to_fade):
    logger.info("in stop")
    if seconds_to_fade_out is None or seconds_to_fade_out == "":
        seconds_to_fade_out = time_to_fade
    if not is_playing():
        logger.info("not playing")
        return
    if active_noise is not None:
        fade_out(seconds_to_fade_out)
        logger.info("going to kill")
        active_noise.kill()
    logger.info("done")

def is_playing():
    return active_noise is not None and active_noise.poll() is None

