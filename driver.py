from datetime import datetime, timedelta
from github import Github
from pytz import timezone
from timezonefinder import TimezoneFinder

import csv
import geocoder
import json
import os
import pytz
import requests
import settings
import string


token = os.getenv("GIT_ACCESS_TOKEN")
g = Github(token)

class Driver(object):

    # Create a json file of target github users
    @staticmethod
    def findUsers():
        print(g.get_user().created_at)
        start = g.get_user().id
        endpoint = "https://api.github.com/users?"
        results = []
        for x in range(1, int(os.getenv("PAGE_COUNT"))):
            pageJump = x*int(os.getenv("JUMP_INTERVAL"))
            since = start+pageJump
            r = requests.get(endpoint + "since="+str(since), headers={'Authorization': 'token ' + token})
            users = json.loads(r.text)
            for user in users:
                results.append(user["login"])
                print(user["login"]+" added!")
            #print(json.dumps(json.loads(r.text) ,sort_keys=True, indent=4))
        with open(os.getenv("USERNAME_FILE"), 'w') as f:
            json.dump(results, f, sort_keys=True, indent=4)
        return 0

    # # Get Events for passed username return as paginated lists
    # @staticmethod
    # def getEvents(username):
    #     user = g.get_user(username)
    #     events = user.get_events()
    #     return events

    # Extrapolate time of passed event, in their local timezone
    # Achieves this by trying to determine their time zone via location
    @staticmethod
    def fetchTimezone(location):
        tf = TimezoneFinder()
        geo = geocoder.osm(location, maxRows=1)
        lat = geo.lat
        lng = geo.lng
        userTz = tf.timezone_at(lat=lat, lng=lng)
        return userTz

    @staticmethod
    def convertTime(time, toTz):
        utcDt = time.replace(tzinfo=pytz.utc)
        targetTz = timezone(toTz)
        targetTime = targetTz.normalize(utcDt.astimezone(targetTz))
        return targetTime

    # Gather all the event times for a given user
    @staticmethod
    def compileTimesForUser(username):
        user = g.get_user(username)
        if user.location == None:
            return False
            pass
        events = user.get_events()
        times = []
        eventTypes = []
        tz = Driver.fetchTimezone(user.location)
        for event in events:
            times.append(Driver.convertTime(event.created_at, tz))
            eventTypes.append(event.type)
        return times, eventTypes

    # Iterate over userlist
    # Creates a file of users with their commit times
    @staticmethod
    def analyzeUsers():
        fmt = "%d/%m/%Y %H:%M%S"
        data = [["username", "event_type", "event_timestamp", "timezone"]]
        users = json.loads(open(os.getenv("USERNAME_FILE")).read())
        for user in users:
            times, types = Driver.compileTimesForUser(user)
            if times != False:
                i = 0
                for time in times:
                    data.append([user, types[i], time, time.tzinfo])
                    i += 1
                pass
        with open(os.getenv("USER_DATA_FILE"), 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(data)
        return 0
