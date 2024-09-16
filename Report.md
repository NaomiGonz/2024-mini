# 2024 Fall Miniproject Report

## Exersice 1 Questions 
max_bright = 1000
min_bright = 30000

## Exercise 2 Question
```python




```

## Exercise 3 Question
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
