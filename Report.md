# 2024 Fall Miniproject Report

## Exersice 1 Questions 
max_bright = 608
min_bright = 52652

Design Description:
    we adjusted the min_bright value to 30000, which represents the lowest duty cycle, and the max_bright value to 1000, which corresponds to the highest duty cycle for bright light, after testing the sensor in a wide range. We looked at a list of generated values and worked on figuring out the average range and decided on the values mentioned above.

## Exercise 2 Question
Design Description:
    Pin GP16 was chosen for the speaker because it supports pulse width modulation (PWM), necessary to produce the different frequencies. We used playtone method to play each note for a certain amount of time, which essentially modulates the PWM frequency.

```python
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



```

## Exercise 3 Question
Design Description:
    In order to generate LED blink at random intervals, the random_time_interval is used. Through using these response times, we werre able to calculate different categories of response times and the times the player missed. The scorer function prints out the player's performance summary. We used firebase as our cloud service as it was relatively easier to use. We used urequests library in micropython to make an HTTP post request and push the created summary JSON file with all of the data onto the cloud.
```python
#modified game 
from machine import Pin
import time
import random
import json
import urequests
import network


N: int = 10
sample_ms = 10.0
on_ms = 500

# WiFi credentials
SSID = ""
PASSWORD = ""

# Firebase API URL
database_api_url = ""


def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print("Already connected to WiFi")
    else:
        # Connect to the WiFi network
        print(f"Connecting to WiFi network '{SSID}'...")
        wlan.connect(SSID, PASSWORD)

        max_wait = 10
        while max_wait > 0:
            if wlan.isconnected():
                print("Connected to WiFi!")
                break
            max_wait -= 1
            print("Waiting for connection...")
            time.sleep(1)

        if wlan.isconnected():
            print("Network config:", wlan.ifconfig())
            return wlan.ifconfig()
        else:
            print("Failed to connect to WiFi")
            return None


def random_time_interval(tmin: float, tmax: float) -> float:
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def scorer(t: list[int | None]) -> None:
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    if t_good:
        avg_response_time = sum(t_good) / len(t_good)
        min_response_time = min(t_good)
        max_response_time = max(t_good)
    else:
        avg_response_time = min_response_time = max_response_time = None

    print(f"Average Response Time: {avg_response_time} ms")
    print(f"Minimum Response Time: {min_response_time} ms")
    print(f"Maximum Response Time: {max_response_time} ms")

    # Prepare data to upload
    data = {
        "average_response_time": avg_response_time,
        "min_response_time": min_response_time,
        "max_response_time": max_response_time,
        "score": (len(t_good) / len(t)),
        "misses": misses,
        "timestamps": t
    }

    # Upload data to Firebase
    try:
        headers = {"Content-Type": "application/json"}
        response = urequests.post(database_api_url, headers=headers, data=json.dumps(data))
        print("Data uploaded to Firebase")
        response.close()
    except Exception as e:
        print(f"Failed to upload to Firebase: {e}")


if __name__ == "__main__":
    # Connect to WiFi
    connect_to_wifi()

    led = Pin("LED", Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)

    # Score and upload results
    scorer(t)
```
