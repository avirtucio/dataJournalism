import json

f1 = open("Test_Scores_by_Econ.csv", "r")
lines = f1.readlines()

dictionary = {}

#lines is a list of each line in the csv
#parse thru each line to get what you want
#loops to make dictionary

for lineIndex in range(1, len(lines)+1):
    #split each line into another array of values separated by commas, use each value as needed
    splitLine = lines[lineIndex].split(",")
    
    if (splitLine[1] not in dictionary): #if district is not in dictionary
        dictionary[splitLine[1]] = {} #dictionary of district
        

f1.close()

f2 = open("math_scores.json", "w")
json.dump(dictionary, f2, indent = 4)

f2.close()