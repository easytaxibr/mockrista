from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
from urlparse import urlparse
import json
import threading
import argparse
import re
import cgi
import random
import sys
import math
 
class HTTPRequestHandler(BaseHTTPRequestHandler):
	def randomTaxiPositionJson(self, lat, lng):
		taxis = []

		radius = 1000
		radiusInDegrees=float(radius)/float(111300)
		r = radiusInDegrees
		x0 = float(lat)
		y0 = float(lng)

		for i in range(1,100):
			u = float(random.random())
			v = float(random.random())
			
			w = r * math.sqrt(u)
			t = 2 * math.pi * v
			x = w * math.cos(t) 
			y = w * math.sin(t)
		  	
			print "x %f y %f" % (x, y)

			xLat  = x + x0
			yLong = y + y0

			taxis.append({"lat": xLat , "lng": yLong})
		return taxis
	def do_GET(self):
		try:
			if None != re.search('/api/gettaxis/*', self.path):
				query = urlparse(self.path).query
				query_components = dict(qc.split("=") for qc in query.split("&"))
				lat = query_components["lat"]
				lng = query_components["lng"]

				response = {"taxis": self.randomTaxiPositionJson(lat, lng)}

				self.send_response(200)
				self.send_header('Content-Type', 'application/json')
				self.end_headers()
				self.wfile.write(json.dumps(response))

			else:
				 self.send_response(403)
				 self.send_header('Content-Type', 'application/json')
				 self.end_headers()
		except ValueError:
			print ValueError
			self.send_response(400)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
		return
 
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	allow_reuse_address = True
 
	def shutdown(self):
		self.socket.close()
		HTTPServer.shutdown(self)
 
class SimpleHttpServer():
	def __init__(self, ip, port):
		self.server = ThreadedHTTPServer((ip,port), HTTPRequestHandler)

	def start(self):
		self.server_thread = threading.Thread(target=self.server.serve_forever)
		self.server_thread.daemon = True
		self.server_thread.start()

	def waitForThread(self):
		self.server_thread.join()

	def stop(self):
		self.server.shutdown()
		self.waitForThread()
 
if __name__=='__main__':
	parser = argparse.ArgumentParser(description='HTTP Server')
	parser.add_argument('port', type=int, help='Listening port for HTTP Server')
	parser.add_argument('ip', help='HTTP Server IP')
	args = parser.parse_args()

	server = SimpleHttpServer(args.ip, args.port)
	print 'HTTP Server Running...........'
	server.start()
	server.waitForThread()