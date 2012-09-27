#!/usr/bin/python
#encoding=utf-8
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import time
import threading

import logging
import log
from superdevice import SuperDevice

logger = logging.getLogger('traversal')

TIMEOUT_NUM = 5

# device manager
class DeviceWorker(threading.Thread):

	def __init__(self, threadname, device_worker_queue, superdevices, timeout_num = TIMEOUT_NUM):
		threading.Thread.__init__(self, name = threadname)
		self.device_worker_queue = device_worker_queue
		self.superdevices = superdevices
		self.timeout_num = timeout_num

	def connection(self, serial_num):
		if self.superdevices.get(serial_num): 
			superdevice = self.superdevices.get(serial_num)
			if superdevice.isConnect():
				logger.info("DeviceWorker: %s is connectd" % (serial_num))
				return
			else:
				superdevice = self.superdevices.pop(serial_num)
				del superdevice
		try:
			device = MonkeyRunner.waitForConnection(self.timeout_num, serial_num)
			superdevice = SuperDevice(serial_num, device, self.device_worker_queue)
			if not superdevice.isConnect():
				logger.info("DeviceWorker: %s is not connectd" % (serial_num))
				superdevice.connect()
			else:
				time.sleep(3)
				self.superdevices[serial_num] = superdevice
				logger.info("DeviceWorker: %s create connection succeed" % (serial_num))
		except Exception, e:
			self.device_worker_queue.put(serial_num)
			logger.error("DeviceWorker: %s create connection fail %s" % (serial_num, e))
	
	def run(self):
		while True:
			serial_num = self.device_worker_queue.get()
			logger.info("DeviceWorker:  %s create connection start" % serial_num)
			self.connection(serial_num)
			time.sleep(2)

def main():
	from Queue import Queue
	import log
	import logging

	logger = logging.getLogger('traversal')
	
	devices = {}
	device_worker_queue = Queue()

	device_worker_queue.put("343267035F1C00EC")
	device_worker_queue.put("02466b93")

	device_worker = DeviceWorker("device_worker", device_worker_queue, devices)
	device_worker.start()
	device_worker.join()

if __name__ == '__main__':
	main()