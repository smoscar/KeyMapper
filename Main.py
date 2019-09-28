from evdev import *
from select import select
from Config import *
import subprocess as sp

class KeyMapper:
	"""docstring for KeyMapper"""
	def __init__(self):
		self.currentOption = 0
		self.currentSelection = -1
		self.mapper = []

		# Keyboard mapping
		self.keymap = [
		103,	# Up
		105,	# Left
		106,	# Right
		108,	# Down
		1,		# Escape (Sleep)
		28,		# Return (Mode)
		44,		# Key Z (A)
		45,		# Key X (B)
		]
		# Menu options
		self.menu = [
		"Map button to keyboard event",
		"Map axis to keyboard events",
		"Map axis to multiple key events",
		"Map sequence to single key press",
		"Quit"
		]
		self.renderMenu()
		self.captureKeyEvents()

	def captureKeyEvents(self):
		# Check for connected devices
		i = 0
		devices = [InputDevice(path) for path in list_devices()]
		devices = {dev.fd: dev for dev in devices}
		# Initialize the menu
		while True:
			r, w, x = select(devices, [], [])
			for fd in r:
				for event in devices[fd].read():
					if self.currentSelection == -1 and event.code in self.keymap and event.value == 1:
						self.udpateMenu(event.code)
					elif self.currentSelection > -1 and event.code not in self.keymap:
						self.storeKeyEvent(event)
	
	def storeKeyEvent(self, event):
		# Single button to key mapping
		if self.currentSelection == 0 and event.value == 1:
			self.mapper.append(event.code)
			
		self.renderMenu()

	def udpateMenu(self, eventCode):
		# KEY UP
		if eventCode == 103:
			self.currentOption = (self.currentOption - 1) if ((self.currentOption - 1) >= 0) else (len(self.menu)-1)
		# KEY DOWN
		if eventCode == 108:
			self.currentOption = (self.currentOption + 1) if ((self.currentOption + 1) < len(self.menu)) else 0
		# Select option 
		if eventCode == 28 or eventCode == 45:
			 self.currentSelection = self.currentOption
		self.renderMenu()
		
	def save(self):
		global Config
		print "\n Saving..."
		conf = Config()
		conf.addMapping(self.mapper)
		self.currentSelection = -1
		self.mapper = []
	
	def renderMenu(self):
		tmp = sp.call('clear', shell=True)
		# Main menu
		if self.currentSelection == -1:
			print "Select option with arrow keys"
			print "-------------------------------"
			for m in range(len(self.menu)):
				print "{}{}. {}".format(("> " if self.currentOption == m else "  "), (m+1), self.menu[m])
		# Button to key press
		if self.currentSelection == 0:
			print ("Press a button on the controller" if len(self.mapper) < 1 else "...now press a key")
			print "-------------------------------"
			print "\n".join(map(str, self.mapper))
			if len(self.mapper) == 2:
				self.save()
				self.renderMenu()

if __name__ == "__main__":
	km = KeyMapper()
