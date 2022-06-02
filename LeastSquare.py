import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from DumpToSqlLite import DumpToSqlLite
from Graphs import plotIdealFunctions,plotTestData
from pyparsing import Or

#Read Data and keep in memory variables
trainCsv = pd.read_csv('train.csv')
idealCsv = pd.read_csv('ideal.csv')
testCsv = pd.read_csv('test.csv')

trainingFunctionWithoutX = trainCsv
trainingFunction = trainCsv
trainingFunctionWithoutX = trainingFunctionWithoutX.drop(trainingFunctionWithoutX.columns[0], axis=1)
idealFunctionWithoutX = idealCsv
idealFunction = idealCsv
idealFunctionWithoutX = idealFunctionWithoutX.drop(idealFunctionWithoutX.columns[0], axis=1)
testFunction = testCsv

def calculateError(firstFunction, secondFunction):
    # Calculates Squared error based on two function's distance
    MSE = np.square(np.subtract(secondFunction,firstFunction)).mean()
    s = np.sum((secondFunction-firstFunction)**2)
    return s

def computeTolerance(trainFunction,bestFunction):
    df = pd.DataFrame(trainingFunctionWithoutX[trainFunction.name])
    df.rename(columns = {trainFunction.name : 'trainData'}, inplace = True)
    df['ideal'] =idealFunction[bestFunction]
    distance = df['trainData'] - df['ideal']
    maxDistance=max(distance.abs())
    tolerance = math.sqrt(2) * maxDistance
    xIdeal = pd.DataFrame({'x': idealFunction['x'].values})
    xIdeal['y'] = idealFunction[bestFunction].values
    data = {'BestFunction': bestFunction,
        'tolerance': tolerance,
        'training_function':trainFunction,
        'idealDataFrame' : xIdeal}
    return data


def computeBestFunction(trainFunction, listOfIdealFunctions):
    functionWithSmallestError = None
    smallestError = None
    for (columnData) in listOfIdealFunctions:
        error = calculateError(trainFunction, listOfIdealFunctions[columnData])
        if ((smallestError == None) or error < smallestError):
            smallestError = error
            functionWithSmallestError = columnData
            

    functionWithSmallestError = computeTolerance(trainFunction,functionWithSmallestError)
    functionWithSmallestError['error'] = smallestError
    return functionWithSmallestError

def findTestDataRow(point, idealFunctions):
    ###
    # This function finds every row of Test Data with the ideal function data
    ###
    lowestClassfication = None
    lowestDistance = None

    for idealFunc in idealFunctions:
        df = pd.DataFrame(idealFunc['BestFunction']['BestFunction'])
        df['x'] = idealFunction['x']
        try:
             yLocation =  df.loc[df['x'] == point[1]['x']]    
             yLocation = yLocation.iat[0,0]
        except IndexError:
            print("There is an index error for the point.")
            raise IndexError

        # finds the absolute absoluteDistance
        absoluteDistance = abs(yLocation - point[1]['y'])
        if (abs(absoluteDistance < idealFunc['tolerance'])):
            # returns the lowest distance
            if lowestDistance is None:
                lowestDistance =0
           
            if ((lowestClassfication is None) or (absoluteDistance < lowestDistance)):
                lowestClassfication = idealFunc
                lowestDistance = absoluteDistance

    return lowestClassfication, lowestDistance

idealFunctions = []
for (columnData) in trainingFunctionWithoutX:
    # find best fitting function
    idealFunctionResult = computeBestFunction(trainFunction=trainingFunctionWithoutX[columnData],
                                     listOfIdealFunctions=idealFunctionWithoutX)
    idealFunctions.append(idealFunctionResult)


testDataArray = []
testDataSetPoints = pd.DataFrame(testFunction,
                                 columns=testFunction.columns) 

idealRowsData = []
x = None
df = pd.DataFrame(idealFunction, 
                columns =idealFunction.columns)
for idealRows in idealFunctions:
    trainingDataFrame = pd.DataFrame({'x': trainingFunction['x'].values})
    trainingDataFrame['y'] = trainingFunction[idealRows['training_function'].name].values
    bestFunction = {'BestFunction' :df[idealRows['BestFunction']],'idealDataFrame' :idealRows['idealDataFrame']}
    trainingfunction = {'training_function':idealRows['training_function'],'trainingDataFrame':trainingDataFrame}
    result = {'BestFunction':bestFunction,
              'tolerance':idealRows['tolerance'],
              'training_function':trainingfunction,
              'error':idealRows['error'],
              'idealDataFrame':idealRows['idealDataFrame']}
    idealRowsData.append(result)

"""This Plots the 4 Ideal Functions from 50"""
plotIdealFunctions(idealRowsData, "plotIdealFunction")
   
for point in testDataSetPoints.iterrows():
    idealFunctionResult, yDelta = findTestDataRow(point=point , idealFunctions=idealRowsData)
    point = {'x':point[1]['x'],'y':point[1]['y']}
    if idealFunctionResult is None:
        bestIdealFunction = None
    else:
        bestIdealFunction = idealFunctionResult
    result = {"point": point, "classification": bestIdealFunction, "delta_y": yDelta}
    testDataArray.append(result)

"""This Plots the Test Data for all rows"""
plotTestData(testDataArray, "TestData&IdealFunctions")

"""This Writes data to SqlLite file"""
DumpToSqlLite(testDataArray)














