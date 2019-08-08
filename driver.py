import requests
import os
import string
import json
import settings

from timezonefinder import TimezoneFinder
from github import Github
from geopy import  geocoders
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
    def fetchTime(event, location):
        if location == "None":
            return ""
            pass
        tf = TimezoneFinder()
        geo = geocoders.GoogleV3()
        location, (lat, lng) = geo.geocode(location)
        timezone = tf.timezone_at(lat=lat, lng=lng)
        print(timezone)

    # Gather all the event times for a given user
    # Uses getEvents and fetchTime
    @staticmethod
    def compileTimesForUser(username):
        user = g.get_user(username)
        events = user.get_events()
        times = []
        for event in events:
            Driver.fetchTime(event, user.location)
        return times

    @staticmethod
    def analyzeUsers(userList):
        # Iterate over userlist
        # Creates a file of users with their commit times
        return ""
