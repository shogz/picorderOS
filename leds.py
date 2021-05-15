#!/usr/bin/python
print("Loading Unified Indicator Module")
# Provides a surface for control over the LEDs connected via GPIO. For the tr-tr108
# LEDs are controlled directly from GPIO, for the tr109 a shift register is used

from objects import *

# External module import
if not configure.pc:
	import RPi.GPIO as GPIO

# the following constants are for the pin addresses of the shift register
# the tr109 supports two shift registers, and so two sets of pin addresses
# prototype unit 00 and 01 have different pin assignments for latch and clock
# so these values may need to be swapped
PIN_DATA  = 16
PIN_LATCH = 6
PIN_CLOCK = 20
PIN_DATA2 = 17
PIN_LATCH2 = 22
PIN_CLOCK2 = 27

# a list of the pin data, for loop purposes.
PINS = [[PIN_DATA,PIN_LATCH,PIN_CLOCK],[PIN_DATA2,PIN_LATCH2,PIN_CLOCK2]]

# set the mode of the shift register pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_DATA,  GPIO.OUT)
GPIO.setup(PIN_LATCH, GPIO.OUT)
GPIO.setup(PIN_CLOCK, GPIO.OUT)
GPIO.setup(PIN_DATA2,  GPIO.OUT)
GPIO.setup(PIN_LATCH2, GPIO.OUT)
GPIO.setup(PIN_CLOCK2, GPIO.OUT)


# delivers data to the shift register
def shiftout(byte,board = 0):
	GPIO.output(PINS[board][1], 0)
	for x in range(8):
		GPIO.output(PINS[board][0], (byte >> x) & 1)
		GPIO.output(PINS[board][2], 1)
		GPIO.output(PINS[board][2], 0)
	GPIO.output(PINS[board][1], 1)

# loads the pin configurations and modes for the tr-108  (3 leds)
if configure.tr108:

	led1 = 4
	led2 = 17
	led3 = 27

	GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
	GPIO.setup(led1, GPIO.OUT) # LED pin set as output
	GPIO.setup(led2, GPIO.OUT) # LED pin set as output
	GPIO.setup(led3, GPIO.OUT) # LED pin set as output

#loads the pin configurations and modes for the tr-109 (many switches)
if configure.tr109:
# Pin Definitons:
	led1 = 16 #19 # Broadcom pin 19
	led2 = 20 #6 # Broadcom pin 13
	led3 = 6 #20
	led4 = 19 #16
	sc_led = 15

	# Pin Setup:
	GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
	GPIO.setup(led1, GPIO.OUT) # LED pin set as output
	GPIO.setup(led2, GPIO.OUT) # LED pin set as output
	GPIO.setup(led3, GPIO.OUT) # LED pin set as output
	GPIO.setup(led4, GPIO.OUT) # LED pin set as output
	GPIO.setup(sc_led, GPIO.OUT)


# a function to clear the gpio
def cleangpio():
	resetleds()
	GPIO.cleanup() # cleanup all GPIO

# a function to clear the LEDs
def resetleds():
	if configure.tr109:
		shiftout(0)
		shiftout(0, board = 1)
	if configure.tr108:
		GPIO.output(led1, GPIO.LOW)
		GPIO.output(led2, GPIO.LOW)
		GPIO.output(led3, GPIO.LOW)

	# if configure.tr109:
	# 	GPIO.output(led1, GPIO.LOW)
	# 	GPIO.output(led2, GPIO.LOW)
	# 	GPIO.output(led3, GPIO.LOW)
	# 	GPIO.output(led4, GPIO.LOW)
	# 	GPIO.output(sc_led, GPIO.LOW)



# # The following set of functions are for activating each LED individually.
# # I figured it was easier than having different functions for different combinations.
# # This way you can just manually set them as you please.
def screen_on():
	GPIO.output(sc_led, GPIO.HIGH)

def leda_on():
	GPIO.output(led1, GPIO.HIGH)

def ledb_on():
	GPIO.output(led2, GPIO.HIGH)

def ledc_on():
	GPIO.output(led3, GPIO.HIGH)

def ledd_on():
	GPIO.output(led4, GPIO.HIGH)

def leda_off():
	GPIO.output(led1, GPIO.LOW)

def ledb_off():
	GPIO.output(led2, GPIO.LOW)

def ledc_off():
	GPIO.output(led3, GPIO.LOW)

def ledd_off():
	GPIO.output(led4, GPIO.LOW)
#
def screen_off():
	GPIO.output(sc_led, GPIO.LOW)

# The following class drives the ripple animation for the tr-109.
class ripple(object):

	def __init__(self):
		self.beat = 0
		self.disabled = False
		self.statuswas = False
		self.lights = True
		pass

	def cycle(self):

		# because the tr-109 uses a shift register to drive its indicator LEDs
		# each frame of LED animations is represented by a byte, with the LEDs
		# being arranged as follows:

		#	0		0		0		0		0		0		0		0
		#	a		b		d		g		pwr		a1		b1		d1

		# the basic ripple animation is as follows.
		#140
		#74
		#41
		#26

		# if sleep detection is active:
		if configure.sleep[0]:
			#check if the door is open.
			if configure.dr_open[0]:
				# if it wasn't open last time.
				if self.statuswas != configure.dr_open[0]:
					# turn on our screen
					screen_on()
				# engage the lights
				self.lights = True
				self.statuswas = configure.dr_open[0]
			else:
				screen_off()
				self.lights = False
				self.statuswas = configure.dr_open[0]
		else:
			screen_on()


		# if lights are engaged this block of code will run the animation, or else
		# turn them off.
		if self.lights:
			self.beat += 1

			if self.beat > 3:
				self.beat = 0

			if self.beat == 0:
				shiftout(140)
				shiftout(140,board = 1)

			if self.beat == 1:
				shiftout(74)
				shiftout(74,board = 1)

			if self.beat == 2:
				shiftout(41)
				shiftout(41, board = 1)

			if self.beat == 3:
				shiftout(26)
				shiftout(26, board = 1)
		else:
			shiftout(0)
			shiftout(0,board =1)
