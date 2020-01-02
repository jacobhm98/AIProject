# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 14:17:32 2019

@author: Oscar
"""

# This program predicts stock prices by using machine learning models

#Install the dependencies
import numpy as np 
from tiingo import TiingoClient
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
import array as arr
import datetime

class Prediction:
    
    def dates(self, days):
        now = datetime.datetime.now() # current date and time

        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")

        currentDate = year + "/" + month + "/" + day
        end_date = now - datetime.timedelta(days)

        prevYear = end_date.strftime("%Y")
        prevMonth = end_date.strftime("%m")
        prevDay = end_date.strftime("%d")

        prevDate = prevYear + "/" + prevMonth + "/" + prevDay
        
        return prevDate, currentDate
    
    def volume(this_object, stock, days, prevDays):
        config = {}
        config['session'] = True
        #Probably shouldn't use my API-key
        config['api_key'] = "5bb2f699440e3f8aeba0b5d8ab6467c00af165bc"
        
        prevDate, currentDate = this_object.dates(days)

        client = TiingoClient(config)
        ticker_history = client.get_dataframe(stock, startDate=prevDate, 
                                              endDate=currentDate)
        
        pDate, cDate = this_object.dates(prevDays)

        ticker_history_last = client.get_dataframe(stock, startDate=pDate, 
                                              endDate=cDate)
        
        #Array of previous volumes
        X = np.array(ticker_history['volume'])
        Y = np.array(ticker_history_last['volume'])
        #print(X)
        #print(Y)
        
        #returns average lastdays divided by average of Days(argument) 
        return np.average(Y) / np.average(X)
    
    def predict(this_object, stock, days):
        config = {}
        config['session'] = True
        #Probably shouldn't use my API-key
        config['api_key'] = "5bb2f699440e3f8aeba0b5d8ab6467c00af165bc"
        
        prevDate, currentDate = this_object.dates(days)        
        
        client = TiingoClient(config)
        ticker_history = client.get_dataframe(stock, startDate=prevDate,
                                          endDate=currentDate)
 
        ticker_history = ticker_history[['close']]
        
        #print(ticker_history.tail(10))
        
        # A variable for predicting 'n' days out into the future
        forecast_out = 30 #forecast_out = 'n=30' days
        
        ticker_history['Prediction'] = ticker_history[['close']].shift(-forecast_out)
        
        ### Create the indeoendent data set (X)  #######
        # Convert the dataframe to a numpy array
        X = np.array(ticker_history.drop(['Prediction'],1))
        
        #Remove the last 'n' rows
        X = X[:-forecast_out]
        
        ### Create the dependent data set (y)  #####
        # Convert the dataframe to a numpy array (All of the values including the NaN's)
        y = np.array(ticker_history['Prediction'])
        # Get all of the y values except the last 'n' rows
        y = y[:-forecast_out]
        
        # Split the data into 90% training and 20% testing
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
        
        # Create and train the Support Vector Machine (Regressor)
        svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.00001)
        svr_rbf.fit(x_train, y_train)
        # Testing Model: Score returns the coefficient of determination R^2 of the prediction. 
        # The best possible score is 1.0
        svm_confidence = svr_rbf.score(x_test, y_test)
        #print("svm confidence: ", svm_confidence)
            
        # Create and train the Linear Regression  Model
        lr = LinearRegression()
        # Train the model
        lr.fit(x_train, y_train)
        
        # Testing Model: Score returns the coefficient of determination R^2 of the prediction. 
        # The best possible score is 1.0
        lr_confidence = lr.score(x_test, y_test)
        #print("lr confidence: ", lr_confidence)
        
        # Set x_forecast equal to the last 30 rows of the original data set from Adj. Close column
        x_forecast = np.array(ticker_history.drop(['Prediction'],1))[-forecast_out:]
        #print(x_forecast)
        #print(ticker_history.tail(30))
        
        # Print linear regression model predictions for the next 'n' days
        lr_prediction = lr.predict(x_forecast)
        #print(lr_prediction)
        
        # Print support vector regressor model predictions for the next 'n' days
        svm_prediction = svr_rbf.predict(x_forecast)
        #print(svm_prediction)
        
        svm_array = arr.array('d',svm_prediction)
        lr_array = arr.array('d',lr_prediction)
        
        return svm_array, lr_array, svm_confidence, lr_confidence  
    
    def inference(this_object, stock, predDays, prevVolume, baseVolume):
        
        svm_array, lr_array, svm_confidence, lr_confidence = this_object.predict(stock, predDays)
        volume_confidence = this_object.volume(stock, prevVolume, baseVolume)
        
        return svm_array, lr_array, svm_confidence, lr_confidence, volume_confidence
