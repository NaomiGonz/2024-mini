#!/usr/bin/env python3
"""
Fur ELise Song:
Naomi G and Anirudh S
playtone() and quiet() found on https://www.coderdojotc.org/micropython/sound/04-play-scale/
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

TEMPO = 100
SPACING = 0.3

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))

song_notes = [
    [REST, E5, DS5, E5, DS5, E5, B4, D5, C5, A4, REST, C4, E4, A4, B4, REST, E4, GS4, B4, C5, REST, E4, E5, DS5],
    [E5, DS5, E5, B4, D5, C5, A4, REST, C4, E4, A4, B4, REST, E4, C5, B4, A4, REST, B4, C5, D5, E5, REST, G4, F5, E5],
    [D5, REST, F4, E5, D5, C5, REST, E4, D5, C5, B4, REST, E5, DS5],
    [E5, DS5, E5, B4, D5, C5, A4, REST, C4, E4, A4, B4, REST, E4, GS4, B4, C5, REST, E4, E5, DS5],
    [E5, DS5, E5, B4, D5, C5, A4, REST, C4, E4, A4, B4, REST, E4, C5, B4, A4]
]

song_times = [
    [HALF, EIGHTH, EIGHTH, EIGHTH, EIGHTH, EIGHTH, EIGHTH, EIGHTH, EIGHTH, QUARTER, EIGHTH, EIGHTH, EIGHTH, EIGHTH, ],
]

#initil status 
a = 0
b = 0

def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)
    speaker.freq(frequency)
    utime.sleep(duration)


def quiet():
    speaker.duty_u16(0)


freq: float = 30
duration: float = 0.1  # seconds

print("Playing frequency (Hz):")

for i in range(64):
    print(freq)
    playtone(freq, duration)
    freq = int(freq * 1.1)

# Turn off the PWM
quiet()
