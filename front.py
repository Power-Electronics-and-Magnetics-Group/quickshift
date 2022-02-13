from main import solveIt
from stackups import parseStackup
from currentSharing import current_sharing_numeric
from colorprocessing import listDeterminer
from decimal import Decimal
from flask import Flask, request, url_for, redirect, render_template,jsonify
app = Flask(__name__)

@app.route('/')
def front():
    return render_template('index.html') 

@app.route('/evaluator')
def evaluator():
    if request.method == 'GET':
	return render_template('evaluator.html')
    if request.method == 'POST': 
	primary=request.form['primaryTurns']
	secondary=request.form['secondaryTurns']
	numLayers = int(request.form['numLayers'])
	completeStack = parseStackup(primary,Secondary,numLayers)
		 
@app.route('/optimizer',methods=["POST","GET"])
def optimizer():
    if request.method == 'GET':
        return render_template('optimizer.html')
    if request.method == 'POST':
        nValue=int(request.form['nValueForm'])
        turnsPerLayer=int(request.form['turnsPerLayer'])
        turnsRatio=int(request.form['turnsRatio'])
        solution = solveIt(nValue,turnsRatio,turnsPerLayer)
        output = solution[1]
        
        # for now
        inStack = solution[0][0]
        layerWidth=float(request.form['layerWidth'])
        operatingFrequency=int(request.form['operatingFrequency'])
        turnLength=float(request.form['turnLength'])
        layerDistances=float(request.form['layerDistances'])
        primaryCurrent=(request.form['primaryCurrent'])
        primCurrent=1.00000
        if(primaryCurrent!=""):
            primCurrent=float(primaryCurrent)
        solute = current_sharing_numeric(inStack,layerWidth,operatingFrequency,turnLength,layerDistances,primCurrent)
        currentList = solute[:nValue]
        hexList = listDeterminer(currentList)
        return render_template('optimizer.html',
                               output="{:.5E}".format(Decimal(output)),
                               inputs=inStack,
                               currentSolution=solute,
                               pC=primCurrent,
                               nVal=nValue,
                               hL=hexList)

