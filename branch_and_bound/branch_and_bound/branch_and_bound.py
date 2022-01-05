import simplex.simplex as sm
import simplex.table as tb
import binarytree as bt
from copy import deepcopy
import sys, getopt
from fractions import Fraction
import numpy as np

class Value:
    def __init__(self, F, solution):
        self.F = F
        self.solution = solution
        
    def __str__(self):
        str = "F = % s\n" % (self.F)
        for ind, key in enumerate(self.solution.keys()): 
            str += "{}:{}   ".format(key, self.solution[key]) 
            if (ind + 1) % 2 == 0:
                str += '\n'
        return str
    
    def get_float(self):
        for val in self.solution.items():
            if not float(val[1]).is_integer():
                return val[0]
        return None
        
def modify(a, b, c, float_key, value, is_right):
    ind = int(float_key[2:]) - 1
    add_to_a = [Fraction(0)] * len(a[0])
    ready_sol = None

    if is_right:
        add_to_a[ind] = Fraction(-1)
        b.append((-1) * Fraction(value.__ceil__()))
        a.append(add_to_a)

    else:
        if (value.__floor__() == 0):
            ready_sol = {float_key : 0}
            for i in range(len(a)):
                a[i].pop(ind)
            c.pop(ind)
                
        else:
            add_to_a[ind] = Fraction(1)
            b.append(Fraction(value.__floor__()))
            a.append(add_to_a)
        
    return a, b, c, ready_sol

class Branch_and_bound:
    def __init__(self, a, b, c, opt, ready_sol = None):
        # Solving with simplex_method
        F, solution = sm.simplex_internal(deepcopy(a), deepcopy(b), deepcopy(c), opt, ready_sol)
        if solution != None:
            sm.print_solution(F, solution, opt)
        
        # Solution of the init problem (ROOT)
        self.value = Value(F, solution)
        self.left = None
        self.right = None
        
        # Recursive
        if solution is not None:
            float_key = self.value.get_float()
            if float_key is not None:
                # Left child
                print("\nBranching", float_key, solution[float_key])
                print("Left child of ", solution)
                a_l, b_l, c_l, ready_sol = modify(deepcopy(a), \
                        deepcopy(b), deepcopy(c), float_key, solution[float_key], False)
                self.left = Branch_and_bound(a_l, b_l, c_l, opt, ready_sol)
            
                # Right chil
                print("\nBranching", float_key, solution[float_key])
                print("Right child of ", solution)
                a_r, b_r, c_r, ready_sol = modify(a, b, c, float_key, solution[float_key], True)
                self.right = Branch_and_bound(a_r, b_r, c_r, opt, ready_sol)

# inly maximazing
def brute_force(a, b, c, right_bound):
    max_F = 0;
    x = [0, 0, 0]

    for x1 in range(right_bound):
        for x2 in range(right_bound):
            for x3 in range(right_bound):
                if (np.matmul(a, np.array([x1, x2, x3]).reshape(3, 1))
                            <= np.array(b).reshape(3, 1)).all():
                    F_value = np.matmul(np.array(c).T, np.array([x1, x2, x3]))
                    print("One the the solutions from brute force: ")
                    print("F = ", F_value, "\nx = ", [x1, x2, x3])
                    if (F_value > max_F):
                        max_F = F_value
                        x = [x1, x2, x3]

    return max_F, x


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

    a, b, c, opt = sm.parse(input_file)
    sys.stdout = open('log.txt', 'w')

    # Brute force
    max_F, brute_sol = brute_force(a, b, c, 10)
    print("Best solution from brute force: ")
    print("F = ", max_F, "\nx = ", brute_sol)

    # Branch and bound
    solution = Branch_and_bound(a, b, c, opt)
    sys.stdout.close()

if __name__ == "__main__":
    main(sys.argv[1:])
