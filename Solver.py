import os
import urllib

import requests

with open("key.txt", "r") as key_file:
    key = key_file.readline()


class Solver:
    def __init__(self):
        self.matrix = list()

        self.values = list()
        self.vectors = list()

    def solve(self, matrix):
        self.matrix = matrix

        json = self.get_json_of_response()

        self.set_values_from_json(json)
        self.set_vectors_for_values()
        print(self.values, self.vectors)

    def get_json_of_response(self) -> dict:
        appid = os.getenv('WA_APPID', key)

        query = urllib.parse.quote_plus(self.build_equation())
        query_url = f"http://api.wolframalpha.com/v2/query?" \
                    f"appid={appid}" \
                    f"&input={query}" \
                    f"&podstate=Solutions" \
                    f"&output=json"

        return requests.get(query_url).json()

    def build_equation(self) -> str:
        matrix = "{{3-x,2,4}, {3,5-x,8}, {1,4,2-x}}"
        # some building logics
        return f"determinant {matrix} = 0"

    def set_values_from_json(self, json) -> list:
        print(str(json).replace('\'', '\"'))
        # parsing magic
        self.values = ["val0", "val1", "val2"]

    def set_vectors_for_values(self) -> list:
        # gauss stuff
        self.vectors = ["vector0", "vector1", "vector2"]
