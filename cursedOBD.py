# -*- coding: utf-8 -*-

"""
TODO:
X Build a basic progress bar function
	X Include labeling support
	X Setup "redline" value
	- Setup "precision" value
	- Allow taller progress bars (remove hardcoded y values)
- Get basic single OBD input
- Get multiple OBD inputs
- Create min/max system
- Priority stats:
	- Tachometer
	- Speedometer
	- Temps (engine/oil/air/etc)
- UI Layout (scaling, etc)
- Flash screen at redline (switch color theme)
- Other features:
	- 0-60 time
	- Gas mileage
"""

import curses
import time
from math import sin
from digGauge import *

stdscr = curses.initscr() # Start curses
curses.start_color() # Enable color
curses.curs_set(False) # Disable cursor
scrheight, scrwidth = stdscr.getmaxyx() # Grab screen size

curses.use_default_colors() # This is required to allow inheritence of the background color for the current terminal
curses.init_pair(1, curses.COLOR_WHITE, -1) # Standard text: White on default
curses.init_pair(2, curses.COLOR_RED, -1) # Redline: Red on default
curses.init_pair(3, curses.COLOR_CYAN, -1) # Redline needle: Cyan on default - Only shown past redline for emphasis
curses.init_pair(4, -1, curses.COLOR_RED) # Redline label: White on red

gauge_char = "█"
redline_char = "░"
redline_flash_char = "█"
needle_char = "█"

def my_precision(x, n): # https://stackoverflow.com/a/30897520
    return '{:.{}f}'.format(x, n)

def scaleValue(oldValue, oldMin, oldMax, newMin=0, newMax=1, clamp=True): # https://stackoverflow.com/a/929107
	if clamp:
		if oldValue < oldMin:
			oldValue = oldMin
		if oldValue > oldMax:
			oldValue = oldMax

	oldRange = (oldMax - oldMin)
	if (oldRange == 0):
		newValue = newMin
	else:
		newRange = (newMax - newMin)
		newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin
	return newValue

class Gauge:
	def __init__(self, title, x, y, width, height):
		self.title = title # Title
		self.x = x # X position
		self.y = y # Y position
		self.width = width # Full width of the gauge window
		self.height = height # Full height of the gauge window

		# Optional values
		self.min = 0 # Define the label minimum
		self.max = 1 # Define the label maximum
		self.scale = 0 # Define the requency of labels
		self.precision = 0 # Define number of decimal points for the scale
		self.drawValue = True # Draw the value of the gauge in the title bar
		self.valuePrecision = 0 # Define number of decimal points for th printed label
		self.unit = None # Unit of measurement

		self.redline = 0 # Defines a literal "redline" to show where the max value of a guage is - optional
		self.redlinepos = 0 # Calculatd later
		self.redlinesize = 0 # Calculated later

		self.win = None # Create a placeholder variable for the window to be created later
		# Gets buggy if I try and defin th window here and stops updating

	def drawScale(self): # Creates a series of labels along the bottom of the gauge for referencing the value
		numberOfMarks = int(self.max/self.scale) # Determine number of labels for the gauge
		for x in range(0, numberOfMarks):
			self.win.addstr(self.height+1, int((self.width/numberOfMarks)*x), my_precision(x*self.scale, self.precision)) # Draw the scale labels

		self.win.addstr(self.height+1, self.width-len(str(self.max))-1, str(self.max)) # Add the max value to the end of the gauge

	def drawRedline(self): # Creates the "redline" showing where the max value of a guage is
		global redline_char
		if (self.value > self.redline):
			if sin(time.time()*30) > 0:
				local_redline = redline_flash_char
			else:
				local_redline = redline_char
		else:
				local_redline = redline_char
		self.redlinepos = int((self.redline/self.max)*self.width) # Set the start of the redline
		self.redlinesize = self.width - self.redlinepos # Set the width of the redline
		for y in range(1, self.height+1):
			self.win.addstr(y, self.redlinepos, local_redline*(self.redlinesize-1), curses.color_pair(2)) # Draw the redline

		self.win.addstr(self.height+1, self.redlinepos, str(self.redline), curses.color_pair(4)) # Highlight the redline value

	def drawGauge(self):
		if self.redline > 0:
			fill = min(int(self.width*self.scl_value), self.redlinepos) # Set the width of the filled progress in characters
		else:
			fill = int(self.width*self.scl_value)

		if self.drawValue:
			if self.valuePrecision>=0:
				prec_str = my_precision(self.value, self.valuePrecision)
			else:
				prec_str = prec_str = int((self.value // 10**-self.valuePrecision) * 10**-self.valuePrecision)

			if self.unit:
				self.win.addstr(0, int((self.width - (len(self.title) + len(str(prec_str)) + len(self.unit) + 5))/2), # Calculate width of title
					" " + self.title + " [" + str(prec_str) + " " + self.unit + "] ", curses.A_STANDOUT) # Draw the gauge label + value + unit
			else:
				self.win.addstr(0, int((self.width - (len(self.title) + len(str(prec_str)) + 5))/2), # Calculate width of title
					" " + self.title + " [" + str(prec_str) + "] ", curses.A_STANDOUT) # Draw the gauge label + value + unit

		else:
			self.win.addstr(0, int((self.width - len(self.title) + 2)/2), # Calculate width of title
			" " + self.title + " ", curses.A_STANDOUT) # Draw the gauge label

		if fill != 0: # Don't draw the guage value if there are no characters
			for y in range(1, self.height+1):
				self.win.addstr(y, 1, gauge_char*(fill-1), curses.color_pair(1)) # Draw the gauge value

				if self.redline!=0: # Don't draw the redline needle if no redline is set
					if int(self.width*self.scl_value) > self.redlinepos:
						self.win.addstr(y, int(self.width*self.scl_value)-1, needle_char, curses.color_pair(3)) # Draw the redline needle

	def setVal(self, value):
		self.value = value # Gague value - expects a float value from 0 to 1
		self.scl_value = scaleValue(self.value, self.min, self.max)
		self.win = curses.newwin(self.height+2, self.width, self.y, self.x) # Create our curses window
		self.win.border(0)

		if not (self.max-self.min==0 or self.scale==0): # Don't draw the scale if it's not defined
			self.drawScale()

		if self.redline!=0: # Don't draw the redline if it's not defined
			self.drawRedline()

		self.drawGauge()

		self.win.refresh() # Update screen

rpm = Gauge("Tachometer", 1, 9, scrwidth-2, 3) # Tachometer
rpm.max = 9000
rpm.scale = 1000
rpm.redline = 7000
rpm.unit = "RPM"
rpm.valuePrecision = -2

thr_pos = Gauge("Throttle", 1, 15, int((scrwidth-1)/2), 2) # Throttle Position
thr_pos.max = 1
thr_pos.scale = .2
thr_pos.precision = 1
thr_pos.valuePrecision = 2

voltage = Gauge("Battery Voltage", int(scrwidth/2)+1, 15, int(scrwidth/2)-2, 2)
voltage.max = 18
voltage.scale = 3
voltage.unit = "V"
voltage.valuePrecision = 1

speed = DigGauge("Speed", 0, 1, 3)
speed.x = int((scrwidth-(speed.width+2))/2)

try:
	while True: # Arbitrary movemnt
		rpm.setVal(time.time()*.3%1*3000+5000)
		thr_pos.setVal(scaleValue(sin(time.time()*3), -1, 1))
		voltage.setVal(12)
		speed.setVal(scaleValue(sin(time.time()*.3), -1, 1, 100, 0))

finally:
	curses.endwin()
