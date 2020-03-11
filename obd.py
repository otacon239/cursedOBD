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
curses.init_pair(1, curses.COLOR_WHITE, -1) # curses color pair 1: White on black, standard text
curses.init_pair(2, curses.COLOR_RED, -1) # curses color pair 2: Red on black, redlines

class ProgBar:
	def __init__(self, title, x, y, width, height, range=0, scale=0, redline=0):
		self.title = title # Title
		self.x = x # X position
		self.y = y # Y position
		self.width = width # Full width of the progress bar window
		self.height = height # Full height of the progress bar window
		self.range = range # Define the label maximum - optional
		self.scale = scale # Define the requency of labels - optional
		self.redline = redline # Defines a literal "redline" to show where the max value of a guage is - optional

		self.redlinepos = int((self.redline/self.range)*self.width) # Set the start of the redline
		self.redlinesize = self.width - self.redlinepos # Set the width of the redline

		self.win = 0 # Creating a placeholder variable for the window to be created later

	def drawScale(self): # Creates a series of labels along the bottom of the window for referencing the value
		numberOfMarks = int(self.range/self.scale) # Determine number of labels for the guage
		for x in range(0, numberOfMarks):
			self.win.addstr(2, int((self.width/numberOfMarks)*x), '%.0f' % (x*self.scale)) # Need to find a way to define precision

		self.win.addstr(2, self.width-len(str(self.range))-1, str(self.range), curses.A_BOLD) # Add the max value to the end of the bar

	def drawRedline(self): # Creates the "redline" showing where the max value of a guage is
		self.win.addstr(1, self.redlinepos, "█"*(self.redlinesize-1), curses.color_pair(2)) # Draw the redline

	def drawProgBar(self):
		fill = min(int(self.width*self.prog), self.redlinepos) # Set the width of the filled progress in characters
		self.win.addstr(0, int((self.width - len(self.title) + 2)/2), " " + self.title + " ", curses.A_STANDOUT) # Draw the progrss bar label
		if fill != 0: # Don't draw the progress bar if there are no characters
			self.win.addstr(1, 1, "█"*(fill-1), curses.color_pair(1)) # Draw the progress bar
			if int(self.width*self.prog) > self.redlinesize:
				self.win.addstr(1, int(self.width*self.prog)-1, "█")

	def setProg(self, prog):
		self.prog = prog # Progress bar percentage - expects a float value from 0 to 1

		self.win = curses.newwin(self.height, self.width, self.y, self.x) # Create our curses window
		self.win.border(0) # Enable the border

		if self.redline!=0: # Don't draw the redline if it's not defined
			self.drawRedline()

		if self.range!=0 and self.scale!=0: # Don't draw the scale if it's not defined
			self.drawScale()

		self.drawProgBar()

		self.win.refresh() # Update screen

bar = ProgBar("RPM", 1, int(scrheight/2-1), scrwidth-1, 3, 9000, 1000, 7000) # Sample guage creation

while True:
	bar.setProg((sin(time.time())+1)*.5) # Create constant movement

curses.endwin() # Need to find a way to gracefully exit
