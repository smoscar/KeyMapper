from evdev import *
from select import select
from Config import *
import subprocess as sp
import hashlib

class KeyMapper:
	"""docstring for KeyMapper"""
	def __init__(self):
		self.currentOption = 0
		self.currentSelection = -1
		self.mapper = []
		self.allowEnter = False
		self.lastEventHash = ''

		# Keyboard mapping
		self.keymap = [
		103,	# Up
		105,	# Left
		106,	# Right
		108,	# Down
		308,	# Up Gamepad
		310,	# Left Gamepad
		311,	# Right Gamepad
		309,	# Down Gamepad
		1,		# Escape (Sleep)
		28,		# Return (Mode)
		44,		# Key Z (A)
		45,		# Key X (B)
		306,		# Key A (Gamepad)
		]
		# Menu options
		self.menu = [
		"Map button to keyboard event",
		"Map analog stick/button to keyboard events",
		"Map analog stick/button to 2 key events",
		"Map sequence to single key press",
		"Quit"
		]
		self.renderMenu()
		self.captureKeyEvents()
		
	def updateDeviceHash(self, name):
		if self.lastEventHash == '':
			self.lastEventHash = hashlib.sha1(name.encode('utf-8')).hexdigest()

	def captureKeyEvents(self):
		# Check for connected devices
		devices = [InputDevice(path) for path in list_devices()]
		devices = {dev.fd: dev for dev in devices}
		# Initialize the menu
		while True:
			r, w, x = select(devices, [], [])
			for fd in r:
				for event in devices[fd].read():
					print(devices)
					# Main Menu selection
					if self.currentSelection == -1 and event.code in self.keymap and event.value == 1:
						self.udpateMenu(event.code)
					# Mapping events
					elif self.currentSelection > -1 and (event.code not in self.keymap or self.allowEnter == True):
						self.updateDeviceHash(devices[fd].name)
						self.storeKeyEvent(event)
	
	def storeKeyEvent(self, event):
		# Map button to keyboard event
		if self.currentSelection == 0 and event.value == 1:
			self.mapper.append(event.code)
			self.renderMenu()
		
		# Map analog stick/button to keyboard events
		if self.currentSelection == 1:
			# Accepting the axe event input
			if len(self.mapper) == 1 and (event.code == 28 or event.code == 306)  and event.value == 1:
				self.mapper.append(0)
				self.renderMenu()
				return
			elif len(self.mapper) == 2 and event.value == 1:
				self.mapper[1] = event.code
				self.renderMenu()
				return
			# No other buttons accepted starting from here
			if event.type != ecodes.EV_ABS:
				return
			delta = False
			absevent = categorize(event)
			axe_name = ecodes.bytype[absevent.event.type][absevent.event.code]
			# Initialize the entry
			if len(self.mapper) == 0:
				self.mapper.append({})
				self.mapper[0][axe_name] = [float("inf"),-float("inf")]
			# Discard other axis events
			if list(self.mapper[0].keys())[0] != axe_name:
				return

			if absevent.event.value < self.mapper[0][axe_name][0]:
				delta = True
				self.mapper[0][axe_name][0] = absevent.event.value
			if absevent.event.value > self.mapper[0][axe_name][1]:
				delta = True
				self.mapper[0][axe_name][1] = absevent.event.value

			if delta:
				self.allowEnter = True
				self.renderMenu()

	def udpateMenu(self, eventCode):
		# KEY UP
		if eventCode == 103 or eventCode == 308:
			self.currentOption = (self.currentOption - 1) if ((self.currentOption - 1) >= 0) else (len(self.menu)-1)
		# KEY DOWN
		if eventCode == 108 or eventCode == 309:
			self.currentOption = (self.currentOption + 1) if ((self.currentOption + 1) < len(self.menu)) else 0
		# Select option 
		if eventCode == 28 or eventCode == 45 or eventCode == 306:
			 self.currentSelection = self.currentOption
		self.renderMenu()
		
	def save(self, type='buttonToKey'):
		global Config
		print("\n Saving...")
		conf = Config()
		conf.addMapping(self.mapper, self.lastEventHash, type)
		self.lastEventHash = ''
		self.currentSelection = -1
		self.mapper = []
	
	def renderMenu(self):
		tmp = sp.call('clear', shell=True)
		# Main menu
		if self.currentSelection == -1:
			print("Select option with arrow keys")
			print("-------------------------------")
			for m in range(len(self.menu)):
				print("{}{}. {}".format(("> " if self.currentOption == m else "  "), (m+1), self.menu[m]))
		# Button to key press
		if self.currentSelection == 0:
			print("Press a button on the controller" if len(self.mapper) < 1 else "...now press a key")
			print("-------------------------------")
			print("\n".join(map(str, self.mapper)))
			if len(self.mapper) == 2:
				self.save()
				self.renderMenu()
		# Axis to key press
		if self.currentSelection == 1:
			consequentMsg = "...when ready press enter" if len(self.mapper) == 1 else "...now press a key"
			print("Slowly move the stick/button all the way" if len(self.mapper) < 1 else consequentMsg)
			print("-------------------------------")
			if len(self.mapper) > 0:
				currentAxe = list(self.mapper[0].keys())[0]
				print("{} -> min: {}, max {}".format(currentAxe, self.mapper[0][currentAxe][0], self.mapper[0][currentAxe][1]))
			if len(self.mapper) == 2 and self.mapper[1] != 0:
				print("\n".join(map(str, self.mapper)))
				self.save('analogToKey')
				self.renderMenu()
