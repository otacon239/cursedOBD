"""
TODO:
X Build a basic progress bar function
	X Include labeling support
	X Setup "redline" value
	- Setup "precision" value
- Get basic OBD inputs
- Get multiple OBD inputs
X Create min/max system
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
curses.init_pair(1, curses.COLOR_WHITE, -1) #curses color pair 1: White on black, standard text
curses.init_pair(2, curses.COLOR_RED, -1) #curses color pair 2: Red on black, redlines

class ProgBar:
	def __init__(self, title, x, y, width, height, range=0, scale=0, redline=0):
		self.title = title # Title
		self.x = x # X position
		self.y = y # Y position
		self.width = width # Full width of the progress bar window
		self.height = height # Full height of the progress bar window
		self.range = range # define the label maximum
		self.scale = scale # define the requency of labels
		self.redline = redline # defines a literal "redline" to show where the max value of a guage is

		#self.win = curses.newwin(self.height, self.width, self.y, self.x) # Create a window for the progrss bar
		self.win = 0 # Creating a placeholder variable for the window to be created later

	def drawScale(self):
		numberOfMarks = int(self.range/self.scale) # Determine number of labels for the guage
		for x in range(0, numberOfMarks):
			self.win.addstr(2, int((self.width/numberOfMarks)*x), '%.0f' % (x*self.scale)) # Need to find a way to define precision

	def drawRedline(self):
		redlinepos = int((self.redline/self.range)*self.width) # Set the start of the redline
		redlinesize = self.width - redlinepos # Set the width of the redline
		self.win.addstr(1, redlinepos, "█"*(redlinesize-1), curses.color_pair(2)) # Draw the redline

	def setProg(self, prog):
		self.prog = prog #Progress bar percentage

		self.win = curses.newwin(self.height, self.width, self.y, self.x) # Create our curses window
		self.win.border(0) # Enable to border
		fill = int(self.width*self.prog) # Set the width of the filled progress in characters
		self.win.addstr(0, int((self.width - len(self.title))/2), " " + self.title + " ", curses.A_STANDOUT) # Draw the progrss bar label

		if self.redline!=0: # Don't draw the redline if it's not defined
			self.drawRedline()

		if fill != 0: # Don't draw the progress bar if there are no characters
			self.win.addstr(1, 1, "█"*(fill-1), curses.color_pair(1)) # Draw the progress bar

		if self.range!=0 and self.scale!=0: # Don't draw the scale if it's not defined
			self.drawScale()

		self.win.refresh() # Update screen

bar = ProgBar("Beep Boop", 1, int(scrheight/2-1), scrwidth-1, 3, 9000, 1000, 7000)

while True:
	bar.setProg((sin(time.time())+1)*.5)

curses.endwin()
