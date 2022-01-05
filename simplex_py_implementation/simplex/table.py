import copy
import pandas

class Table:
    def __init__(self, rows, columns, values):
        self.rows = rows
        self.columns = columns
        self.values = values

    def print(self):
        out = pandas.DataFrame(self.values, self.rows, self.columns)
        print(out)
        print('')

    def swap(self, row, column):
        self.rows[row], self.columns[column] = \
                self.columns[column], self.rows[row]
        old_values = copy.deepcopy(self.values)
        
        # Разрешающая строка
        for i in range(len(self.values[0])):
            self.values[row][i] = old_values[row][i] / old_values[row][column]

        # Разрешающий столбец
        for i in range(len(self.values)):
            self.values[i][column] = (-1) * \
                    old_values[i][column] / old_values[row][column]

        # Разрешающий элемент
        self.values[row][column] = 1 / old_values[row][column] 

        for i in range(len(old_values)):
            if i != row:
                for j in range(len(old_values[0])):
                    if j != column:
                        self.values[i][j] = old_values[i][j] - old_values[i][column] * \
                                old_values[row][j] / old_values[row][column]

    # Поиск разрешающего столбца
    def find_res_column(self, row):
        num_of_resolvent_column = None
        for i in range(1, len(self.values[0])):
            if self.values[row][i] < 0:
                return i
        return num_of_resolvent_column

    # Поиск разрешающей строки
    def find_res_row(self, column):
        row = None
        min_value = float('inf')
        for i in range(len(self.values) - 1):

            if self.values[i][column] == 0: 
                continue

            val = self.values[i][0] / self.values[i][column]
            if val < min_value and val > 0:
                min_value = val
                row = i
        return row

