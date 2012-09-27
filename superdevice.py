#!/usr/bin/python
#encoding=utf-8
class SuperDevice():
	
	def __init__(self, serial_num, device, device_worker_queue):
		self.serial_num = serial_num
		self.device = device
		self.device_worker_queue = device_worker_queue

	def getProperty(self, property):
		return self.device.getProperty(property)

	def takeSnapshot(self):
		return self.device.takeSnapshot()

	def drag(self, start, end, duration, steps):
		self.device.drag(start, end, duration, steps)

	def startActivity(self, data, action, component):
		self.device.startActivity(data = data, action = action, component = component)

	def isConnect(self):
		try:
			if self.device.getProperty('display.width'):
				return True
			else:
				return False
		except:
			return False	

	def connect(self):
		self.device_worker_queue.put(self.serial_num)