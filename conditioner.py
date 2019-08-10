import json
import os
import random
import settings
import string


class Conditioner(object):

    @staticmethod
    def reduceList():
        target = os.getenv("USERNAME_FILE")
        desiredSize = int(os.getenv("MAX_LIST_SIZE"))
        file = json.loads(open(target).read())
        results = random.sample(file, desiredSize)
        destination = target.replace(".json", "_reduced.json")

        with open(destination, 'w') as f:
            json.dump(results, f, sort_keys=True, indent=4)
        pass


    pass
