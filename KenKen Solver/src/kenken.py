import ast

import time
from csp import CSP

from csp import backtracking_search

from csp import mrv

from csp import forward_checking, mac

from csp import min_conflicts


class Kenken(CSP):
    """ A Kenken problem """
    n = 0   # n uninitialized
    variables = list()  # a list for the csp's variables
    domains = dict()    # a dictionary for the domains of the csp's variables
    neighbors = dict()  # a dictionary for the neighbors of each csp's variable (I consider a neighbor for each variable every other variable in the same column or row with that one)
    cage_constraints = list()   # a list for each cage constraint as read from the text file
    cages = dict()      # a dictionary that for each variable stores it's whole cage, with the constraint and the target value)
    constraint_checks = 0    # to measure algorithms' efficiency
    number_of_assignments = 0   # to measure algorithms' efficiency

    # initialization function
    def __init__(self, filename):
        """Create a Kenken puzzle by taking all the neccessary input from the specified text file"""
        ln = 0  # number of line-to-read
        with open(filename) as f:   # take input from the text file
            for line in f:
                ln += 1  # the line that we are reading
                if ln == 1:
                    print(line)
                    self.n = int(line)
                else:
                    a = line.split()
                    b = list()
                    pairs = ast.literal_eval(a[0])
                    for p in pairs:
                        b.append("K"+str(p[0])+str(p[1]))
                    c = list()
                    c.append(b)
                    c.append(a[1])
                    c.append(ast.literal_eval(a[2]))
                    self.cage_constraints.append(c)
        # fill variables' list
        for i in range(0, self.n):
            for j in range(0, self.n):
                self.variables.append("K"+str(i)+str(j))
        # fill cages' dictionary
        for constr in self.cage_constraints:
            for c1 in constr[0]:
                self.cages[c1] = constr
        # fill variable domains' dictionary
        for v in self.variables:
            self.domains[v] = [i for i in range(1,self.n+1)]
        # initialize lists for neighbors' dictionary members
        for v in self.variables:        # initialize neighbors
            self.neighbors[v] = list()
        # fill neighbors' dictionary
        for v1 in self.variables:
            for v2 in self.variables:   # neighbors by row or column constraint
                if (v1 != v2) and ((v1[1] == v2[1]) or (v1[2] == v2[2])) and (v2 not in self.neighbors[v1]):
                    self.neighbors[v1].append(v2)
        # print the structures that we have created so far
        print("Variables : ", self.variables)
        print("Domains : ", self.domains)
        print("Cage constraints : ", self.cage_constraints)
        #print("Cages : ", self.cages)
        #print("Neighbors : ", self.neighbors)
        print("")  # in order to change line
        # initialize CSP
        CSP.__init__(self, self.variables, self.domains, self.neighbors, self.kenken_constraint)

    # reset CSP's elements
    def reset(self):
        self.n = 0  # n uninitialized
        del self.variables[:]   # delete variables' list
        self.domains.clear()    # clear domains' dictionary
        self.neighbors.clear()  # clear neighbors' dictionary
        del self.cage_constraints[:]    # delete cage constraints' list
        self.cages.clear()              # clear cages' dictionary
        self.reset_constraint_checks()  # reset constraint checks counter
        self.reset_number_of_assignments()  # reset number of assignments counter

    # reset number of constraint checks counter
    def reset_constraint_checks(self):
        self.constraint_checks = 0

    # reset number of assignments counter
    def reset_number_of_assignments(self):
        self.number_of_assignments = 0

    # get number of constraint checks counted
    def get_constraint_checks(self):
        return self.constraint_checks

    # get number of assignments counted
    def get_number_of_assignments(self):
        return self.number_of_assignments

    # overriding original assignment function so we can count assignments
    def assign(self, var, val, assignment):
        "Add {var: val} to assignment; Discard the old value if any."
        assignment[var] = val
        self.nassigns += 1
        self.number_of_assignments += 1  # one more assignment occurred

    # display function
    def display(self, assignment):
        """ Show a human-readable representation of our Kenken CSP """
        # create our board and initialize it to zeros (0)
        board = []
        for i in range(0, self.n):
            b = []
            for j in range(0, self.n):
                b.append(0)
            board.append(b)
        # pass the assignment to our board
        for v in assignment:
            i = int(v[1])
            j = int(v[2])
            board[i][j] = assignment[v]
        # print board
        for i in range(0, self.n):
            for j in range(0, self.n):
                print(board[i][j], end=" ")
            print("")   # in order to change line
        print("")  # in order to change line

    # constraints function
    def kenken_constraint(self, A, a, B, b):
        """ Check if we can have A=a and B=b in the same time """
        self.constraint_checks += 1     # one more constraint check made
        my_assignment = self.infer_assignment()  # get the current assignment (B included)
        my_assignment[A] = a  # add A to the current assignment
        # if A and B are the same variable
        if A == B:
            return True
        # two neighbors can't have the same values
        if B in self.neighbors[A] and a == b:
            return False
        # check cages
        if B in self.cages[A][0]:  # if A and B in the same cage
            assert self.cages[A][0] != "''"
            if self.cages[A][1] == 'sub':
                if abs(a - b) != self.cages[A][2]:
                    return False
            elif self.cages[A][1] == 'div':
                d = float(a)/b
                if d > 1:
                    if d != self.cages[A][2]:
                        return False
                else:
                    if 1/d != self.cages[A][2]:
                        return False
            elif self.cages[A][1] == 'add':
                res = 0
                for v in self.cages[A][0]:
                    if v in my_assignment:
                        res += my_assignment[v]
                    else:
                        return True
                    if res > self.cages[A][2]:
                        return False
                if res != self.cages[A][2]:
                    return False
            elif self.cages[A][1] == 'mult':
                res = 1
                for v in self.cages[A][0]:
                    if v in my_assignment:
                        res *= my_assignment[v]
                    else:
                        return True
                    if res > self.cages[A][2]:
                        return False
                if res != self.cages[A][2]:
                    return False
        else:
            if self.cages[A][1] == "''":
                if a != self.cages[A][2]:
                    return False
            elif self.cages[A][1] == 'sub':
                for v in self.cages[A][0]:
                    if v != A:
                        if v in my_assignment:
                            if abs(a - my_assignment[v]) != self.cages[A][2]:
                                return False
            elif self.cages[A][1] == 'div':
                for v in self.cages[A][0]:
                    if v != A:
                        if v in my_assignment:
                            d = float(a)/my_assignment[v]
                            if d > 1:
                                if d != self.cages[A][2]:
                                    return False
                            else:
                                if 1/d != self.cages[A][2]:
                                    return False
            elif self.cages[A][1] == 'add':
                res = 0
                for v in self.cages[A][0]:
                    if v in my_assignment:
                        res += my_assignment[v]
                    else:
                        return True
                    if res > self.cages[A][2]:
                        return False
                if res != self.cages[A][2]:
                    return False
            elif self.cages[A][1] == 'mult':
                res = 1
                for v in self.cages[A][0]:
                    if v in my_assignment:
                        res *= my_assignment[v]
                    else:
                        return True
                    if res > self.cages[A][2]:
                        return False
                if res != self.cages[A][2]:
                        return False

        # if A=a and B=b passed all of the above tests successfully
        return True


