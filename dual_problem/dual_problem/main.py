import simplex.simplex as simplex
import simplex.table as table
import numpy as np
import sys, copy

def get_dual_problem(a, b, c, opt):
    a = (np.array(a).transpose()) * (-1)
    c, b =  b, [ j * (-1) for j in c ]

    # if max
    if opt == 1:
        opt = 0
        c = [i * (-1) for i in c]

    return a.tolist(), b, c, opt


def main (argv):
    print('===========================')
    print('||     Direct problem    ||')
    print('===========================\n')
    a, b, c, opt = simplex.main(argv)
    a, b, c, opt = get_dual_problem(a, b, c, opt)

    print('\n\n===========================')
    print('||      Dual problem     ||')
    print('===========================\n')
    F, solution = simplex.simplex_internal(copy.deepcopy(a), \
            copy.deepcopy(b), copy.deepcopy(c), opt)
    simplex.print_solution(F, solution, opt)

if __name__ == "__main__":
    main(sys.argv[1:])
