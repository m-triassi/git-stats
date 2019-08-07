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

    # Get Commits for passed username return as paginated lists
    @staticmethod
    def getCommits(username):
        user = g.get_user(username)
        repositories = user.get_repos()
        commits = []
        for repo in repositories:
            repoCommits = repo.get_commits()
            commits.append(repoCommits)
        print(commits)
        return commits

    # Extrapolate time of passed commit, in our standardized form
    @staticmethod
    def fetchTime(commit):
        return ""

    # Gather all the commit times for a given user
    # Uses getCommits and fetchTime
    @staticmethod
    def compileTimesForUser(username):
        commits = Driver.getCommits(username)
        times = []
        for commitList in commits:
            for commit in commitList:
                print(commit.commit.committer.name + " : " + str(commit.commit.committer.date))
                #times.append(commit.stats)
        return times

    @staticmethod
    def analyzeUsers(userList):
        # Iterate over userlist
        # Creates a file of users with their commit times
        return ""
