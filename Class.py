import numpy.linalg

from Pattern import *


class Class:
    def __init__(self, filename: str):
        self.name = filename.replace(".txt", "")
        self._patterns: list = get_patterns(filename)
        self._rows: int = len(self._patterns[0])
        self._columns: int = len(self._patterns[0][0])
        self._elements: int = self._rows * self._columns
        self._core: list = self.get_core()
        self._cov: list = self.get_cov()
        self._inv_cov = self.get_inv_cov()

    @property
    def size(self) -> int:
        return len(self._patterns)

    def __str__(self) -> str:
        result = self.name + "\n"
        for i in range(self.size):
            result += f"Pattern #{i}\n{self._patterns[i]}\n"
        else:
            result += f"Class core\n{self.matrix_to_str(self._core)}"
        return result

    def get_core(self) -> list:
        core: list = list()
        for i in range(self._rows):
            row: list = []
            for j in range(self._columns):
                number: int = 0
                for k in range(self.size):
                    number += self._patterns[k][i][j]
                else:
                    row.append(float('{:.5f}'.format(number / self.size)))
            else:
                core.append(row)
        return core

    def get_cov(self) -> list:
        cov: list = [[1 / (self.size - 1) for _ in range(self._elements)] for _ in range(self._elements)]
        for i in range(self._elements):
            for j in range(self._elements):
                number: int = 0
                for k in range(self.size):
                    number += (self._patterns[k][i // self._columns][i % self._columns] -
                               self._core[i // self._columns][
                                   i % self._columns]) * \
                              (self._patterns[k][j // self._columns][j % self._columns] -
                               self._core[j // self._columns][
                                   j % self._columns])
                else:
                    cov[i][j] *= number
                if i == j:
                    cov[i][j] += 1
        return cov

    def get_inv_cov(self) -> list:
        return numpy.linalg.inv(numpy.array(self._cov)).tolist()

    def matrix_to_str(self, matrix: list, delimiter: str = "   ") -> str:
        columns_width: list = [self.get_column_width(matrix, column) for column in range(len(matrix[0]))]
        result: str = ""
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                result += " " * (columns_width[j] - len(str(matrix[i][j]))) + str(matrix[i][j]) + delimiter
            else:
                result += "\n"
        else:
            result += "\n"
        return result

    @staticmethod
    def get_column_width(matrix: list, column: int) -> int:
        return max(
            [len(str(matrix[row][column])) for row in range(len(matrix))])  # перебираем все элементы столбца column

    def find_distance(self, pattern: Pattern) -> float:
        difference: list = list()
        for i in range(self._rows):
            row = list()
            for j in range(self._columns):
                row.append(pattern[i][j] - self._core[i][j])
            difference.append(row)
        difference: list = numpy.transpose(numpy.array(difference)).tolist()
        Y = list()
        for i in range(self._elements):
            s = 0
            for j in range(self._elements):
                s += difference[j // self._rows][j % self._rows] * self._inv_cov[i][j]
            Y.append(s)
        final = 0
        for i in range(self._elements):
            final += Y[i] * difference[i // self._rows][i % self._rows]

        from math import sqrt
        final = sqrt(final)
        return final


def get_patterns(filename: str):
    with open(filename, "r") as file:
        pattern = list()
        result = list()
        for row in file:
            if row == "\n":
                result.append(Pattern(pattern.copy()))
                pattern.clear()
            else:
                pattern.append([int(el) for el in row[:-1]])
        else:
            result.append(Pattern(pattern.copy()))
        return result
