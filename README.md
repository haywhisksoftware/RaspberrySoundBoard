Raspberry Sound Board

A sound board for Raspberry Pi.

It plays noises.

You'll need
# pyqt5
# python3

You'll need to configure your cue list thusly:
# make a CSV file named `cue_list.csv`
# give it these columns:
## sketch
### the name of the scene or sketch the sound belongs to. Currently unsued.
## cue
### the thing that cues the sound (e.g, for a fart noise: "Gregg lifts his buttcheek")
## fade_out_time
### the length in seconds that it should take to stop playing the currently playing noise. Defaults to something configured in noises.py
## track 
### the filename relative to the `noises` directory

You'll need to layout your directories thusly:
```
.
+ simple_window.py
+ noises.py
+ ...other scripts...
\ noises
 \ sketch_1
  + cue1.mp3
  + cue2.mp3
 \ sketch2
  + cue1.mp3
```
