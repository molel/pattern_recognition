import numpy.linalg

from Obj import Obj


class Class:
    def __init__(self, filename: str):
        self.name = filename.replace(".txt", "")
        self._objs: list = get_objects(filename)
        self._rows: int = len(self._objs[0])
        self._columns: int = len(self._objs[0][0])
        self._elements: int = self._rows * self._columns
        self._core: list = self.get_core()
        self._cov: list = self.get_cov()
        self._inv_cov = self.get_inv_cov()

    @property
    def size(self) -> int:
        return len(self._objs)

    def __str__(self) -> str:
        result = self.name + "\n"
        for i in range(self.size):
            result += f"Object #{i}\n{self._objs[i]}\n"
        result += f"Class core\n{self.matrix_ro_str(self._core)}"
        return result

    def get_core(self) -> list:
        core: list = list()
        for i in range(self._rows):
            row: list = []
            for j in range(self._columns):
                number: int = 0
                for k in range(self.size):
                    number += self._objs[k][i][j]
                row.append(number / self._elements)
            core.append(row)
        return core

    def get_cov(self) -> list:
        cov: list = [[1 / (self.size - 1) for _ in range(self._elements)] for _ in range(self._elements)]
        for i in range(self._elements):
            for j in range(self._elements):
                real_i_for_i: int = i // self._columns
                real_j_for_i: int = i % self._columns
                real_i_for_j: int = j // self._columns
                real_j_for_j: int = j % self._columns
                number: int = 0
                for k in range(self.size):
                    number += (self._objs[k][i // self._columns][i % self._columns] - self._core[i // self._columns][
                        i % self._columns]) * \
                              (self._objs[k][j // self._columns][j % self._columns] - self._core[j // self._columns][
                                  j % self._columns])
                cov[i][j] *= number
                if i == j:
                    cov[i][j] += 1
        return cov

    def get_inv_cov(self) -> list:
        # E = [[0 for _ in range(self._elements)] for _ in range(self._elements)]
        # for i in range(self._elements):
        #     E[i][i] = 1
        #
        # for k in range(self._elements):
        #     temp = self._cov[k][k]
        #     for i in range(self._elements):
        #         self._cov[k][i] /= temp
        #         E[k][i] /= temp
        #     for i in range(k + 1, self._elements):
        #         temp = self._cov[i][k]
        #         for j in range(self._elements):
        #             self._cov[i][j] -= self._cov[k][j] * temp
        #             E[i][j] -= E[k][j] * temp
        #
        # for k in range(self._elements - 1, 0, -1):
        #     for i in range(k - 1, -1, -1):
        #         temp = self._cov[i][k]
        #         for j in range(self._elements):
        #             self._cov[i][j] -= self._cov[k][j] * temp
        #             E[i][j] -= E[k][j] * temp
        #
        # for i in range(self._elements):
        #     for j in range(self._elements):
        #         self._cov[i][j] = E[i][j] if abs(E[i][j]) == 1 else 0
        # return self._cov
        return numpy.linalg.inv(self._cov).tolist()

    def matrix_ro_str(self, matrix: list, delimiter: str = "   ") -> str:
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
        return max([len(str(matrix[row][column])) for row in range(len(matrix))])

    def find_distance(self, obj: Obj) -> float:

        difference = list()
        for i in range(self._rows):
            for j in range(self._columns):
                difference.append(obj[i][j] - self._core[i][j])

        Y = list()
        for i in range(self._elements):
            s = 0
            for j in range(self._elements):
                s += difference[j] * self._inv_cov[i][j]
            Y.append(s)

        final = 0
        for i in range(self._elements):
            final += Y[i] * difference[i]

        from math import sqrt
        final = sqrt(final)
        return final
        # # находим (x - y)^T, т.к. в чистом виде координаты x не понадобятся
        # difference: list = copy(obj)
        # for i in range(self._rows):
        #     for j in range(self._columns):
        #         difference[i][j] -= self._core[i][j]
        #
        # # умножаем вектор на матрицу, чтобы получить вектор (x-y)^T * S^(-1)
        # Y: list = list()
        # for i in range(self._elements):
        #     s: float = 0
        #     for j in range(self._elements):
        #         s += difference[j // self._columns][j % self._columns] * self._cov[i][j]
        #     else:
        #         Y.append(s)
        #
        # # находим (x-y)^T * S^(-1) * (x-y)
        # final: float = 0
        # for i in range(self._rows):
        #     for j in range(self._columns):
        #         final += Y[i * 10 + j] * self._cov[i][j]
        # else:
        #     from math import sqrt
        #     final = sqrt(final)
        # return final


def get_objects(filename: str):
    with open(filename, "r") as file:
        obj = list()
        result = list()
        for row in file:
            if row == "\n":
                result.append(Obj(obj.copy()))
                obj.clear()
            else:
                obj.append([int(el) for el in row[:-1]])
        else:
            result.append(Obj(obj.copy()))
        return result
