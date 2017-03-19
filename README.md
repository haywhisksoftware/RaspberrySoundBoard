# Raspberry Sound Board

## A sound board for Raspberry Pi.

It plays noises.

### You'll need
1. pyqt5
1. python3
1. mpg123 (if running on Raspberry Pi) or afplay (if running on OS X)

### You'll need to configure your cue list thusly:
1. make a CSV file named `cue_list.csv`
1. give it these columns:
   1. sketch
      1. the name of the scene or sketch the sound belongs to. Currently unsued.
   1. cue
      1. the thing that cues the sound (e.g, for a fart noise: "Gregg lifts his buttcheek")
   1. fade_out_time
      1. the length in seconds that it should take to stop playing the currently playing noise. Defaults to something configured in noises.py
   1. track  
      1. the filename relative to the `noises` directory

### You'll need to layout your directories thusly:
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

### Invoke it thusly:
```
python3 simple_window.py
```
