# -*- coding: utf-8 -*-
"""
Server for AI Car Project

"""
import time
import BaseHTTPServer
import json
import persisting
import learningV2NaiveBayes


HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 80 # Maybe set this to 9000.

# API Routes - on the view of the car
SEND_DRIVING_DATA_ROUTE = '/sendDrivingData'
GET_DRIVING_DATA_ROUTE = '/getDrivingData'


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    learningManager = learningV2NaiveBayes.LearningManagerNB()
    
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
            persistanceManager = persisting.PersistanceManager()
            persistanceManager.getDataAndSave(body_raw)
            MyHandler.learningManager = learningV2NaiveBayes.LearningManagerNB()
        elif path == GET_DRIVING_DATA_ROUTE:
            #Data which needs to be sent is: scaledSpeed, scaledForward, scaledLeftRightRatio
            #Output of model needs to be: isTurningLeft, isTurningRight, isKeepingStraight, isAccelerating
            print("Data is input for Model and command for car needs to be sent back------")
            data_dict = json.loads(body_raw)
            scaledForward = data_dict["data"]["scaledForward"]
            scaledSpeed = data_dict["data"]["scaledSpeed"]
            scaledLeftRightRatio = data_dict["data"]["scaledLeftRightRatio"]
            predict_input = [[scaledForward, scaledLeftRightRatio,scaledSpeed]]
            result =  MyHandler.learningManager.predict(predict_input)
            print("Predicted: " + str(result))
            print("--------------------------------------------------")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            send_back = {'isTurningLeft': result[0], 'isTurningRight': result[1], 
                         'isKeepingStraight': result[2], 'isAccelerating': result[3]}
            send_back = json.dumps(send_back)
            self.wfile.write(send_back)

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