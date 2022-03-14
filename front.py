from main import solveIt
from stackups import parseStackup
from currentSharing import current_sharing_numeric
from colorprocessing import listDeterminer
from decimal import Decimal
from flask import Flask, request, url_for, redirect, render_template,jsonify
import numpy
import math
app = Flask(__name__)

@app.route('/')
def front():
    return render_template('index.html') 

@app.route('/evaluator',methods=["POST","GET"])
def evaluator():
    if request.method == 'GET':
        return render_template('evaluator.html')
    if request.method == 'POST': 
        primary=str(request.form['primaryTurns'])
        secondary=str(request.form['secondaryTurns'])
        nValue = int(request.form['nValueForm'])
        inStack = parseStackup(primary,secondary,nValue)

        layerWidth=float(request.form['layerWidth'])
        operatingFrequency=int(request.form['operatingFrequency'])
        turnLength=float(request.form['turnLength'])
        layerDistances=float(request.form['layerDistances'])

        primaryCurrent=(request.form['primaryCurrent'])
        primCurrent=1.00000
        if(primaryCurrent!=""):
            primCurrent=float(primaryCurrent)

        if (inStack==0):
            return render_template('evaluator.html',
                                    invalidStackup=1)

        d = math.sqrt(2*(1.68*math.pow(10,-8))/((2*math.pi*operatingFrequency)*(4*math.pi*pow(10,-7))))
        R = 1.68*math.pow(10,-8)*turnLength/(d*layerWidth)
        stackLoss = 0
        solute = current_sharing_numeric(inStack, layerWidth, operatingFrequency, turnLength, layerDistances)
        try:
            solutionVector = list(solute)
            for i in range(nValue,3*nValue):
                stackLoss = stackLoss + .5*R*((layerWidth*solutionVector[i])**2)
        except numpy.linalg.LinAlgError:
            solutionVector = [100] * 3*nValue
            stackLoss = 9999

        currentDensityList = solute[nValue:]
#        print(currentDensityList)
        hexList = listDeterminer(currentDensityList)
        hexListA = []
        for i in hexList:
            hexListA.append(i.zfill(6))
#        print(hexListA)
        return render_template('evaluator.html',
                                inputs=inStack,
                                sL="{:.5E}".format(Decimal(stackLoss)),
                                currentSolution=solute,
                                pC=primCurrent,
                                nVal=nValue,
                                hL=hexListA)
 
		 
@app.route('/optimizer',methods=["POST","GET"])
def optimizer():
    if request.method == 'GET':
        return render_template('optimizer.html')
    if request.method == 'POST':
        nValue=int(request.form['nValueForm'])
        turnsPerLayer=int(request.form['turnsPerLayer'])
        turnsRatio=int(request.form['turnsRatio'])
        layerWidth=float(request.form['layerWidth'])
        operatingFrequency=int(request.form['operatingFrequency'])
        turnLength=float(request.form['turnLength'])
        layerDistances=float(request.form['layerDistances'])
        solution = solveIt(nValue,turnsRatio,turnsPerLayer,layerWidth,operatingFrequency,turnLength,layerDistances)
        output = solution[1]
        options = solution[4]

        # for now
        inStack = solution[0][0]
        primaryCurrent=(request.form['primaryCurrent'])
        primCurrent=1.00000
        if(primaryCurrent!=""):
            primCurrent=float(primaryCurrent)
        solute = current_sharing_numeric(inStack,layerWidth,operatingFrequency,turnLength,layerDistances,primCurrent)
        currentDensityList = solute[nValue:]
        hexList = listDeterminer(currentDensityList)
        hexListA = []
        for i in hexList:
            hexListA.append(i.zfill(6))
        return render_template('optimizer.html',
                               output="{:.5E}".format(Decimal(output)),
                               inputs=inStack,
                               currentSolution=solute,
                               pC=primCurrent,
                               nVal=nValue,
                               hL=hexListA,
                               count=options)

