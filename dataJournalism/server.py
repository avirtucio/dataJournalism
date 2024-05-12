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

@app.route('/citywidescores')
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

    if (type(request.args.get('year')) != str):
        year = "2023"
    elif (type(request.args.get('year')) == str):
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
    
    lowestScore=100
    highestScore=0
    highestScoreDistrict = "0"
    lowestScoreDistrict = "0"
    for district in avg_Score:
        if avg_Score[district] > highestScore:
            highestScore = avg_Score[district]
            highestScoreDistrict = district
        if avg_Score[district] < lowestScore:
            lowestScore = avg_Score[district]
            lowestScoreDistrict = district
    
    lowestEconDisadvPop=100
    highestEconDisadvPop=0
    lowestEconDisadvPopDistrict="0"
    highestEconDisadvPopDistrict="0"
    for district in percent_Disadv:
        if percent_Disadv[district] > highestEconDisadvPop:
            highestEconDisadvPop = percent_Disadv[district]
            highestEconDisadvPopDistrict = district
        if percent_Disadv[district] < lowestEconDisadvPop:
            lowestEconDisadvPop = percent_Disadv[district]
            lowestEconDisadvPopDistrict = district
            
    bar_Colors = []
    for percent in range(90,6,-12):
        bar_Colors.append("hsl(0,100%,"+str(percent)+"%)")
    #range from 30%-100%
    #0;90 1;80 2;70 3;60 4;50 5;40 6;30
    #0;brightest                   6;darkest

    data_Points_to_Colors = {}
    for district in percent_Disadv:
        data_Points_to_Colors[district] = bar_Colors[math.floor(percent_Disadv[district]/10) - 3]
    #30-39%;0 40-49%;1 50-59%;2 60-69%;3 70-79%;4 80-89%;5 90-99%;6

    return render_template('citywidescores.html', data=data, years=years, districts=districts, percent_Disadv=percent_Disadv, avg_Score=avg_Score, bar_Colors=bar_Colors, data_Points_to_Colors=data_Points_to_Colors, year=year,
                           lowestScore=(lowestScore/100)*4, highestScore=(highestScore/100)*4, lowestScoreDistrict=lowestScoreDistrict, highestScoreDistrict=highestScoreDistrict,
                           lowestEconDisadvPop=lowestEconDisadvPop, highestEconDisadvPop=highestEconDisadvPop, lowestEconDisadvPopDistrict=lowestEconDisadvPopDistrict,
                           highestEconDisadvPopDistrict=highestEconDisadvPopDistrict)

@app.route('/districtscores/<district>')
def micro(district):
    f = open("dataJournalism/data/math_scores.json")
    data = json.load(f)
    f.close()

    if (type(request.args.get('score')) != str):
        score = "4"
    elif (type(request.args.get('score')) == str):
        score = request.args.get('score')

    years = []
    for year in data["1"]["Econ Disadv"]:
        years.append(year)
    numYears = len(years)-1
    
    districts = []
    for dist in data:
        districts.append(dist)

    district_Scores = {}
    district_Scores["Econ Disadv"], district_Scores["Not Econ Disadv"] = {}, {}
    for year in data[district]["Econ Disadv"]:
        district_Scores["Econ Disadv"][year] = data[district]["Econ Disadv"][year]["Pct"+score]
    for year in data[district]["Not Econ Disadv"]:
        district_Scores["Not Econ Disadv"][year] = data[district]["Not Econ Disadv"][year]["Pct"+score]

    sumPercDisadv=0
    amntPercDisadv=0
    for year in district_Scores["Econ Disadv"]:
        sumPercDisadv+=district_Scores["Econ Disadv"][year]
        amntPercDisadv+=1
    avgPercDisadv=sumPercDisadv/amntPercDisadv

    sumPercNotDisadv=0
    amntPercNotDisadv=0
    for year in district_Scores["Not Econ Disadv"]:
        sumPercNotDisadv+=district_Scores["Not Econ Disadv"][year]
        amntPercNotDisadv+=1
    avgPercNotDisadv=sumPercNotDisadv/amntPercNotDisadv

    if avgPercDisadv > avgPercNotDisadv:
        higherCategory = "economically disadvantaged"
    else:
        higherCategory= "non economically disadvantaged"


    return render_template('districtscores.html', data=data, years=years, districts=districts, district=str(district), 
                           district_Scores=district_Scores, numYears=numYears, score=score, higherCategory=higherCategory)

app.run(debug=True)