#!/usr/bin/python
#encoding=utf-8
import threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import json
from Queue import Queue
import logging
import log

logger = logging.getLogger('traversal')

PORT_NUMBER = 8889

task_queue = Queue()

class PushHandler(BaseHTTPRequestHandler):	

	def addTask(self, path):
		query = urlparse.parse_qs(path.query)

		# add a task to task_queue
		if query["task"]:
			task = json.read(str(query["task"][0]))
			logger.info(task)
			task_queue.put(task)

		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write("succeed")
		return

	def route(self):
		try:
			path = urlparse.urlparse(self.path)

			logger.debug('path: %s' % path.path)
			if path.path == "/addTask":
				self.addTask(path)
		except Exception, ex:
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write("fail")
			logger.error(ex)

	#Handler for the GET requests
	def do_POST(self):
		self.route()
		return

	#Handler for the POST requests
	def do_GET(self):
		self.route()
		return		
	
class PushWorker(threading.Thread):

	def __init__(self, threadname):
		threading.Thread.__init__(self, name = threadname)

	def run(self):
		try:
			server = HTTPServer(('', PORT_NUMBER), PushHandler)
			server.serve_forever()
		except KeyboardInterrupt:
			logger.info('^C received, shutting down the web server')
			server.socket.close()

def main():

	pushWorker = PushWorker('PushWorker')
	pushWorker.start()
	pushWorker.join()

if __name__ == '__main__':
	main()

