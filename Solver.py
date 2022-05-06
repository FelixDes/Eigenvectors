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
        self.set_vectors(roots)
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

    def set_vectors(self) -> list:

        for e_val in self.values:
            matrix = self.matrix.copy()
            for i in range(len(self.matrix)):
                matrix[i][i] -= e_val
            self.vectors.append(self.solve_for_gauss_method(matrix, self.get_rank(matrix)))

    def get_rank(self, matrix):
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
                    if matrix[i][row]:
                        matrix[row][rank], matrix[i][rank] = matrix[i][rank], matrix[row][rank]
                        reduce = False
                        break
                if reduce:
                    rank -= 1
                    for i in range(len(matrix)):
                        matrix[i][row] = matrix[i][rank]
                row -= 1
        return rank

    def solve_for_gauss_method(self, matrix, rank):
        matrix = sorted(matrix, reverse=True)

        for i in range(len(matrix)):
            for j in range(i + 1, len(matrix)):
                if matrix[j][i] != 0:
                    coef = -matrix[i][i] / matrix[j][i]
                    for k in range(i, len(matrix)):
                        matrix[j][k] = matrix[j][k] * coef + matrix[i][k]

        vectors = list()

        for rank_i in range(len(matrix) - rank):
            res = [[0] for _ in range(len(matrix))]
            right_values = [[0] for _ in range(len(matrix))]

            for i in range(len(matrix) - rank):
                res[len(matrix) - 1 - i][0] = 1 if rank_i == i else 0

            for i in range(len(matrix) - 1 - (len(matrix) - rank), -1, -1):
                for j in range(i + 1, len(matrix)):
                    right_values[i][0] -= matrix[i][j] * res[j][0]
                res[i][0] = right_values[i][0] / matrix[i][i]
            vectors.append(res.copy())
        return vectors
