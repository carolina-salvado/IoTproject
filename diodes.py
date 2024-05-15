import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
for i in range(1, 1000):
    GPIO.output(22, True)
    time.sleep(2/i)
    GPIO.output(22, False)
    time.sleep(2/i)
    print(i)
# GPIO.output(27, True)
# GPIO.output(27, False)
GPIO.cleanup()
