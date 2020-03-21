# -*- coding: utf-8 -*-

"""
 ███    ██   ████  ████    ███ █████  ███  █████  ███   ███       
█   █  █ █       █     █  █  █ █     █        █  █   █ █   █      
█   █    █    ███   ███  █████ ████  ████    █    ███   ████      
█   █    █   █         █     █     █ █   █   █   █   █     █      
 ███   █████ █████ ████      █ ████   ███    █    ███   ███    █  
"""
import curses

big_font = {}

big_font['0'] = [" ███ ","█   █","█   █","█   █"," ███ "]
big_font['1'] = [" ██  ","█ █  ","  █  ","  █  ","█████"]
big_font['2'] = ["████ ","    █"," ███ ","█    ","█████"]
big_font['3'] = ["████ ","    █"," ███ ","    █","████ "]
big_font['4'] = ["  ███"," █  █","█████","    █","    █"]
big_font['5'] = ["█████","█    ","████ ","    █","████ "]
big_font['6'] = [" ███ ","█    ","████ ","█   █"," ███ "]
big_font['7'] = ["█████","   █ ","  █  ","  █  ","  █  "]
big_font['8'] = [" ███ ","█   █"," ███ ","█   █"," ███ "]
big_font['9'] = [" ███ ","█   █"," ████","    █"," ███ "]
big_font['.'] = ["     ","     ","     ","     ","  █  "]

char_width = 5 # Width of the font
char_height = 5 # Height of the font

def my_precision(x, n): # https://stackoverflow.com/a/30897520
    return '{:.{}f}'.format(x, n)

class DigGauge:
  def __init__(self, title, x, y, dig_width):
    self.title = title # Title
    self.x = x # X position
    self.y = y # Y position
    self.dig_width = dig_width # Width of the dgital gauge in characters
    self.width = dig_width * char_width + 1

    # Optional values
    self.valuePrecision = 0

    self.win = None # Create a placeholder variable for the window to be created later

  def setVal(self, value):
    self.value = value
    self.value = my_precision(self.value, self.valuePrecision)
    self.value = self.value.zfill(self.dig_width)

    self.win = curses.newwin(char_height+2, self.width+self.dig_width, self.y, self.x)
    self.win.border(0)

    self.win.addstr(0, int((self.width - len(self.title) + 2)/2), # Calculate width of title
			" " + self.title + " ", curses.A_STANDOUT) # Draw the gauge label

    for x in range(0, min(len(self.value), self.dig_width)):
      for i in range(0, len(big_font[self.value[x]])):
        self.win.addstr(i+1, x*6+1, big_font[self.value[x]][i])

    self.win.refresh()