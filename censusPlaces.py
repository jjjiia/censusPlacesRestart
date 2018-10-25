import tweepy
import os
import oauth2, time, urllib, urllib2, json
from functools import partial
import random
import pprint
import csv
import math
import json
from math import radians, cos, sin, asin, sqrt
from shapely.geometry import *
from shapely.ops import cascaded_union
from operator import itemgetter
import time
from datetime import datetime
# Authentication details. To  obtain these visit dev.twitter.com
consumer_key = 'VeJ1NTd94reHZ7ENSrT7vgUWh'
consumer_secret = 'NOfEPy56DFJcaeRhPQEG7W8wgnGwXprnvIERy2NWyjDJgKyjBN'
access_token = '3332909505-5xSBQF1Qxu6FlfGAOKprk9ym6rTeKKyfkHZKPW2'
access_token_secret = 'bbqj0YF97GgT3V0hCH9vIUzppGxBZ0sN3cuu4OkpmHaWh'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#step 1, get census area id by running shapely loop
def getId(lng,lat):
    point = Point(float(lng),float(lat))
    print point
    with open("data/newYorkState_noWater.geojson") as f:
        js =json.load(f)
        for i in range(len(js['features'])):
            feature = js['features'][i]            
            uid = feature["properties"]["GEOID"]
            polygon = shape(feature['geometry'])
           # print uid
            if polygon.contains(point)==True:
                return uid
				
		
#step 2 get data of the census geo id from file
def getData(bgid):
    #all data for area is loaded
    dataByIdFile = open("data/R11891292_SL150.json")
    dataById =json.load(dataByIdFile)
    
    #data for this id is:
    currentData = dataById[bgid]
    
    #the selected categories are loaded
    dataDictionarySelectedFile = open("data/R11891292_data_dictionary_selected.json")
    dataDictionarySelected = json.load(dataDictionarySelectedFile)
    
    tweetString = ""
    for key in dataDictionarySelected:
        keyTerm = dataDictionarySelected[key]
        value = currentData[key]
        if value!="" and value!="0":
            tweetString += str(keyTerm)+":"+str(value)+"/"
    print len(tweetString)
    return tweetString
         


# constantly listens for tweets @censusPlaces and gets the coordinates from tweet to get census data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format
        decoded = json.loads(data)
        #print decoded
        #the fields are: user, userid, and user location
        #coordinates = decoded["coordinates"]["coordinates"]
        user = decoded['user']['screen_name']
        userId = decoded["id"]
        print userId,user
		
        #if the coordinates are empty, then prompt user to turn on exact location
        if user!="censusPlaces":
            if decoded["coordinates"] == None:
                message = "@"+user+" share precise location is not enabled on your tweet. Please turn it on at bottom of screen and try again."
                api.update_status(message,userId)
            else:
                if decoded["coordinates"]["coordinates"]==None:
                    message = "@"+user+" 2 share precise location is not enabled on your tweet. Please turn it on at bottom of screen and try again."
                    api.update_status(message,userId)
                else:
                    #if the coordinates are ok, then get the id
                    coordinates = decoded["coordinates"]["coordinates"]
                    lng = coordinates[0]
                    lat = coordinates[1]
                    bgid = getId(lng,lat)
                    if bgid == None:
                        message = "@"+user+" i'm so sorry, i don't think you are in nyc and i didn't upload that data yet :("
                        api.update_status(message,userId)
                    else:
                        sentence = getData(bgid)
                        message = "@"+user+" "+sentence
                        if len(message)>280:
                            message = message[0:270]+"..."
                        api.update_status(message,userId)
            
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print message
        #print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ''
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    
   #gid = getId(-73.960604,40.808534)
   #print gid
   #

    
    
    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['@censusPlaces'])
    