""" My public functions"""

def solve_kenken(k):
    """ Solve a given Kenken CSP using a variety of algorithms """
    # solve csp with BT algorithm
    print("Solving with BT algorithm...")
    start_time = time.clock()
    BT_ans = backtracking_search(k)
    end_time = time.clock()
    print("BT algorithm runtime: " + str(end_time - start_time) + " seconds")
    print("In this time, constraints got checked " + str(k.get_constraint_checks()) + " times and " + str(k.get_number_of_assignments()) + " assignments occurred")
    k.reset_constraint_checks()
    k.reset_number_of_assignments()
    print("\tBT = ", BT_ans)
    if BT_ans != None:
        k.display(BT_ans)

    # solve csp with BT+MRV algorithm
    print("Solving with BT+MRV algorithm...")
    start_time = time.clock()
    BT_MRV_ans = backtracking_search(k, select_unassigned_variable=mrv)
    end_time = time.clock()
    print("BT+MRV algorithm runtime: " + str(end_time - start_time) + " seconds")
    print("In this time, constraints got checked " + str(k.get_constraint_checks()) + " times and " + str(k.get_number_of_assignments()) + " assignments occurred")
    k.reset_constraint_checks()
    k.reset_number_of_assignments()
    print("\tBT_MRV_ans = ", BT_MRV_ans)
    if BT_MRV_ans != None:
        k.display(BT_MRV_ans)

    # solve csp with FC algorithm
    print("Solving with FC algorithm...")
    start_time = time.clock()
    FC_ans = backtracking_search(k, inference=forward_checking)
    end_time = time.clock()
    print("FC algorithm runtime: " + str(end_time - start_time) + " seconds")
    print("In this time, constraints got checked " + str(k.get_constraint_checks()) + " times and " + str(k.get_number_of_assignments()) + " assignments occurred")
    k.reset_constraint_checks()
    k.reset_number_of_assignments()
    print("\tFC_ans = ", FC_ans)
    if FC_ans != None:
        k.display(FC_ans)

    # solve csp with FC+MRV algorithm
    print("Solving with FC+MRV algorithm...")
    start_time = time.clock()
    FC_MRV_ans = backtracking_search(k, select_unassigned_variable=mrv, inference=forward_checking)
    end_time = time.clock()
    print("FC+MRV algorithm runtime: " + str(end_time - start_time) + " seconds")
    print("In this time, constraints got checked " + str(k.get_constraint_checks()) + " times and " + str(k.get_number_of_assignments()) + " assignments occurred")
    k.reset_constraint_checks()
    k.reset_number_of_assignments()
    print("\tFC_MRV_ans = ", FC_MRV_ans)
    if FC_MRV_ans != None:
        k.display(FC_MRV_ans)

    # solve csp with MAC algorithm
    print("Solving with MAC algorithm...")
    start_time = time.clock()
    MAC_ans = backtracking_search(k, inference=mac)
    end_time = time.clock()
    print("MAC algorithm runtime: " + str(end_time - start_time) + " seconds")
    print("In this time, constraints got checked " + str(k.get_constraint_checks()) + " times and " + str(k.get_number_of_assignments()) + " assignments occurred")
    k.reset_constraint_checks()
    k.reset_number_of_assignments()
    print("\tMAC_ans = ", MAC_ans)
    if MAC_ans != None:
        k.display(MAC_ans)

    # solve csp with MINCONFLICTS algorithm
    print("Solving with MINCONFLICTS...")
    start_time = time.clock()
    minconflicts_ans = min_conflicts(k)
    end_time = time.clock()
    print("MINCONFLICTS runtime: " + str(end_time - start_time) + " seconds")
    print("In this time, constraints got checked " + str(k.get_constraint_checks()) + " times and " + str(k.get_number_of_assignments()) + " assignments occurred")
    k.reset_constraint_checks()
    k.reset_number_of_assignments()
    print("\tMINCONFLICTS_ans = ", minconflicts_ans)
    if minconflicts_ans != None:
        k.display(minconflicts_ans)


