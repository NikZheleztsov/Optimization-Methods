from fractions import Fraction
import sys, getopt
from .table import *

num_of_variables = 0
needed_val = []
# if max then opt = 1 else opt = 0
verb = 0

def find_basic_solution(a, b, c):

    print('===========================')
    print('| Find the basic solution |')
    print('===========================')

    # Gauss method
    for i in range(len(a)):
        a[i].insert(0, b[i])
    a.append(c)

    # Making the columns
    columns = ['S_0']
    for i in range(1, num_of_variables + 1):
        columns.append('x_' + str(i))
    
    global needed_val
    needed_val = copy.deepcopy(columns[1:])

    # Making the rows
    rows = []
    for i in range(num_of_variables + 1, \
            num_of_variables + len(a)):
        rows.append('x_' + str(i))
    rows.append('F')

    table = Table(rows, columns, a)

    print('Initial table:')
    table.print()

    while(True):
        is_ok = True
        row = None
        for i in range(len(table.values) - 1):
            if table.values[i][0] < 0:
                is_ok = False
                row = i
                break

        if is_ok:
            print('Basic solution was found')
            break
    
        num_of_resolvent_column = table.find_res_column(row)
        print('Num of column to swap:', num_of_resolvent_column)
        if num_of_resolvent_column == None:
            print('Solution doesn\'t exist')
            sys.exit(0)
    
        num_of_resolvent_row = table.find_res_row(num_of_resolvent_column)
        print('Num of row to swap:', num_of_resolvent_row)
        print('')
        table.swap(num_of_resolvent_row, num_of_resolvent_column)
        print('Table (after swap):')
        table.print()

    return table

def optimize(table):

    print('\n\n===========================')
    print('|      Optimization       |')
    print('===========================')

    while(True):
        is_ok = True
        column = 0
        for i in range(1, len(table.values[0])): 
            if table.values[len(table.values) - 1][i] > 0:
                is_ok = False
                column = i
                break
    
        if is_ok:
            break 

        print('Num of column to swap:', column)
        for i in range(len(table.values) - 1):
            if table.values[i][column] > 0:
                is_ok = True
                break

        if not is_ok:
            print('Infinite number of solutions')
            sys.exit(0)

        row = table.find_res_row(column)
        print('Num of row to swap:', row)
        print('')
        table.swap(row, column)
        print('Table (after swap):')
        table.print()

    print('Optimization is done')
    return table

def get_solution(table, opt):

    if opt == 1:
        F = (-1) * table.values[len(table.values) - 1][0]
    else:
        F = table.values[len(table.values) - 1][0]

    solution = dict.fromkeys(needed_val, 0)
    for i in range(len(table.values) - 1):
        if table.rows[i] in needed_val:
            solution[table.rows[i]] = table.values[i][0]

    return F, solution

def parse(input_file):

    global num_of_variables
    opt = -1
    a, b, c = [], [], []

    with open(input_file, 'r') as file:
        content = file.readlines()
        del_char = [' ', '=', '[', ']', '\n']

        for line in content:

            # Comments in data file
            if (line.find('#') == 0):
                continue

            if line.find('max') != -1:
                opt = 1
                continue
            elif line.find('min') != -1:
                opt = 0
                continue
            
            for char in del_char:
                line = line.replace(char, '')

            if line.find('a') != -1:

                line = line.replace('a', '')
                numbers = line.split(',')
                if num_of_variables == 0:
                    print('Please add -n <num_of_vars> or put "c" \
in data.txt before "a"')
                    sys.exit()

                try:
                    for i in range(0, len(numbers) - 1, num_of_variables):
                        temp = []
                        for j in range(0, num_of_variables):
                            temp.append(Fraction(numbers[i + j]))
                        a.append(temp)

                except IndexError:
                    print('Incorrect -n value')
                    sys.exit(6)

            elif line.find('b') != -1:
                line = line.replace('b', '')
                numbers = line.split(',')
                for num in numbers:
                    b.append(Fraction(num))

            elif line.find('c') != -1:
                line = line.replace('c', '')
                numbers = line.split(',')
                for num in numbers:
                    c.append(Fraction(num))

                if num_of_variables == 0:
                    num_of_variables = len(c)

    # check data
    if opt == -1:
        print('Please, add "max" or "min" to data.txt')
        sys.exit(4)

    if len(c) != len(a[0]) or len(a) != len(b):
        print('Incorrect values. Check data.txt or -n parametr for mistakes ')
        sys.exit(5)
    
    # [5, 6, 1]
    # F = 5x_1 + 6x_2 + x_3
    # -> min: F = -(-5x_1 - 6x_2 - x_3)
    # -> max = -min(-F): -F = -(5x_1 + 6x_2 + x_3)

    # if min
    if opt == 0:
        for i in range(len(c)):
            c[i] = c[i] * (-1)

    return a, b, c, opt

def print_solution(F, solution, opt):

    print('\n\n===========================')
    print('|         Solution        |')
    print('===========================')

    min_or_max = ''
    if (opt == 0):
        min_or_max = 'min'
    else:
        min_or_max = 'max'

    print('{} value of F: {}'.format(min_or_max, F))
    for i in needed_val:
        print(i, solution[i])


def simplex_internal(a, b, c, opt):
    # Method returns simplex table 
    c.insert(0, 0)
    table = find_basic_solution(a, b, c)
    optimize(table)
    return get_solution(table, opt)

def main (argv):
    global opt, num_of_variables
    input_file, output_file = '', ''

    try:
        # args is empty
        opts, args = getopt.getopt(argv,"hvi:n:",["ifile=", "varnum="])
    except getopt.GetoptError:
        print ('core.py -i <inputfile>')
        sys.exit(2)

    for option, arg in opts:
        if option == '-h':
            print ('simplex.py -i <inputfile> (-n <num_of_variables>)')
            sys.exit()
        elif option in ("-i", "--ifile"):
            input_file = arg
        elif option in ("-n", "--varnum"):
            num_of_variables = int(arg)

    if input_file == '':
        print('Please, add input file:')
        print ('    simplex.py -i <inputfile>')
        sys.exit()

    a, b, c, opt = parse(input_file)
    F, solution = simplex_internal(copy.deepcopy(a), copy.deepcopy(b), \
            copy.deepcopy(c), opt)
    print_solution(F, solution, opt)

    return a, b, c, opt

if __name__ == "__main__":
    main(sys.argv[1:])

