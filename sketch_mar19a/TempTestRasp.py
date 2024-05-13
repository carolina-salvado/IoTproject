import Adafruit_DHT
import time 
sensor = Adafruit_DHT.DHT22
pin = 26

while True:
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		print("Temp = {0:0.1f}*C Humidity = {1:0.1f}/".format(temperature, humidity))
	else :
		print("Sensor failure")
	time.sleep(1800) #wait 1800 sec (30 min) before next measurement 
