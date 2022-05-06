import os
import urllib
import re

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

        list_of_equations = self.get_equations_from_json(json)
        equation = self.select_equation(list_of_equations)
        roots = self.split_equation_for_roots(equation)
        self.set_values(roots)
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

        # print(str(requests.get(query_url).json()).replace('\'', '\"'))
        return requests.get(query_url).json()

    def build_equation(self) -> str:
        size = len(self.matrix)
        if size == 1:
            raise Exception("Can not parse matrix for one element")
        matrix = "{"
        for i in range(size):
            matrix += "{"
            for j in range(size):
                matrix += str(self.matrix[i][j])
                if i == j:
                    matrix += "-x"
                if j != size - 1:
                    matrix += ","
            matrix += "}"
            if i != size - 1:
                matrix += ","
        matrix += "}"
        return f"determinant {matrix} = 0"

    def get_equations_from_json(self, json):
        res = list()
        for block in json["queryresult"]["pods"][3]["subpods"]:
            res.append(block["plaintext"])
        return res

    def select_equation(self, equations) -> str:
        for eq in equations:
            if re.fullmatch("\-?((\(x[+\-]\d+(.\d*)?\))(\^\d+)?)+=0", eq.replace(' ', '')):
                return eq
        raise Exception("Some of the roots are not real")

    def split_equation_for_roots(self, equation) -> dict:
        return {float(i.split("^")[0].replace(" ", "").replace("x", "")) * -1: 1 if i.find("^") == -1 else int(
            i.split("^")[-1]) for i in
                equation.replace("-(", "").replace(" (", "|").replace("(", "").replace(")", "").split(" =")[0].split(
                    "|")}

    def set_values(self, roots):
        self.values = list()
        for k in roots.keys():
            for _ in range(int(roots.get(k))):
                self.values.append(k)

    def set_vectors_for_values(self) -> list:
        self.vectors = list()
        # math stuff
        self.vectors = ["vector0", "vector0", "vector0", "vector0", "vector0", "vector0", "vector0", "vector0"]

    def get_rank(self, m):
        matrix = m.copy()
        rank = len(matrix)
        for row in range(rank):
            if matrix[row][row]:
                for col in range(len(matrix)):
                    if col != row:
                        mult = matrix[col][row] / matrix[row][row]
                        for i in range(rank):
                            matrix[col][i] -= mult * matrix[row][i]
            else:
                reduce = True
                for i in range(row + 1, len(matrix)):
                    if (matrix[i][row]):
                        matrix[row][rank], matrix[i][rank] = matrix[i][rank], matrix[row][rank]
                        reduce = False
                        break
                if reduce:
                    rank -= 1
                    for i in range(len(matrix)):
                        matrix[i][row] = matrix[i][rank]
                row -= 1
        return rank
