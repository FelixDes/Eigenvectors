import ast
import json
import os
import urllib
import re

import requests
from PyQt6 import QtCore, QtWidgets

from py4j.java_gateway import JavaGateway

from InfoWidget import InfoWidget
from Exceptions import *

with open("key.txt", "r") as key_file:
    key = key_file.readline()


class Solver:
    def __init__(self, matrix):
        self.matrix = matrix

        self.result = dict()

    def solve(self):
        json = self.get_json_of_response()

        list_of_equations = self.get_equations_from_json(json)

        equation = self.select_equation(list_of_equations)

        roots = self.split_equation_for_roots(equation)

        self.set_result_for_roots(roots)

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
        size = len(self.matrix)
        if size == 1:
            raise IncorrectMatrixException()
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

    def select_equation(self, equations: list) -> str:
        for eq in equations:
            if re.fullmatch("\-?(x(\^\d+)?)?((\(x[+\-]\d+(.\d*)?\))(\^\d+)?(x(\^\d+)?)?)*=0", eq.replace(' ', '')):
                return eq
        raise ComplexRootsException()

    def split_equation_for_roots(self, equation: str) -> dict:
        print(equation)
        return {float(i.split("^")[0].replace(" ", "").replace("x", "")) * -1: 1 if i.find("^") == -1 else int(
            i.split("^")[-1]) for i in
                equation.replace("-(", "").replace(" (", "|").replace("(", "").replace(")", "").split(" =")[0].split(
                    "|")}

    # def set_values(self, roots):
    #     self.values = list()
    #     for k in roots.keys():
    #         for _ in range(int(roots.get(k))):
    #             self.values.append(k)

    def set_result_for_roots(self, roots: dict):
        self.get_data_for_gateway(roots)

    def get_data_for_gateway(self, roots):
        gateway = JavaGateway()

        java_matrix = gateway.new_array(gateway.jvm.java.lang.Double, len(self.matrix), len(self.matrix[0]))
        java_map = gateway.jvm.java.util.HashMap()

        for item in roots.items():
            java_map.put(item[0], item[1])

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                java_matrix[i][j] = float(self.matrix[i][j])

        response = gateway.entry_point.getResponseForMatrix(java_matrix, java_map)

        self.result = ast.literal_eval(str(response.getEVectors().toString()).replace("=", " : "))
