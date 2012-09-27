#!/usr/bin/python
#encoding=utf-8
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import time
import threading
import httplib
import sys
import os
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import logging
import log

logger = logging.getLogger('traversal')

URL = "http://m.baidu.com"
BROWSERS = [{"id":"1", 
	"BrowserName":"ANDROID自带浏览器", 
	"packageName":"com.android.browser", 
	"activity":".BrowserActivity", 
	"apkName":"", 
	"version":""}]
WAIT = 8
PATH = "tmp/"
RESULT_HOST = ""

class Worker(threading.Thread):
	def __init__(self, serial_num, work_queue, superdevices):
		threading.Thread.__init__(self, name = serial_num)
		self.serial_num = serial_num
		self.work_queue = work_queue
		self.superdevices = superdevices

	def killPackage(self, package):

		
	def pageDown(self, superdevice):
		width = int(superdevice.getProperty('display.width'));
		height = int(superdevice.getProperty('display.height'));
		x1 = x2  = width / 2
		y2 = height / 8
		y1 = height * 7 / 8
		superdevice.drag((x1, y1), (x2, y2), 1.5, 10)

	def fullCapture(self, superdevice, task_id, browser_id, path):
		path = path + task_id + "/" + browser_id + "/"
		max, loop_num, time_temp = 7, 0, time.time()
		pics_cur = None

		while True:
			if loop_num >= max:
				break
			else:
				loop_num += 1
			if not pics_cur: pics_cur = superdevice.takeSnapshot()
			self.pageDown(superdevice)
			pics_nxt = superdevice.takeSnapshot()
			if not os.path.isdir(path): os.makedirs(path)
			pics_cur.writeToFile(path + str(time_temp) + '_' + str(loop_num) + '.gif')
			pics_cur = pics_nxt
			if pics_cur.sameAs(pics_nxt, 0.8):
				break
			MonkeyRunner.sleep(1)

	def pushResult(self, task_id, serial_num, path, host):
		return

	def execute(self, superdevice, task_id, serial_num, url, browsers = BROWSERS, wait = WAIT, path = PATH, result_host = RESULT_HOST):
		for browser in browsers:
			runComponent = browser["packageName"] + "/" + browser["activity"]
			logger.info("worker %s : url %s runComponent %s " % (serial_num, url, runComponent))
			logger.info(superdevice)
			superdevice.startActivity(data = url, action = 'android.intent.action.VIEW', component = runComponent)
			MonkeyRunner.sleep(wait)
			self.fullCapture(superdevice, task_id, browser["id"], path)
		self.pushResult(task_id, serial_num, path, result_host)

	def retryWork(self, task):
		self.work_queue.put(task)	

	def run(self):
		time.sleep(3)
		while True:
			time.sleep(1)
			task = self.work_queue.get()
			logger.info("worker %s: work start" % self.serial_num)
			task_id = task["id"]
			serial_num = task["serial_num"]

			superdevice = self.superdevices.get(self.serial_num)
			if not superdevice:
				logger.info("Worker %s : task_id %s retry" % (serial_num, task_id))
				self.retryWork(task)
				continue
			if not task_id or not serial_num:
				logger.info("worker %s: task none device serial number" % serial_num)
			else:
				if not task.get("url"): url = URL
				if not task.get("browsers"): browsers = BROWSERS
				if not task.get("wait"): wait = WAIT
				if not task.get("path"): path = PATH 
				if not task.get("result_host"): result_host = RESULT_HOST 
				try:
					self.execute(superdevice, task_id, serial_num, url, browsers, wait, path, result_host)	
				except Exception, ex:
					logger.error(ex)
					if superdevice.isConnect():
						logger.error("Worker %s: task_id %s abort" % (serial_num, task_id))
					else:
						logger.info("Worker %s : task_id %s retry" % (serial_num, task_id))
						superdevice.connect()
						self.retryWork(task)
						continue

def main():
	from Queue import Queue
	from deviceworker import DeviceWorker
	
	devices = {} 
	workers = {}
	worker_queues = {}
	device_worker_queue = Queue()

	device_worker = DeviceWorker("device_worker", device_worker_queue, devices)
	device_worker.start()
	
	task1 = {"id":"1", "serial_num":"343267035F1C00EC"}
	task2 = {"id":"2", "serial_num":"343267035F1C00EC"}
	task3 = {"id":"3", "serial_num":"343267035F1C00EC"}
	task4 = {"id":"4", "serial_num":"02466b93"}
	task5 = {"id":"5", "serial_num":"02466b93"}
	task6 = {"id":"6", "serial_num":"02466b93"}
	task7 = {"id":"7", "serial_num":"BX90317BR6"}
	task8 = {"id":"8", "serial_num":"BX90317BR6"}
	task9 = {"id":"9", "serial_num":"BX90317BR6"}
	task10 = {"id":"10", "serial_num":"01469C1B1201D015"}
	task11 = {"id":"11", "serial_num":"01469C1B1201D015"}
	task12 = {"id":"12", "serial_num":"01469C1B1201D015"}
	task13 = {"id":"13", "serial_num":"i5590431fbd79"}
	task14 = {"id":"14", "serial_num":"i5590431fbd79"}
	task15 = {"id":"15", "serial_num":"i5590431fbd79"}

	def execute(task):
		serial_num = task["serial_num"]
		if not devices.get(serial_num):
			device_worker_queue.put(serial_num)
		if not worker_queues.get(serial_num):
			logger.info("worker %s : create queue" % serial_num)
			worker_queues[serial_num] = Queue()
		if not workers.get(serial_num):
			logger.info("worker %s : create worker" % serial_num)
			workers[serial_num] = Worker(serial_num, worker_queues[serial_num], devices)
			workers[serial_num].start()
		worker_queues[serial_num].put(task)

	execute(task1)
	execute(task2)
	execute(task3)
	execute(task4)
	execute(task5)
	execute(task6)
	execute(task7)
	execute(task8)
	execute(task9)		
	execute(task10)
	execute(task11)
	execute(task12)	
	execute(task13)
	execute(task14)
	execute(task15)

	logger.info(worker_queues)

	while True:
		time.sleep(1)

if __name__ == '__main__':
	main()
