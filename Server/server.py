# -*- coding: utf-8 -*-
"""
Server for AI Car Project

"""
import time
import BaseHTTPServer
import json
import learning


HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 80 # Maybe set this to 9000.

# API Routes
SEND_DRIVING_DATA_ROUTE = '/sendDrivingData'
GET_DRIVING_DATA_ROUTE = '/getDrivingData'


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Autonomous Magic</title></head>")
        s.wfile.write("<body><h1> Welcome to the server </h1>")
        s.wfile.write("<p>Here the machine learning happens</p>")
        s.wfile.write("</body></html>")
    #The car sends data via POST -> either full data to give training sets or just the environment
    #data to retrieve the commands
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.getheader('Content-Length', 0))))
        path = self.path
        body_raw = json.dumps(body)
        print ("Received: " + body_raw)
        if path == SEND_DRIVING_DATA_ROUTE:
            print "Data needs to be saved in training csv"
            persistanceManager = learning.PersistanceManager()
            persistanceManager.getDataAndSave(body_raw)
        elif path == GET_DRIVING_DATA_ROUTE:
            print("Data is input for Model and command for car needs to be sent back")
        else:
            print "You accessed: ", path
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write("Succesfull json retrieved!!!!!!")

        
if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = BaseHTTPServer.HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)