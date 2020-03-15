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

stdscr = curses.initscr() # Start curses
curses.start_color() # Enable color
curses.curs_set(False) # Disable cursor
scrheight, scrwidth = stdscr.getmaxyx() # Grab screen size

curses.use_default_colors() # This is required to allow inheritence of the background color for the current terminal
curses.init_pair(1, curses.COLOR_WHITE, -1) # Standard text: White on default
curses.init_pair(2, curses.COLOR_RED, -1) # Redline: Red on default
curses.init_pair(3, curses.COLOR_BLACK, -1) # Redline needle: Cyan on default - Only shown past redline for emphasis
curses.init_pair(4, -1, curses.COLOR_RED) # Redline label: White on red

def my_precision(x, n): # https://stackoverflow.com/a/30897520
    return '{:.{}f}'.format(x, n)

def scaleValue(OldValue, OldMin, OldMax, NewMin=0, NewMax=1, clamp=True): # https://stackoverflow.com/a/929107
	if clamp:
		if OldValue < OldMin:
			OldValue = OldMin
		if OldValue > OldMax:
			OldValue = OldMax

	OldRange = (OldMax - OldMin)
	if (OldRange == 0):
		NewValue = NewMin
	else:
		NewRange = (NewMax - NewMin)
		NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	return NewValue

class Gauge:
	def __init__(self, title, x, y, width, height):
		self.title = title # Title
		self.x = x # X position
		self.y = y # Y position
		self.width = width # Full width of the gauge window
		self.height = height # Full height of the gauge window

		self.range = 0 # Define the label maximum - optional
		self.scale = 0 # Define the requency of labels - optional
		self.precision = 0 # Define number of decimal points for the scale

		self.redline = 0 # Defines a literal "redline" to show where the max value of a guage is - optional
		self.redlinepos = 0 # Calculatd later
		self.redlinesize = 0 # Calculated later

		self.win = None # Creating a placeholder variable for the window to be created later; gets buggy if I try and defin th window here and stop updating

	def drawScale(self): # Creates a series of labels along the bottom of the gauge for referencing the value
		numberOfMarks = int(self.range/self.scale) # Determine number of labels for the gauge
		for x in range(0, numberOfMarks):
			self.win.addstr(self.height+1, int((self.width/numberOfMarks)*x), my_precision(x*self.scale, self.precision)) # Draw the scale labels

		self.win.addstr(self.height+1, self.width-len(str(self.range))-1, str(self.range)) # Add the max value to the end of the gauge

	def initRedline(self, redline):
		self.redline = redline
		if self.redline!=0:
			self.redlinepos = int((self.redline/self.range)*self.width) # Set the start of the redline
			self.redlinesize = self.width - self.redlinepos # Set the width of the redline

	def drawRedline(self): # Creates the "redline" showing where the max value of a guage is
		for y in range(1, self.height+1):
			self.win.addstr(y+self.y, self.redlinepos, "█"*(self.redlinesize-1), curses.color_pair(2)) # Draw the redline

		self.win.addstr(self.height+1, self.redlinepos, str(self.redline), curses.color_pair(4))# Highlight the redline value

	def drawProgBar(self):
		if self.redline > 0:
			fill = min(int(self.width*self.prog), self.redlinepos) # Set the width of the filled progress in characters
		else:
			fill = int(self.width*self.prog)

		self.win.addstr(0, int((self.width - len(self.title) + 2)/2), " " + self.title + " ", curses.A_STANDOUT) # Draw the gauge label
		if fill != 0: # Don't draw the guage value if there are no characters
			for y in range(1, self.height+1):
				self.win.addstr(y, 1, "█"*(fill-1), curses.color_pair(1)) # Draw the gauge value
				if self.redline!=0:
					if int(self.width*self.prog) > self.redlinepos:
						self.win.addstr(y, int(self.width*self.prog)-1, "█", curses.color_pair(3))

	def setProg(self, prog):
		self.prog = prog # Gague value - expects a float value from 0 to 1
		self.win = curses.newwin(self.height+2, self.width, self.y, self.x) # Create our curses window

		self.win.border(0) # Enable the border

		if not (self.range==0 or self.scale==0): # Don't draw the scale if it's not defined
			self.drawScale()

		if self.redline!=0: # Don't draw the redline if it's not defined
			self.drawRedline()

		self.drawProgBar()

		self.win.refresh() # Update screen

rpm = Gauge("RPM", 0, 0, scrwidth, 3) # Tachometer
rpm.range = 9000
rpm.scale = 1000
rpm.initRedline(7000)

thr_pos = Gauge("Throttle", 0, 6, int(scrwidth/2), 2) # Throttle Position
thr_pos.range = 1
thr_pos.scale = .1
thr_pos.precision = 1

while True: # Arbitrary movemnt
	rpm.setProg(scaleValue(time.time()*.3%1*2500+5000, 0, 9000))
	thr_pos.setProg(scaleValue(sin(time.time()*.3), -1, 1))

curses.endwin() # Need to find a way to gracefully exit
