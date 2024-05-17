import BlynkLib
import random
import time
from BlynkTimer import BlynkTimer
import Adafruit_DHT
import RPi.GPIO as GPIO
import requests
import threading

GPIO.setmode(GPIO.BCM)
TRIG = 17
ECHO = 4
#distance sensor setup
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)
distance = 0

#led setup
green_pin = 27
red_pin = 22
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.output(green_pin, False)
GPIO.output(red_pin, False)

BLYNK_HOSTNAME = "lon1.blynk.cloud"
BLYNK_AUTH = "OS5uWHlVwpyopOvxfaDn2QVb5d14WGEh"
blynk = BlynkLib.Blynk(BLYNK_AUTH,server=BLYNK_HOSTNAME)
timer = BlynkTimer()

def http_send(pin, value):
    requests.get(f"http://{BLYNK_HOSTNAME}/external/api/update?token={BLYNK_AUTH}&V{pin}={value}")

sensor = Adafruit_DHT.DHT22
pin = 26
def temp_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        http_send(0,temperature)
        http_send(2,humidity)
        
def distance_sensor():
    global distance
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    if distance < 40:
        distance_latency = distance / 80
        GPIO.output(green_pin, False)
        GPIO.output(red_pin, True)
        time.sleep(distance_latency)
        GPIO.output(red_pin, False)
        time.sleep(distance_latency)
    else:
        GPIO.output(green_pin, True)
        GPIO.output(red_pin, False)

def distance_send():
    global distance
    if distance <= 220:
        http_send(3, distance)
    else:
        http_send(3, 0)

timer.set_interval(10, temp_sensor)
timer.set_interval(2, distance_send)
time.sleep(2)
while True:
    thread = threading.Thread(target=distance_sensor)
    thread.start()
    blynk.run()
    timer.run()
    time.sleep(0.1)