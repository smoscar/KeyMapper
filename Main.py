from evdev import *
from select import select
import subprocess as sp

class KeyMapper:
	"""docstring for KeyMapper"""
	def __init__(self):
		self.currentOption = 0
		self.currentSelection = False

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
		"Map input to key press",
		"Map axis to multiple key events",
		"Map sequence to key press",
		"Quit"
		]
		self.renderMenu()
		self.lookForDevices()

	def lookForDevices(self):
		# Check for connected devices
		i = 0
		devices = [InputDevice(path) for path in list_devices()]
		devices = {dev.fd: dev for dev in devices}
		# Initialize the menu
		while True:
			r, w, x = select(devices, [], [])
			for fd in r:
				for event in devices[fd].read():
					if self.currentSelection == False and event.code in self.keymap and event.value == 1:
						self.udpateMenu(event.code)

	def udpateMenu(self, eventCode):
		# KEY UP
		if eventCode == 103:
			self.currentOption = (self.currentOption - 1) if ((self.currentOption - 1) >= 0) else (len(self.menu)-1)
		# KEY DOWN
		if eventCode == 108:
			self.currentOption = (self.currentOption + 1) if ((self.currentOption + 1) < len(self.menu)) else 0
		self.renderMenu()
	
	def renderMenu(self):
		tmp = sp.call('clear', shell=True)
		print "Select your desired option"
		print "---------------------------"
		for m in range(len(self.menu)):
			print "{}{}. {}".format(("> " if self.currentOption == m else "  "), (m+1), self.menu[m])

def main():
	km = KeyMapper()

if __name__ == "__main__":
	main()
