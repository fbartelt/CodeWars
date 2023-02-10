#%%
import numpy as np

class Constraint():
    def __init__(self, variables):
        self.variables = variables

    def satisfied(self, assignment) -> bool:
        for (i, j), num in assignment.items():
            for row_i in range(9):
                if num == assignment.get((row_i, j)) and row_i != i:
                    return False

            for col_j in range(9):
                if num == assignment.get((i, col_j)) and col_j != j:
                    return False
            
            block = [(x, y) for x in range((i//3)*3, (i//3+1)*3) if x!=i for y in range((j//3)*3, (j//3+1)*3) if y!=j]
            for (block_i, block_j) in block:
                 if num == assignment.get((block_i, block_j)):
                    return False
            
        return True    

class CSP():
    def __init__(self, variables, domains):
        self.variables= variables 
        self.domains = domains 
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")
            
    def add_constraint(self, constraint) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError(f"Variable <{variable}> in constraint not in CSP")  
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True
    
    def backtracking_search(self, assignment={}):
        if len(assignment) == len(self.variables):
            return assignment

        unassigned = [v for v in self.variables if v not in assignment]
        first = unassigned[0]

        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value

            if self.consistent(first, local_assignment):
                result = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None

class Sudoku:
    def __init__(self, board):
        if (len(board), len(board[0])) != (9, 9):
            raise ValueError("Sudoku board must be 9x9")
        self.board = np.array(board)
        self.initial_assignment = {}
        self.csp = self._init_csp()
        self.solution = None
    
    def __repr__(self):
        string = 'Sudoku problem:\n'
        for i, row in enumerate(self.board):
            for j, num in enumerate(row):
                string += f"{num} {'|' if (((j+1) % 8)//3 > j//3) else ''}"
            string+= '\n'
            if ((i+1) % 8)//3 > i//3:
                string += '-'*19 + '\n'
        return string
    
    def _init_csp(self):
        variables = []
        domains = {}
        options = set(list(range(1,10)))
        for i, row in enumerate(self.board): 
            for j, num in enumerate(row):
                variable = (i, j)
                variables.append(variable)
                if num != 0:
                    domains[variable] = [num,]
                    self.initial_assignment[variable] = num
                else: 
                    in_row = set(row)
                    in_col = set(self.board[:, j])
                    in_block = set(self.get_block(i, j).flatten())
                    domain = options - in_row - in_col - in_block
                    domains[variable] = list(domain)
        return CSP(variables, domains)
    
    def get_block(self, i, j):
        block_i, block_j = i//3, j//3
        block = self.board[block_i*3: (block_i+1)*3, block_j*3: (block_j+1)*3]
        return block
    
    def solve(self):
        self.csp.add_constraint(Constraint(self.csp.variables))
        unsorted_sol = self.csp.backtracking_search(self.initial_assignment)
        self.solution = dict(sorted(unsorted_sol.items(), key=lambda x: (x[0], x[1])))
        self.print_solution()
        return self.solution
    
    def print_solution(self):
        string = 'Solution:'
        for (i, j), num in self.solution.items():
            if not j%9:
                string+= '\n'
            string += f"{num} {'|' if (((j+1) % 8)//3 > j//3) else ''}"
            if (((i+1) % 8)//3 > i//3 and j==8):
                string += '\n' + '-'*19
        print(string)

def sudoku(puzzle):
    s = Sudoku(puzzle)
    sol = np.array(list(s.solve().values())).reshape(9, 9).tolist()
    return sol
#%%
# TEST
import time
start_time = time.time()
board = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]

s1 = Sudoku(board)
print(s1)
sol = s1.solve()
print("--- %s seconds ---" % (time.time() - start_time))