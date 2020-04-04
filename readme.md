# cursedOBD - A Python/curses-based car dashboard

**cursedOBD** is a dashboard inspired by the [r/FUI](https://reddit.com/r/FUI) subreddit. I wanted to capture 80s-style retro terminals and 90s hacker movies.

![](preview.gif)

## **It has been tested to work on**
* Python 3 (latest)
* Debian-Based Linux Distros, MacOS (only graphics tested)
* ELM327-Based USB OBD Adapter ([mine](https://www.amazon.com/gp/B07Y5B5WLV))

## **It should work on**
* Python 3.X
* Any terminal that can run curses and Python
* Any valid ELM327 OBD tty session

## **Features**
* Display real-time output from the OBD adapter (In my testing, limited to ~1 update/sec) including, but not limited to:
  * Speed (mph/kph)
  * RPM
  * Battery Voltage
  * Engine Temperature
  * Throttle Postition
* UI Features:
  * Custom title/unit support
  * Fully customizable window position based on the curses library
  * BIG value output
  * Custom scale support
  * Customizable fonts
  * Customizable progress bar characters

## **What I plan on doing next (in no particular order)**
* Vertical progress bar support
* Easier color customization
* Proper config file support
* Fancier progress bars (needle/fantasy dials?)
* OBD prompts and interesting loading screens
