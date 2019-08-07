import requests
import os
import string
import json
import settings

from github import Github

class Driver(object):

    def __init__():
        g = Github(os.getenv("GIT_ACCESS_TOKEN"))

    @staticmethod
    def findUsers():
        endpoint = "https://api.github.com/users?"
        print(endpoint)
        # Create a json file of target github users
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
