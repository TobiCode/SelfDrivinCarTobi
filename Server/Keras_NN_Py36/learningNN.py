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
from sklearn.model_selection import train_test_split 

#by default Keras's model.compile() sets the shuffle argument as True. 
#You should the set numpy seed before importing keras. e.g.
np.random.seed(1337) # for reproducibility

from keras.models import Sequential
from keras.layers import Dense, Activation


#used to load data
DATA_DUMP_DIRECTORY = 'data_dump'
TRAINING_DATA_FILE = "training_data.csv"
NORMALIZE = True

class LearningManager:
    
    def __init__(self):
        print ("----------Build models, train them and test them....---------")
        if os.path.exists(DATA_DUMP_DIRECTORY):
            print ("Data_dump folder exists")
            os.chdir(DATA_DUMP_DIRECTORY)
            filepath = TRAINING_DATA_FILE
            if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
                print ("File with Data already exists, the ML-Algorithm can be trained -> Read File Data")
                with open(TRAINING_DATA_FILE, 'rt') as csvfile:
                    file_reader = csv.reader(csvfile)
                    #skip header
                    next(file_reader)
                    next(file_reader)
                    whole_data=[]
                    for line in file_reader:
                        whole_data.append(line)
                    whole_data = np.asarray(whole_data)  
                    whole_data = whole_data.astype(np.float)
                    print(whole_data)
                    
                    
                    #create train_x, train_Y, test_x, test_Y
                    
                    #Used for normalizing input values
                    #Use min-max normalization
                    max_scaled_forward = maxValueListList(0, whole_data)
                    min_scaled_forward = minValueListList(0, whole_data) 

                    
                    max_scaled_speed = maxValueListList(2, whole_data)
                    min_scaled_speed = minValueListList(2, whole_data)

                    X= []
                    Y= []
                    for datavector in whole_data:
                        datavector = list(map(float, datavector))
                        #Normalize Training Data
                        #normalizeScaledForward
                        datavector[0] = (datavector[0] - min_scaled_forward) / (max_scaled_forward- min_scaled_forward)
                        
                        #normalize speed
                        datavector[2] = (datavector[2] - min_scaled_speed) / (max_scaled_speed - min_scaled_speed)
                        
                        
                        #X has datavectors with [scaled_forward, scaledLeftRightRatio and scaledSpeed]
                        X.append([datavector[0],datavector[1], datavector[2]])
                        #Y has datavectors with [isTurningLeft, isTurningRight, isKeepingStraight, isAccelerating]
                        Y.append([datavector[3],datavector[4], datavector[5], datavector[6]])
                    
                    
                    
                    print("Elements of X look like:" + str(X[0]))
                    print("Elements of Y look like:" + str(Y[0]))
                    
                    X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = train_test_split(X,Y, test_size=0.3, random_state=2, shuffle=False)
                    X_TRAIN = np.asarray(X_TRAIN)
                    X_TEST = np.asarray(X_TEST)
                    Y_TRAIN = np.asarray(Y_TRAIN)
                    Y_TEST = np.asarray(Y_TEST)
                    print("Anzahl an Trainingsdaten:" + str(len(X_TRAIN)))
                    print("Anzahl an Testdaten:" + str(len(X_TEST)))
                    #End create training testing datasets
                    
                    
                    #Create Model 
                    self.model = Sequential()
                    self.model.add(Dense(8, input_shape=(3,), activation='relu'))
                    self.model.add(Dense(4, activation='sigmoid'))
                    self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

                    
                    #Train the model
                    self.model.fit(X_TRAIN, Y_TRAIN, epochs=1, validation_data=(X_TEST,Y_TEST), verbose =2)
                    
                    
                    #Evaluate the model
                    score = self.model.evaluate(X_TEST, Y_TEST, batch_size=32)
                    print("Score of Model: " + str(score))
                    
            else:
                print ("File does not exist -> Tell Unity that the user has to train first")


        else:
            print ("File does not exist-> Tell Unity that the user has to train first")
            
        os.chdir("..")
    
    def predict(self, data):
        data_as_np = np.array(data).astype(np.float)
        
        predicted = self.model.predict(data_as_np)
        print ("Predicted not round:" + str(predicted))
        predicted = np.around(predicted[0]).astype(int).tolist()
        
        return predicted
        
def maxValueListList(index, llist):
    return max(sublist[index] for sublist in llist)
def minValueListList(index, llist):
    return min(sublist[index] for sublist in llist)

if __name__ == '__main__':
    learningManager = LearningManager()
    print ("------------------")
    print ("Input Array: scaledForward, scaledLeftRightRatio, scaledSpeed")
    testArray = [0.22880003720806005, 0.0, 0.11407798294863335]
    print ("Input Array: " + str(testArray))
    print("Prediction:[isTurningLeft, isTurningRight, isKeepingStraight, isAccelerating]")
    testPredict = learningManager.predict([testArray])
    print ("Predicted round: " + str(testPredict))
           