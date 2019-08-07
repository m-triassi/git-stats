import requests
import os
import string
import json
import settings

from github import Github
token = os.getenv("GIT_ACCESS_TOKEN")
g = Github(token)

class Driver(object):

    # Create a json file of target github users
    @staticmethod
    def findUsers():
        print(g.get_user().created_at)
        start = g.get_user().id
        endpoint = "https://api.github.com/users?"
        response = requests.get(endpoint + "since="+str(start), headers={'Authorization': 'token ' + token})
        print(json.dumps(json.loads(response.text) ,sort_keys=True, indent=4))
        return ""

    @staticmethod
    def getCommits(user):
        # Get Commits for passed username
        return ""

    @staticmethod
    def fetchTime(commit):
        # Extrapolate time of passed commit, in our standardized form
        return ""

    @staticmethod
    def compileTimesForUser(user):
        # Gather all the commit times for a given user
        # Uses getCommits and fetchTime
        return ""

    @staticmethod
    def analyzeUsers(userList):
        # Iterate over userlist
        # Creates a file of users with their commit times
        return ""
