#!/usr/bin/python
#encoding=utf-8
from Queue import Queue
import logging
import time
import log
from deviceworker import DeviceWorker
from worker import Worker
from pushworker import PushWorker
from pushworker import task_queue
from taskworker import TaskWorker

logger = logging.getLogger('traversal')

device_worker_queue = Queue()
workers = {}
worker_queues = {}
devices = {} 

def main():
	device_worker = DeviceWorker("DeviceWorker", device_worker_queue, devices)
	device_worker.start()
	
	logger.info("deviceworker start....")

	push_worker = PushWorker('PushWorker')
	push_worker.start()

	logger.info("traversal services start....")

	task_worker = TaskWorker("TaskWorker", task_queue, workers, worker_queues, devices, device_worker_queue)
	task_worker.start()

	logger.info("taskworker start....")

	while True:
		time.sleep(1)

if __name__ == '__main__':
	main()