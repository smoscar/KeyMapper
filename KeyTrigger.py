import hashlib
from evdev import *
from select import select
from Config import *

class KeyTrigger:
	"""docstring for KeyTrigger"""
	def __init__(self):
		conf = Config('/home/pi/KeyMap/config.cfg')
		self.events = conf.getContents()
		print self.events
		self.captureKeyEvents()

	def captureKeyEvents(self):
		# Check for connected devices to which an entry has been stored
		devices = [InputDevice(path) for path in list_devices()]
		devices = list(filter(lambda x: hashlib.sha1(x.name).hexdigest() in self.events, devices))
		devices = {dev.fd: dev for dev in devices}
		# Initialize the menu
		while True:
			r, w, x = select(devices, [], [])
			for fd in r:
				for event in devices[fd].read():
					deviceHash = hashlib.sha1(devices[fd].name).hexdigest()
					#Button presses
					if event.type == ecodes.EV_KEY and str(event.code) in self.events[deviceHash]['buttonToKey']:
						buttonCode = ecodes.bytype[1][self.events[deviceHash]['buttonToKey'][str(event.code)]]
						with uinput.UInput() as ui:
							ui.write(ecodes.EV_KEY, getattr(ecodes, buttonCode), 1)
							ui.syn()
					# elif event.type == ecodes.EV_ABS:
