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
from sklearn.metrics import accuracy_score


#used to load data
DATA_DUMP_DIRECTORY = 'data_dump'
TRAINING_DATA_FILE = "training_data.csv"

class LearningManagerNB:
    def __init__(self):
        print "----------Build models, train them and test them....---------"
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
                    #create train_x and trainY's
                    train_counter = 0
                    train_x=[]
                    train_Y_isTurning_Left = []
                    train_Y_isTurning_Right = []
                    train_Y_isKeepingStraight = []
                    train_Y_isAcelerating = []
                    
                    while train_counter< length_train:
                        #train_x
                        scaled_forward = whole_data[train_counter][0]
                        scaledLeftRightRatio = whole_data[train_counter][1]
                        scaledSpeed = whole_data[train_counter][2]
                        train_x_1 = [scaled_forward,scaledLeftRightRatio,scaledSpeed]
                        train_x.append(train_x_1)
                        #train_Y_
                        isTurningLeft = whole_data[train_counter][3]
                        isTurningRight = whole_data[train_counter][4]
                        isKeepingStraight= whole_data[train_counter][5]
                        isAccelerating = whole_data[train_counter][6]
                        train_Y_isTurning_Left.append(isTurningLeft)
                        train_Y_isTurning_Right.append(isTurningRight)
                        train_Y_isKeepingStraight.append(isKeepingStraight)
                        train_Y_isAcelerating.append(isAccelerating)
                        train_counter +=1
                        
                    #Create test_x and test_Y's
                    test_counter = train_counter
                    test_x=[]
                    test_Y_isTurning_Left = []
                    test_Y_isTurning_Right = []
                    test_Y_isKeepingStraight = []
                    test_Y_isAcelerating = []
                    length_test_data = len(whole_data) - test_counter
                    print "Length of Test-Data: ",  length_test_data
                    while test_counter< len(whole_data):
                        #train_x
                        scaled_forward = whole_data[test_counter][0]
                        scaledLeftRightRatio = whole_data[test_counter][1]
                        scaledSpeed = whole_data[test_counter][2]
                        test_x_1 = [scaled_forward,scaledLeftRightRatio,scaledSpeed]
                        test_x.append(test_x_1)
                        #train_Y_
                        isTurningLeft = whole_data[test_counter][3]
                        isTurningRight = whole_data[test_counter][4]
                        isKeepingStraight= whole_data[test_counter][5]
                        isAccelerating = whole_data[test_counter][6]
                        test_Y_isTurning_Left.append(isTurningLeft)
                        test_Y_isTurning_Right.append(isTurningRight)
                        test_Y_isKeepingStraight.append(isKeepingStraight)
                        test_Y_isAcelerating.append(isAccelerating)
                        test_counter +=1 
                    
                    #Create Model 
                    #print test_x
                    self.model_isTurning_Left = GaussianNB()
                    self.model_isTurning_Right = GaussianNB()
                    self.model_isKeepingSTraight = GaussianNB()
                    self.model_isAccelerating = GaussianNB()

                    #Np-arrays needed for training
                    train_x_np = np.array(train_x).astype(np.float)
                    train_Y_isTurning_Left_np = np.array(train_Y_isTurning_Left).astype(np.float)
                    train_Y_isTurning_Right_np = np.array(train_Y_isTurning_Right).astype(np.float)
                    train_Y_isKeepingStraight_np = np.array(train_Y_isKeepingStraight).astype(np.float)
                    train_Y_isAcelerating_np = np.array(train_Y_isAcelerating).astype(np.float)
                    
                    #Train the model
                    self.model_isTurning_Left.fit(train_x_np, train_Y_isTurning_Left_np)
                    self.model_isTurning_Right.fit(train_x_np, train_Y_isTurning_Right_np)
                    self.model_isKeepingSTraight.fit(train_x_np, train_Y_isKeepingStraight_np)
                    self.model_isAccelerating.fit(train_x_np, train_Y_isAcelerating_np)
                    
                    #predict                   
                    predicted_isTurning_Left = self.model_isTurning_Left.predict(train_x_np)
                    predicted_isTurning_Right = self.model_isTurning_Right.predict(train_x_np)
                    predicted_isKeepingStraight = self.model_isKeepingSTraight.predict(train_x_np)
                    predicted_isAccelerating = self.model_isAccelerating.predict(train_x_np)
                    #print predicted_isKeepingStraight
                    
                    #Test the model
                    print "-----Test Score-----"
                    #http://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html
                    
                    score_isTurning_Left = accuracy_score(train_Y_isTurning_Left_np, 
                                                             predicted_isTurning_Left)
                    score_isTurningRight = accuracy_score(train_Y_isTurning_Right_np, 
                                                             predicted_isTurning_Right)
                    score_isKeepingStraight = accuracy_score(train_Y_isKeepingStraight_np, 
                                                             predicted_isKeepingStraight)
                    score_isAccelerating = accuracy_score(train_Y_isAcelerating_np, 
                                                             predicted_isAccelerating)
                    print "Score of isTurningLeft-Prediction: ", score_isTurning_Left
                    print "Score of isTurningRight-Prediction: ", score_isTurningRight
                    print "Score of isKeepingSTraight-Prediction: ", score_isKeepingStraight
                    print "Score of isAccelerating-Prediction: ", score_isAccelerating
                    
            else:
                print "File does not exist -> Tell Unity that the user has to train first"


        else:
            print "File does not exist-> Tell Unity that the user has to train first"
            
        os.chdir("..")
    
    def predict(self, data):
        data_as_np = np.array(data).astype(np.float)
        
        predicted_isTurning_Left = self.model_isTurning_Left.predict(data_as_np)
        predicted_isTurning_Right = self.model_isTurning_Right.predict(data_as_np)
        predicted_isKeepingStraight = self.model_isKeepingSTraight.predict(data_as_np)
        predicted_isAccelerating = self.model_isAccelerating.predict(data_as_np)  
        
        return [predicted_isTurning_Left[0], predicted_isTurning_Right[0], predicted_isKeepingStraight[0],
                predicted_isAccelerating[0]]

if __name__ == '__main__':
    learningManager = LearningManagerNB()
    print "------------------"
    testPredict = learningManager.predict([['26.33905', '0.5196293', '3.332337']])
    print testPredict
           