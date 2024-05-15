import BlynkLib
import random
import time
from BlynkTimer import BlynkTimer
import Adafruit_DHT
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
TRIG = 17
ECHO = 4
#distance sensor setup
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)


BLYNK_AUTH = "OS5uWHlVwpyopOvxfaDn2QVb5d14WGEh"
blynk = BlynkLib.Blynk(BLYNK_AUTH,server='lon1.blynk.cloud')
timer = BlynkTimer()


sensor = Adafruit_DHT.DHT22
pin = 26
def temp_sensor():
	#num = random.choice(range(-20,40))
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		blynk.virtual_write(0,temperature)
		blynk.virtual_write(2,humidity)
		print(temperature, humidity)

def distance_sensor():
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
	if distance > 220:
		blynk.virtual_write(3, 0)
	else:
		blynk.virtual_write(3, distance)

@blynk.VIRTUAL_WRITE(1)
def write_virtual_pin_handler(value):
	print(value)

timer.set_interval(10,temp_sensor)
timer.set_interval(2, distance_sensor)
time.sleep(2)
while True:
	blynk.run()
	timer.run()
