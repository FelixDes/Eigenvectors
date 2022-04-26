class MatrixSolver:  # Класс для выполнения математических операций (model)

    def __init__(self, left_values, right_values):
        self.left_values = left_values
        self.right_values = right_values

    # Метод обратной матрицы
    def solve_for_opposite_matrix_method(self):
        if self.get_det(self.left_values) == 0:
            return [[0] for _ in range(len(self.left_values))]
        return self.multiply(self.get_opposite_table(self.left_values), self.right_values)

    # Метод Крамера
    def solve_for_kramer_method(self):
        if self.get_det(self.left_values) == 0:
            return [[0] for _ in range(len(self.left_values))]
        lst = list()
        det = self.get_det(self.left_values)
        for i in range(len(self.left_values[0])):
            lst.append([self.get_det(self.get_matrix_for_kramer(i)) / det])
        return lst

    # Получаем матрицу, состающую из левой, в которой на место столбца index поставлена правая матрица
    def get_matrix_for_kramer(self, index):
        lst = list(list())
        for i in range(len(self.left_values)):
            sub_lst = list()
            for j in range(len(self.left_values[0])):
                if j == index:
                    sub_lst.append(self.right_values[i][0])
                else:
                    sub_lst.append(self.left_values[i][j])
            lst.append(sub_lst)
        return lst

    # Метод Гаусса
    def solve_for_gauss_method(self):
        res = [[0] for _ in range(len(self.left_values))]
        if self.get_det(self.left_values) == 0:
            return res
        # Приводим матрицу к верхнедиагональному виду
        for i in range(len(self.left_values)):
            for j in range(i + 1, len(self.left_values)):
                self.make_zero_started_string(i, j, i)

        res[len(self.left_values) - 1][0] = self.right_values[len(self.left_values) - 1][0] / \
                                            self.left_values[len(self.left_values) - 1][len(self.left_values) - 1]

        for i in range(len(self.left_values) - 2, -1, -1):
            for j in range(i + 1, len(self.left_values)):
                self.right_values[i][0] -= self.left_values[i][j] * res[j][0]
            res[i][0] = self.right_values[i][0] / self.left_values[i][i]
        return res

    # Приводим строку с индексом i2 к нулям с индекса j складывая со строкой i1 с коефициентом
    def make_zero_started_string(self, i1, i2, j):
        if self.left_values[i2][j] != 0:
            coef = -self.left_values[i1][j] / self.left_values[i2][j]
            self.right_values[i2][0] = self.right_values[i2][0] * coef + self.right_values[i1][0]
            for i in range(j, len(self.left_values)):
                self.left_values[i2][i] = self.left_values[i2][i] * coef + self.left_values[i1][i]

    # Умножение матриц
    @staticmethod
    def multiply(table1, table2):
        result_matrix = [[0 for _ in range(len(table2[0]))] for _ in range(len(table1))]
        for i in range(len(table1)):
            for j in range(len(table2[0])):
                for k in range(len(table2)):
                    result_matrix[i][j] += table1[i][k] * table2[k][j]
        return result_matrix

    # Получить матрицу без ряда i_n и строки j_n
    @staticmethod
    def get_table_no_point(input_table, i_n, j_n):
        table_res = []
        for i in range(len(input_table) - 1):
            table_row = []
            for j in range(len(input_table) - 1):
                table_row.append(input_table[i if i < i_n else i + 1][j if j < j_n else j + 1])
            if bool(table_row):
                table_res.append(table_row)
        return table_res

    # Транспонирование матрицы
    def reverse(self, input_table):
        table_res = []
        for i in range(len(input_table)):
            table_row = []
            for j in range(len(input_table)):
                table_row.append(input_table[j][i])
            table_res.append(table_row)
        return table_res

    # Найти определитель матрицы
    def get_det(self, input_table):
        if len(input_table) == 1:
            return input_table[0][0]
        sum = 0
        for i in range(len(input_table)):
            sum += input_table[i][0] * (-1 if i % 2 != 0 else 1) * self.get_det(
                self.get_table_no_point(input_table, i, 0))
        return sum

    # найти обратную матрицу
    def get_opposite_table(self, input_table):
        input_table = self.reverse(input_table)
        table_res = []
        det = self.get_det(input_table)
        for i in range(len(input_table)):
            table_row = []
            for j in range(len(input_table)):
                table_row.append(
                    (-1 if (i + j) % 2 != 0 else 1) * self.get_det(self.get_table_no_point(input_table, i, j)) / det)
            table_res.append(table_row)
        return table_res
