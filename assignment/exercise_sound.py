#!/usr/bin/env python3
"""
Fur ELise Song:
Naomi G and Anirudh S
- playtone() and quiet() found on https://www.coderdojotc.org/micropython/sound/04-play-scale/
- used sheet music: https://musescore.com/user/2816076/scores/5418894
"""

import machine
import utime

# Notes in Hz
E5 = 659.255
DS5 = 622.254
B4 = 493.883
D5 = 587.330
C5 = 523.251
A4 = 440
C4 = 261.626
E4 = 329.628
GS4 = 415.305
G4 = 391.995
F5 = 698.456
F4 = 349.228
REST = -1

# Note lengths
QUARTER = 4
EIGHTH = 2
HALF = 8
HALF_DOTTED = 12

TEMPO = 0.12
SPACING = 0.025

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))

# Fur Elise notes 
song_notes = [
    [REST, E5, DS5, E5, DS5, E5, B4, D5, C5, A4, REST, C4, E4, A4, B4, REST, E4, GS4, B4, C5, REST, E4, E5, DS5],
    [E5, DS5, E5, B4, D5, C5, A4, REST, C4, E4, A4, B4, REST, E4, C5, B4, A4, REST, B4, C5, D5, E5, REST, G4, F5, E5],
    [D5, REST, F4, E5, D5, C5, REST, E4, D5, C5, B4, REST, E5, DS5],
    [E5, DS5, E5, B4, D5, C5, A4, REST, C4, E4, A4, B4, REST, E4, GS4, B4, C5, REST, E4, E5, DS5],
    [E5, DS5, E5, B4, D5, C5, A4, REST, C4, E4, A4, B4, REST, E4, C5, B4, A4]
]

# Measure lengths
two8 = [HALF, EIGHTH, EIGHTH]
six8 = [EIGHTH, EIGHTH, EIGHTH, EIGHTH, EIGHTH, EIGHTH]
four8 = [QUARTER, EIGHTH, EIGHTH, EIGHTH, EIGHTH]
zero8 = [HALF_DOTTED]

# measure lengths in order
song_times = [ 
    [two8, six8, four8, four8, four8], 
    [six8, four8, four8, four8, four8],
    [four8, four8, zero8, two8],
    [six8, four8, four8, four8],
    [six8, four8, four8, zero8],

]

#initil status 
line = 0
a = 0
b = 0
c = 0
current_measure = song_times[line][b]

def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)
    speaker.freq(int(frequency))
    utime.sleep(duration)


def quiet():
    speaker.duty_u16(0)

while line < len(song_notes):
    a = 0
    b = 0
    c = 0
    while a < len(song_notes[line]):
        current_note = song_notes[line][a]
        current_note_length = current_measure[c]
        print(f"Playing Note: {current_note}")
        if current_note == REST:
            quiet()
            utime.sleep(current_note_length * TEMPO)
        else:
            playtone(current_note, current_note_length * TEMPO)
        
        # Spacing between notes
        quiet()
        utime.sleep(SPACING)

        # Move to the next note
        a+=1
        c+=1
        if c >= len(current_measure):
            c = 0
            b += 1
            if b >= len(song_times[line]):
                break
            current_measure = song_times[line][b]
    line += 1
    if line < len(song_notes):
        current_measure = song_times[line][0]
    

# Turn off the PWM
quiet()
