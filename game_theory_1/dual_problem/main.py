import simplex.simplex as simplex
import simplex.table as table
import numpy as np
import sys, copy, getopt
from fractions import Fraction

# Parsing of the input file
def parse(input_file, num_of_variables):

    a = []
    with open(input_file, 'r') as file:
        content = file.readlines()[0]
        del_char = [' ', '=', '[', ']', '\n']
        for char in del_char:
            content = content.replace(char, '')

        numbers = content.split(',')
        if num_of_variables == 0:
            print('Please add -n <num_of_vars> or put "c" in data.txt before "a"')
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

    return a, len(a)

def get_simplex_for_player_A(input_matrix):
    c = [1 for _ in range(len(input_matrix))]
    b = [-1 for _ in range(len(input_matrix[0]))]
    a = []

    for j in range(len(input_matrix[0])):
        temp = []
        for i in range(len(input_matrix)):
            temp.append(input_matrix[i][j] * (-1))
        a.append(temp)

    return a, b, c, 0

def get_dual_problem(a, b, c, opt):
    a = (np.array(a).transpose()) * (-1)
    b, c = c, [i * (-1) for i in b]
    opt = 0 if opt == 1 else 1
    return a.tolist(), b, c, opt, len(a[0])

def get_solution(F, solut, num):
    g = Fraction(1 / F)
    opt_strat = [i * g for i in solut]

    print("Optimal mixed strategy:")
    for j in opt_strat:
        print(j)

    print()

def main (argv):

    num_of_variables = 0;
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


    print('=====================================================')
    print('=                   PLAYER A                        =')
    print('=====================================================')
    print('----              NAKED SIMPLEX                  ----')
    input_matrix, variables_num = parse(input_file, num_of_variables)
    a, b, c, opt = get_simplex_for_player_A(input_matrix)
    F_1, solut_1 = simplex.simplex_internal(copy.deepcopy(a), \
                                            copy.deepcopy(b), copy.deepcopy(c),
                                            opt, variables_num)
    final_solut_1 = simplex.print_solution(F_1, solut_1, opt)
    print('-----------------------------------------------------')
    get_solution(F_1, final_solut_1, len(input_matrix))

    print('=====================================================')
    print('=                   PLAYER B                        =')
    print('=====================================================')
    print('----              NAKED SIMPLEX                  ----')
    a_2, b_2, c_2, opt_2, num_2 = get_dual_problem(a, b, c, opt)
    F_2, solut_2 = simplex.simplex_internal(copy.deepcopy(a_2), \
                                            copy.deepcopy(b_2),
                                            copy.deepcopy(c_2), opt_2, num_2)
    final_solut_2 = simplex.print_solution(F_2, solut_2, opt_2)
    print('-----------------------------------------------------')
    get_solution(F_2, final_solut_2, len(input_matrix))

    # Checking the solution
    assert F_1 == F_2
    sum_1, sum_2 = 0, 0;
    for i in final_solut_1:
        sum_1 += i / F_1

    for i in final_solut_2:
        sum_2 += i / F_2

    assert sum_1 == sum_2 == 1
    print("Assertion passed")

    print('=====================================================')
    print('=                   SUMMARY                         =')
    print('=====================================================')
    print("Game cost:", Fraction(1 / F_1))
    print("Player A: [", end="")
    for a in final_solut_1:
        if a != final_solut_1[-1]:
            print(a / F_1, end = ", ")
        else:
            print(a / F_1, end = "")
    print("]")

    print("Player B: [", end="")
    for a in final_solut_2:
        if a != final_solut_2[-1]:
            print(a / F_2 , end = ", ")
        else:
            print(a / F_2, end = "")

    print("]")


if __name__ == "__main__":
    main(sys.argv[1:])
