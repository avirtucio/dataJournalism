# flask --app data_server run
from flask import Flask
from flask import render_template
from flask import request
import json
import math

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/about')
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

    years = []
    for year in data["1"]["Econ Disadv"]:
        years.append(year)
    
    districts = []
    for district in data:
        districts.append(district)

    return render_template('about.html', data=data, years=years, districts=districts)

@app.route('/macro')
def macro():
    f = open("dataJournalism/data/math_scores.json")
    data = json.load(f)
    f.close()

    years = []
    for year in data["1"]["Econ Disadv"]:
        years.append(year)
    
    districts = []
    for district in data:
        districts.append(district)

    if (type(request.args.get('year')) != 'str'):
        year = "2023"
    else:
        year = request.args.get('year')

    percent_Disadv = {}
    for district in data:
        numDisadv = data[district]["Econ Disadv"][year]["NumTested"]
        numNotDisadv = data[district]["Not Econ Disadv"][year]["NumTested"]
        percent_Disadv[district] = int((numDisadv/(numDisadv+numNotDisadv))*100)

    avg_Score = {}
    for district in data:
        notDisadvTesters = data[district]["Not Econ Disadv"][year]["NumTested"]
        disadvTesters = data[district]["Econ Disadv"][year]["NumTested"]
        totalTests = notDisadvTesters + disadvTesters
        total1 = (data[district]["Not Econ Disadv"][year]["Pct1"])*notDisadvTesters + (data[district]["Econ Disadv"][year]["Pct1"])*disadvTesters
        total2 = (data[district]["Not Econ Disadv"][year]["Pct2"])*notDisadvTesters + (data[district]["Econ Disadv"][year]["Pct2"])*disadvTesters
        total3 = (data[district]["Not Econ Disadv"][year]["Pct3"])*notDisadvTesters + (data[district]["Econ Disadv"][year]["Pct3"])*disadvTesters
        total4 = (data[district]["Not Econ Disadv"][year]["Pct4"])*notDisadvTesters + (data[district]["Econ Disadv"][year]["Pct4"])*disadvTesters
        avg = (total1 + total2*2 + total3*3 + total4*4)/(totalTests*4)
        avg_Score[district] = int(avg)

    bar_Colors = []
    for percent in range(51,107,7):
        bar_Colors.append("hsl(0,100%,"+str(percent)+"%)")
    #range is 100% to 30%
    
    return render_template('macro.html', data=data, years=years, districts=districts, percent_Disadv=percent_Disadv, avg_Score=avg_Score, bar_Colors=bar_Colors)

@app.route('/micro/<district>')
def micro(district):
    f = open("dataJournalism/data/math_scores.json")
    data = json.load(f)
    f.close()

    years = []
    for year in data["1"]["Econ Disadv"]:
        years.append(year)
    
    districts = []
    for dist in data:
        districts.append(dist)

    return render_template('micro.html', data=data, years=years, districts=districts, district=district)

app.run(debug=True)