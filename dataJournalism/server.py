# flask --app data_server run
from flask import Flask
from flask import render_template
from flask import request
import json
import math

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def about():
    f = open("dataJournalism/data/math_scores.json")
    data = json.load(f)
    f.close()
    
    percentDict = {}
    for district in data:
        disadv2023 = data[district]["Econ Disadv"]["2023"]["NumTested"]
        notdisadv2023 = data[district]["Not Econ Disadv"]["2023"]["NumTested"]
        total = disadv2023 + notdisadv2023
        percentDict[district] = int((disadv2023/total)*100)

    lowestperc, highestperc = 101,0
    for district in percentDict:
        if (percentDict[district] > highestperc):
            highestperc = percentDict[district]
        if (percentDict[district] < lowestperc):
            lowestperc = percentDict[district]

    print(percentDict)
    print("Range is "+str(lowestperc)+"% to "+str(highestperc)+"%")
    
    return render_template('about.html')


app.run(debug=True)