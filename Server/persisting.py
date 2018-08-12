# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 13:03:25 2018
        #Data which needs to be sent is: scaledSpeed, scaledForward, scaledLeftRightRatio
        #Output of model needs to be: isTurningLeft, isTurningRight, isKeepingStraight, isAccelerating
@author: Tobi
"""

import os
import csv
import json


#used to save training data or to load it 
DATA_DUMP_DIRECTORY = 'data_dump'
TRAINING_DATA_FILE = "training_data.csv"
example_json = '{"data":[{"scaledForward":23.93192,"scaledLeftRightRatio":0.5572439,"isAccelerating":1,"scaledSpeed":15.03786,"isTurningLeft":0,"isTurningRight":0,"isKeepingStraight":1},{"scaledForward":18.0533,"scaledLeftRightRatio":0.6257154,"isAccelerating":1,"scaledSpeed":26.89997,"isTurningLeft":0,"isTurningRight":1,"isKeepingStraight":0},{"scaledForward":20.39035,"scaledLeftRightRatio":0.6053656,"isAccelerating":1,"scaledSpeed":35.61538,"isTurningLeft":0,"isTurningRight":0,"isKeepingStraight":1}],"types":["motion","steering"]}'


class PersistanceManager:
    def __init__(self):
        if os.path.exists(DATA_DUMP_DIRECTORY):
            print "data_dump folder exists"
        else:
            os.mkdir(DATA_DUMP_DIRECTORY)
            print("Created data_dump folder")
        filepath = os.path.join(DATA_DUMP_DIRECTORY, TRAINING_DATA_FILE)
        if os.path.isfile(filepath):
            print "Training data file already exists"
        else:
            os.chdir(DATA_DUMP_DIRECTORY)
            with open('training_data.csv', 'wt') as csvfile:
                print("Created training_data file")
                field_names = ['ScaledForward', 'scaledLeftRightRatio', 'ScaledSpeed',
                               'isTurningLeft', 'isTurningRight', 'isKeepingStraight', 
                               'isAccelerating']
                writer = csv.DictWriter(csvfile, fieldnames = field_names)
                #First 3 variables are current and Environment Varibales which are needed as an input for Model
                #Last 4 variables are commands for the car, they are the output of the machine learning model
                #writer.writerow(('ScaledForward', 'scaledLeftRightRatio', 'ScaledSpeed', 'isTurningLeft', 'isTurningRight', 
                                 #'isKeepingStraight', 'isAccelerating'))
                writer.writeheader()
            os.chdir("..")
   
            
   
    def getDataAndSave(self, data):
        data_dict = json.loads(data)
        print  (data_dict["data"][0]["scaledForward"])
        print  (data_dict["data"][0]["scaledLeftRightRatio"])
        print  (data_dict["data"][0]["isAccelerating"])
        print  (data_dict["data"][0]["scaledSpeed"])
        print  (data_dict["data"][0]["isTurningLeft"])
        print  (data_dict["data"][0]["isTurningRight"])
        print  (data_dict["data"][0]["isKeepingStraight"])
        
        os.chdir(DATA_DUMP_DIRECTORY)
        with open('training_data.csv', 'ab') as csvfile:
            writer = csv.writer(csvfile)
            for t in data_dict["data"]:
                writer.writerow((t["scaledForward"], t["scaledLeftRightRatio"], 
                                  t["scaledSpeed"], 
                                 t["isTurningLeft"], t["isTurningRight"],
                                 t["isKeepingStraight"], t["isAccelerating"])) 
        os.chdir("..")

    
if __name__ == '__main__':
    persistanceManager = PersistanceManager()
    persistanceManager.getDataAndSave(example_json)
           
            