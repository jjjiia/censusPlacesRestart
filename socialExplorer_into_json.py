import json
import csv

def convertCsvToJson(inputFileName,outputFileName):
    csvInput = csv.reader(open(inputFileName,"r"))
    for row in csvInput:
        header = row
        break
    
    print header
    jsonOutput = {}
    for row in csvInput:
        gid = row[0]
        jsonOutput[gid]={}
        for i in range(0,len(header)):
            value = row[i]
            key = header[i]
            if key not in badKeys:
                jsonOutput[gid][key]=value
    with open(outputFileName, "wb") as outfile:
        json.dump(jsonOutput,outfile)

badKeys = ['Geo_FIPS', 'Geo_GEOID', 'Geo_NAME', 'Geo_QName', 'Geo_STUSAB', 'Geo_SUMLEV', 'Geo_GEOCOMP', 'Geo_FILEID', 'Geo_LOGRECNO', 'Geo_US', 'Geo_REGION', 'Geo_DIVISION', 'Geo_STATECE', 'Geo_STATE', 'Geo_COUNTY', 'Geo_COUSUB', 'Geo_PLACE', 'Geo_PLACESE', 'Geo_TRACT', 'Geo_BLKGRP', 'Geo_CONCIT', 'Geo_AIANHH', 'Geo_AIANHHFP', 'Geo_AIHHTLI', 'Geo_AITSCE', 'Geo_AITS', 'Geo_ANRC', 'Geo_CBSA', 'Geo_CSA', 'Geo_METDIV', 'Geo_MACC', 'Geo_MEMI', 'Geo_NECTA', 'Geo_CNECTA', 'Geo_NECTADIV', 'Geo_UA', 'Geo_UACP', 'Geo_CDCURR', 'Geo_SLDU', 'Geo_SLDL', 'Geo_VTD', 'Geo_ZCTA3', 'Geo_ZCTA5', 'Geo_SUBMCD', 'Geo_SDELM', 'Geo_SDSEC', 'Geo_SDUNI', 'Geo_UR', 'Geo_PCI', 'Geo_TAZ', 'Geo_UGA', 'Geo_BTTR', 'Geo_BTBG', 'Geo_PUMA5', 'Geo_PUMA1'] 
fileId = "R11897141_SL150"
convertCsvToJson("data/"+fileId+".csv","data/"+fileId+".json")