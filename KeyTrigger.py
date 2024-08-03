import hashlib
from evdev import *
from select import select
from Config import *

class KeyTrigger:
	"""docstring for KeyTrigger"""
	def __init__(self):
		conf = Config('/home/pi/KeyMapper/config.cfg')
		self.events = conf.getContents()
		self.pressedEvents = set()
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
					deviceMap = self.events[deviceHash]
					#Button events
					if event.type == ecodes.EV_KEY and 'buttonToKey' in deviceMap and str(event.code) in deviceMap['buttonToKey']:
						buttonCode = ecodes.bytype[1][deviceMap['buttonToKey'][str(event.code)]]
						with uinput.UInput() as ui:
							ui.write(ecodes.EV_KEY, getattr(ecodes, buttonCode), event.value)
							ui.syn()
					elif event.type == ecodes.EV_ABS and 'analogToKey' in deviceMap:
						absevent = categorize(event)
						axe_name = ecodes.bytype[absevent.event.type][absevent.event.code]
						if axe_name in deviceMap['analogToKey']:
							axeEvent = deviceMap['analogToKey'][axe_name]
							minValue = axeEvent['axeValues'][0]
							maxValue = axeEvent['axeValues'][1]
							triggerValue = ((maxValue - minValue) // 2) + minValue
							buttonCode = ecodes.bytype[1][axeEvent['mappedKey']]
							if absevent.event.value >= triggerValue and axe_name not in self.pressedEvents:
								self.pressedEvents.add(axe_name)
								with uinput.UInput() as ui:
									ui.write(ecodes.EV_KEY, getattr(ecodes, buttonCode), 1)
									ui.syn()
							elif absevent.event.value < triggerValue and axe_name in self.pressedEvents:
								self.pressedEvents.remove(axe_name)
								with uinput.UInput() as ui:
									ui.write(ecodes.EV_KEY, getattr(ecodes, buttonCode), 0)
									ui.syn()