""" My Main Method """

if __name__ == '__main__':
    print("Solving a Kenken puzzle with N = 3...\n")
    # create a kenken csp
    k1 = Kenken('../input/kenken3.txt')
    start_time = time.clock()
    solve_kenken(k1)
    end_time = time.clock()
    print("Total runtime: " + str(end_time-start_time) + " seconds\n")
    k1.reset()
    print("-----------------------------------------------------------------------------------------------------------")
    #time.sleep(5)

    print("Solving a Kenken puzzle with N = 3 (different case)...\n")
    # create a kenken csp
    k2 = Kenken('../input/kenken3b.txt')
    start_time = time.clock()
    solve_kenken(k2)
    end_time = time.clock()
    print("Total runtime: " + str(end_time - start_time) + " seconds\n")
    k2.reset()
    print("-----------------------------------------------------------------------------------------------------------")
    # time.sleep(5)

    print("Solving a Kenken puzzle with N = 4...\n")
    # create a kenken csp
    k3 = Kenken('../input/kenken4a.txt')
    start_time = time.clock()
    solve_kenken(k3)
    end_time = time.clock()
    print("Total runtime: " + str(end_time - start_time) + " seconds\n")
    k3.reset()
    print("-----------------------------------------------------------------------------------------------------------")
    #time.sleep(5)

    print("Solving a Kenken puzzle with N = 4 (different case)...\n")
    # create a kenken csp
    k4 = Kenken('../input/kenken4b.txt')
    start_time = time.clock()
    solve_kenken(k4)
    end_time = time.clock()
    print("Total runtime: " + str(end_time - start_time) + " seconds\n")
    k4.reset()
    print("-----------------------------------------------------------------------------------------------------------")
    #time.sleep(5)

    print("Solving a Kenken puzzle with N = 5...\n")
    # create a kenken csp
    k5 = Kenken('../input/kenken5.txt')
    start_time = time.clock()
    solve_kenken(k5)
    end_time = time.clock()
    print("Total runtime: " + str(end_time - start_time) + " seconds\n")
    k5.reset()
    print("-----------------------------------------------------------------------------------------------------------")
    #time.sleep(5)

    print("Solving a Kenken puzzle with N = 6...\n")
    # create a kenken csp
    k6 = Kenken('../input/kenken6.txt')
    start_time = time.clock()
    solve_kenken(k6)
    end_time = time.clock()
    print("Total runtime: " + str(end_time - start_time) + " seconds\n")
    k6.reset()
    print("-----------------------------------------------------------------------------------------------------------")
    #time.sleep(5)

    print("Solving a Kenken puzzle with N = 6 (different case)...\n")
    # create a kenken csp
    k7 = Kenken('../input/kenken6b.txt')
    start_time = time.clock()
    solve_kenken(k7)
    end_time = time.clock()
    print("Total runtime: " + str(end_time - start_time) + " seconds\n")
    k7.reset()
    print("-----------------------------------------------------------------------------------------------------------")
    # time.sleep(5)

    print("Solving a Kenken puzzle with N = 7...\n")
    # create a kenken csp
    k8 = Kenken('../input/kenken7.txt')
    start_time = time.clock()
    solve_kenken(k8)
    end_time = time.clock()
    print("Total runtime: " + str(end_time - start_time) + " seconds\n")
    k8.reset()
    print("-----------------------------------------------------------------------------------------------------------")
    #time.sleep(5)

    print("Solving a Kenken puzzle with N = 7 (different case)...\n")
    # create a kenken csp
    k9 = Kenken('../input/kenken7b.txt')
    start_time = time.clock()
    solve_kenken(k9)
    end_time = time.clock()
    print("Total runtime: " + str(end_time - start_time) + " seconds\n")
    k9.reset()
    print("-----------------------------------------------------------------------------------------------------------")
    # time.sleep(5)

    print("Solving a Kenken puzzle with N = 8...\n")
    # create a kenken csp
    k10 = Kenken('../input/kenken8.txt')
    start_time = time.clock()
    solve_kenken(k10)
    end_time = time.clock()
    print("Total runtime: " + str(end_time - start_time) + " seconds\n")
    k10.reset()
    print("-----------------------------------------------------------------------------------------------------------")
    # time.sleep(5)
