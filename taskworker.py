#!/usr/bin/python
#encoding=utf-8
import time
import threading
import logging
from Queue import Queue
from worker import Worker
import log

logger = logging.getLogger('traversal')

class TaskWorker(threading.Thread):
	def __init__(self, threadname, task_queue, workers, worker_queues, devices, device_worker_queue):
		threading.Thread.__init__(self, name = threadname)
		self.task_queue = task_queue
		self.workers = workers
		self.worker_queues = worker_queues
		self.devices = devices
		self.device_worker_queue = device_worker_queue

	def run(self):
		while True:
			try:
				task = self.task_queue.get()
				logger.info("TaskWorker: %s" % task)
				serial_num = task["serial_num"]
				if not self.devices.get(serial_num):
					self.device_worker_queue.put(serial_num)
				if not self.worker_queues.get(serial_num):
					logger.info("worker %s : create queue" % serial_num)
					self.worker_queues[serial_num] = Queue()
				if not self.workers.get(serial_num):
					logger.info("worker %s : create worker" % serial_num)
					self.workers[serial_num] = Worker(serial_num, self.worker_queues[serial_num], self.devices)
					self.workers[serial_num].start()
				self.worker_queues[serial_num].put(task)
			except Exception, ex:
				logger.error(ex)
				time.sleep(1)
			else:
				logger.debug("TaskWorker(system info): %s %s %s %s" % (self.task_queue, self.workers, self.devices, self.device_worker_queue))

