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

        self.values = self.get_values_from_json(json)
        self.vectors = self.get_vectors_for_values()
        print(self.values, self.vectors)

    def get_json_of_response(self) -> dict:
        appid = os.getenv('WA_APPID', key)

        query = urllib.parse.quote_plus(self.build_equation())
        query_url = f"http://api.wolframalpha.com/v2/query?" \
                    f"appid={appid}" \
                    f"&input={query}" \
                    f"&includepodid=Result" \
                    f"&output=json"

        return requests.get(query_url).json()

    def build_equation(self) -> str:
        matrix = ""
        # some building logics
        return f"determinator {matrix} = 0"

    def get_values_from_json(self, json) -> list:
        # parsing magic
        return list()

    def get_vectors_for_values(self) -> list:
        # gauss stuff
        return list()
