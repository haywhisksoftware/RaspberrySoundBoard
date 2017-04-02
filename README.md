# Raspberry Sound Board

## A sound board for Raspberry Pi.

Problem: sketch comedy shows need sound effects. These sound effects are largely in a specific order. There isn't a lot of space for a full-sized laptop at the sound desk. 
Solution: this thing. A Raspberry Pi and a keyboard fit nicely at the sound desk. This thing runs in OS X and Raspbian.

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
Note that probably the best way to do this is to have a shell script (located on your Pi's desktop) invoke this script.

### Control it thusly:
(Caveat: for keyboard controls, you may have to tap on empty space to de-focus a button, letting the main widget receive keyboard events.)
1. Play next cue
   1. plays the next cue, stopping the currently playing cue, if applicable.
   1. Keyboard: right arrow
1. ^
   1. sets the next cue to the previous cue. 
   1. Useful for re-playing a cue, or skipping around during rehearsal
   1 Keyboard: up arrow
1. V
   1. sets the next cue to the following cue.
   1. Useful for skipping ahead in the show, or skipping around during rehearsal
   1. Keyboard: down arrow
1. Stop!
   1. stops playing the currently playing cue, fading out according to the currently playing cue's fade_out_time value
   1. Keyboard: left arrow
