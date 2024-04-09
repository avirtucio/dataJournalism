import json

f1 = open("dataJournalism/data/Test_Scores_by_Econ.csv", "r")
lines = f1.readlines()

dictionary = {}

for lineIndex in range(1, len(lines)):
    #split each line into another array of values separated by commas, use each value as needed
    splitLine = lines[lineIndex].split(",")
    
    if (splitLine[1] not in dictionary): #if district is not in dictionary
        dictionary[splitLine[1]] = {} #dictionary of district
    
    if (splitLine[4] not in dictionary[splitLine[1]]): #if econ not in districtDict
        dictionary[splitLine[1]][splitLine[4]] = {} #dictionary of econ per district
    
    if (splitLine[3] not in dictionary[splitLine[1]][splitLine[4]]): #if yr not in districtEconDict
        dictionary[splitLine[1]][splitLine[4]][splitLine[3]] = {} #dictionary of yr per econ per district
    
    dictionary[splitLine[1]][splitLine[4]][splitLine[3]]["NumTested"] = int(splitLine[5]) #num of students tested from the category of district, econ, yr
    dictionary[splitLine[1]][splitLine[4]][splitLine[3]]["Pct1"] = float(splitLine[7]) # % of those students who scored 1
    dictionary[splitLine[1]][splitLine[4]][splitLine[3]]["Pct2"] = float(splitLine[8]) # % of those students who scored 2
    dictionary[splitLine[1]][splitLine[4]][splitLine[3]]["Pct3"] = float(splitLine[9]) # % of those students who scored 3
    dictionary[splitLine[1]][splitLine[4]][splitLine[3]]["Pct4"] = float(splitLine[10]) # % of those students who scored 4

f1.close()

f2 = open("math_scores.json", "w")
json.dump(dictionary, f2, indent = 4)

f2.close()