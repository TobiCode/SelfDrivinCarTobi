# -*- coding: utf-8 -*-
"""
Server for AI Car Project

"""
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import persisting
import learningNN
import numpy as np


HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 80 # Maybe set this to 9000.

# API Routes - on the view of the car
SEND_DRIVING_DATA_ROUTE = '/sendDrivingData'
GET_DRIVING_DATA_ROUTE = '/getDrivingData'


class Request_Handler(BaseHTTPRequestHandler):
    
    learningManager = learningNN.LearningManager()

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
    
    
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        send_back = "<html><head><title>Autonomous Magic</title></head>"
        send_back += "<body><h1> Welcome to the server </h1>"
        send_back += "<p>Here the machine learning happens</p>"
        send_back += "</body></html>"
        s.wfile.write(bytes(send_back, "UTF-8"))


    #The car sends data via POST -> either full data to give training sets or just the environment
    #data to retrieve the commands
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        body = self.rfile.read(content_length) # <--- Gets the data itself
        #body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        path = self.path
        print("DEBUG BODY:" + str(body))
        #body_raw = json.dumps(body.decode("utf-8")) 
        body_raw = json.loads(body.decode("utf-8")) 
        print ("Received: " + str(body_raw))
        if path == SEND_DRIVING_DATA_ROUTE:
            print ("Data needs to be saved in training csv")
            persistanceManager = persisting.PersistanceManager()
            persistanceManager.getDataAndSave(body_raw)
            Request_Handler.learningManager = learningNN.LearningManager()
        elif path == GET_DRIVING_DATA_ROUTE:
            #Data which needs to be sent is: scaledSpeed, scaledForward, scaledLeftRightRatio
            #Output of model needs to be: isTurningLeft, isTurningRight, isKeepingStraight, isAccelerating
            print("Data is input for Model and command for car needs to be sent back------")
            data_dict = body_raw
            scaledForward = data_dict["data"]["scaledForward"]
            scaledSpeed = data_dict["data"]["scaledSpeed"]
            scaledLeftRightRatio = data_dict["data"]["scaledLeftRightRatio"]
            predict_input = [[scaledForward, scaledLeftRightRatio,scaledSpeed]]
            result =  Request_Handler.learningManager.predict(predict_input)
            print("Predicted: " + str(result))
            print("--------------------------------------------------")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            send_back = {'isTurningLeft': result[0], 'isTurningRight': result[1], 
                         'isKeepingStraight': result[2], 'isAccelerating': result[3]}
            send_back = json.dumps(send_back)
            self.wfile.write(bytes(send_back, "UTF-8"))

        else:
            print ("You accessed: ", path)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Succesfull json retrieved!!!!!!", "UTF-8"))

        
if __name__ == '__main__':
    np.random.seed(1337) # for reproducibility
    server_adress= (HOST_NAME, PORT_NUMBER)
    httpd = HTTPServer(server_adress, Request_Handler)
    
    print (time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print (time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))