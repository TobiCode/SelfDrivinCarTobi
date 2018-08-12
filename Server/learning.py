# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 19:13:59 2018
First Try with Naive Bayes 
https://www.analyticsvidhya.com/blog/2017/09/naive-bayes-explained/
@author: Tobi

'ScaledForward', 'scaledLeftRightRatio', 'ScaledSpeed',
                               'isTurningLeft', 'isTurningRight', 'isKeepingStraight', 
                               'isAccelerating'
"""

import os
import csv
import json
import numpy as np
from sklearn.naive_bayes import GaussianNB


#used to load data
DATA_DUMP_DIRECTORY = 'data_dump'
TRAINING_DATA_FILE = "training_data.csv"

class LearningManagerNB:
    def __init__(self):
        if os.path.exists(DATA_DUMP_DIRECTORY):
            print "Data_dump folder exists"
            os.chdir(DATA_DUMP_DIRECTORY)
            filepath = TRAINING_DATA_FILE
            if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
                print "File with Data already exists, the ML-Algorithm can be trained -> Read File Data"
                with open(TRAINING_DATA_FILE, 'rb') as csvfile:
                    file_reader = csv.reader(csvfile)
                    #skip header
                    next(file_reader)
                    whole_data=[]
                    for line in file_reader:
                        whole_data.append(line)
                    print whole_data[1]
                    #create train_x, train_Y, test_x, test_Y
                    length_dataset = len(whole_data)
                    print "Length of Dataset: " , length_dataset
                    length_train = (length_dataset/4) * 3
                    print "Length of Training-Data: " , length_train
                    train_counter = 0
                    train_x=[]
                    train_Y = []
                    while train_counter< length_train:
                        #train_x
                        scaled_forward = whole_data[train_counter][0]
                        scaledLeftRightRatio = whole_data[train_counter][1]
                        scaledSpeed = whole_data[train_counter][2]
                        train_x_1 = [scaled_forward,scaledLeftRightRatio,scaledSpeed]
                        train_x.append(train_x_1)
                        #train_Y
                        isTurningLeft = whole_data[train_counter][3]
                        isTurningRight = whole_data[train_counter][4]
                        isKeepingStraight= whole_data[train_counter][5]
                        isAccelerating = whole_data[train_counter][6]
                        train_Y_1 = [isTurningLeft, isTurningRight,isKeepingStraight, isAccelerating]
                        train_Y.append(train_Y_1)
                        train_counter +=1
                    #Create Model
                    model = GaussianNB()
                    # Train the model using the training sets
                    train_x_np = np.array(train_x)
                    train_Y_np = np.array(train_Y)
                    model.fit(train_x_np, train_Y_np)
        else:
            print "File does not exist-> Tell Unity that the user has to train first"
            
        os.chdir("..")
                
#1.Data loading and preperation


if __name__ == '__main__':
    learningManager = LearningManagerNB()
           