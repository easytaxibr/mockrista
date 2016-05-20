#Modicado
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
 
positions = [
	{"lat": -23.542887 , "lng": -46.73158},
	{"lat": -23.542179 , "lng": -46.730915},
	{"lat": -23.541411 , "lng": -46.729907},
	{"lat": -23.541333 , "lng": -46.729113},
	{"lat": -23.541215 , "lng": -46.728255},
	{"lat": -23.541569 , "lng": -46.727933},
	{"lat": -23.541824 , "lng": -46.727697},
	{"lat": -23.542454 , "lng": -46.727203},
	{"lat": -23.542965 , "lng": -46.726795},
	{"lat": -23.543320 , "lng": -46.726152},
	{"lat": -23.543595 , "lng": -46.725658},
	{"lat": -23.544205 , "lng": -46.724006},
	{"lat": -23.544303 , "lng": -46.723105},
	{"lat": -23.544382 , "lng": -46.722032},
	{"lat": -23.544598 , "lng": -46.721216},
	{"lat": -23.544775 , "lng": -46.720251},
	{"lat": -23.544940 , "lng": -46.719849},
	{"lat": -23.545149 , "lng": -46.719221},
	{"lat": -23.545444 , "lng": -46.71862},
	{"lat": -23.545896 , "lng": -46.717869},
	{"lat": -23.546585 , "lng": -46.717032},
	{"lat": -23.547155 , "lng": -46.716324},
	{"lat": -23.547805 , "lng": -46.715659},
	{"lat": -23.548257 , "lng": -46.71523},
	{"lat": -23.548650 , "lng": -46.714844},
	{"lat": -23.548864 , "lng": -46.714516},
	{"lat": -23.549218 , "lng": -46.714162},
	{"lat": -23.549454 , "lng": -46.714312},
	{"lat": -23.549621 , "lng": -46.714527},
	{"lat": -23.549956 , "lng": -46.714838},
	{"lat": -23.550113 , "lng": -46.715117},
	{"lat": -23.550349 , "lng": -46.715418},
	{"lat": -23.550516 , "lng": -46.715686},
	{"lat": -23.550831 , "lng": -46.715997},
	{"lat": -23.551146 , "lng": -46.71619},
	{"lat": -23.552483 , "lng": -46.716952},
	{"lat": -23.552926 , "lng": -46.717209},
	{"lat": -23.553388 , "lng": -46.717424},
	{"lat": -23.553811 , "lng": -46.717671},
	{"lat": -23.554086 , "lng": -46.717992},
	{"lat": -23.552444 , "lng": -46.72134},
	{"lat": -23.551116 , "lng": -46.724065},
	{"lat": -23.549828 , "lng": -46.726704},
	{"lat": -23.549297 , "lng": -46.727348},
	{"lat": -23.548185 , "lng": -46.729333},
	{"lat": -23.547153 , "lng": -46.731114},
	{"lat": -23.546208 , "lng": -46.732391},
	{"lat": -23.545943 , "lng": -46.732702},
	{"lat": -23.545490 , "lng": -46.733195},
	{"lat": -23.544104 , "lng": -46.734311},
	{"lat": -23.542953 , "lng": -46.735438},
	{"lat": -23.542412 , "lng": -46.735223},
	{"lat": -23.541005 , "lng": -46.733807},
	{"lat": -23.540602 , "lng": -46.733378},
	{"lat": -23.540150 , "lng": -46.732991},
	{"lat": -23.540386 , "lng": -46.73268},
	{"lat": -23.540986 , "lng": -46.731994},
	{"lat": -23.541487 , "lng": -46.731393},
	{"lat": -23.541822 , "lng": -46.731039},
	{"lat": -23.542018 , "lng": -46.730781},
	{"lat": -23.542451 , "lng": -46.731135},
	{"lat": -23.543169 , "lng": -46.731886}
]

class HTTPRequestHandler(BaseHTTPRequestHandler):
	sessionCounter = {}
	arrived = False
	def getTheCurrentTaxiPosition(self, session):
		if session in self.sessionCounter:
			print "There is Session"
			tick = self.sessionCounter[session]
			tick = tick + 1
			self.sessionCounter[session] = tick
		else:
			print "There NO is Session"
			self.sessionCounter[session] = 0

		pos = self.sessionCounter[session]

		if len(positions) > pos:
			self.arrived = False
			return positions[pos]
		else:
			self.arrived = True
			return positions[len(positions) - 1]
	def randomTaxiPositionJson(self, lat, lng, n):
		taxis = []

		radius = 500
		radiusInDegrees=float(radius)/float(111300)
		r = radiusInDegrees
		x0 = float(lat)
		y0 = float(lng)

		for i in range(1,n):
			u = float(random.random())
			v = float(random.random())
			
			w = r * math.sqrt(u)
			t = 2 * math.pi * v
			x = w * math.cos(t) 
			y = w * math.sin(t)
		  	
			print "x %f y %f" % (x, y)

			xLat  = x + x0
			yLong = y + y0

			taxis.append({"lat": xLat , "lng": yLong, "driver-name" : "Driver Test", "driver-car" : "Driver Car"})
		return taxis
	def do_GET(self):
		try:
			if None != re.search('/api/taxi-position/the-taxi/*', self.path):
				query = urlparse(self.path).query
				query_components = dict(qc.split("=") for qc in query.split("&"))
				session = query_components["session"]

				response = {"driver_name": "Foo Bar",
							"car_model" : "Tesla Model", 
							"license_plate" : "FOO-4242",
							"position" : self.getTheCurrentTaxiPosition(session),
							"is_arravied" : self.arrived}

				self.send_response(200)
				self.send_header('Content-Type', 'application/json')
				self.end_headers()
				self.wfile.write(json.dumps(response))

			elif None != re.search('/api/gettaxis/*', self.path):
				query = urlparse(self.path).query
				query_components = dict(qc.split("=") for qc in query.split("&"))
				lat = query_components["lat"]
				lng = query_components["lng"]

				response = {"taxis": self.randomTaxiPositionJson(lat, lng, 100)}

				self.send_response(200)
				self.send_header('Content-Type', 'application/json')
				self.end_headers()
				self.wfile.write(json.dumps(response))

			elif None != re.search('/api/taxi-avarage-eta/*', self.path):
				query = urlparse(self.path).query
				query_components = dict(qc.split("=") for qc in query.split("&"))
				lat = query_components["lat"]
				lng = query_components["lng"]

				response = {"taxis": self.randomTaxiPositionJson(lat, lng, 10),
							"agarage-eta": 5}

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
