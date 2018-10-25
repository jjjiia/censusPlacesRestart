import json
import csv

def convertCsvToJson(inputFileName,outputFileName):
    csvInput = csv.reader(open(inputFileName,"r"))
    for row in csvInput:
        header = row
        break
    
    jsonOutput = {}
    for row in csvInput:
        gid = row[0]
        jsonOutput[gid]={}
        for i in range(0,len(header)):
            value = row[i]
            key = header[i]
            jsonOutput[gid][key]=value
    with open(outputFileName, "wb") as outfile:
        json.dump(jsonOutput,outfile)
    
fileId = "R11891292_SL150"
convertCsvToJson("data/"+fileId+".csv","data/"+fileId+".json")