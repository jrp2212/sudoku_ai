import sys
import time
import statistics

ROW = "ABCDEFGHI"
COL = "123456789"
domain = {1,2,3,4,5,6,7,8,9}

def print_board(board):
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def findsquare(position):
        letter = position[0]
        num = position[1]
        
        letters  = []
        nums = []
        
        abc = ['A','B','C']
        deff = ['D','E','F']
        ghi = ['G','H','I']
        one = ['1','2','3']
        four = ['4','5','6']
        seven = ['7','8','9']
        
        if letter in abc:
            letters = abc
        elif letter in deff:
            letters = deff
        elif letter in ghi:
            letters = ghi
        if num in one:
            nums = one
        elif num in four:
            nums = four
        elif num in seven:
            nums = seven
        
        return letters, nums

def aval_values(position, board):
    letter = position[0]
    num = position[1]
    letters, nums = findsquare(position)
    
    values = set()
    
    for i in COL:
        values.add(board[letter+i])
    for i in ROW:
        values.add(board[i+num])
    for i in letters:
        for j in nums:
            values.add(board[i+j])
    
    return domain.difference(values)

def mrp(board):
    min_var = ""
    min_len = 9
    
    for r in range(9): 
        for c in range(9):
            if board[ROW[r]+COL[c]] == 0:
                aval_vals = aval_values(ROW[r]+COL[c], board)
                if len(aval_vals) == 0:
                    return "00"
                elif len(aval_vals) < min_len:
                    min_len = len(aval_vals)
                    min_var = ROW[r]+COL[c]
                    
    return min_var


def alldiff(position, board):

    def diffrow(position, board):
        values = set()
        letter = position[0]
        
        for i in COL:
            if board[letter+i] in values or board[letter+i] == 0:
                return False
            else:
                values.add(board[letter+i])
                
        return True


    def diffcolumn(position, board):
        values = set()
        num = position[1]
        
        for i in ROW:
            if board[i+num] in values or board[i+num] == 0:
                return False
            else:
                values.add(board[i+num])
                
        return True


    def diffsquare(position, board):
        values = set()
        letters, nums = findsquare(position)
        
        for i in letters:
            for j in nums:
                if board[i+j] in values or board[i+j] == 0:
                    return False
                else:
                    values.add(board[i+j])
        
        return True
    
    if diffrow(position, board) == False:
        return False
    if diffcolumn(position, board) == False:
        return False
    if diffsquare(position, board) == False:
        return False

    return True

def complete(board):
    letters = ["A","B","C","D","E","F", "G", "H", "I"]
    nums = ["1","4","7","1","4","7","1","4","7"]
    
    for i in range(len(letters)):
        position = letters[i]+nums[i]
        if alldiff(position, board) == False:
            return False

    return True



def backtracking(board):
    
    if complete(board):
        return board
    var = mrp(board)
    if var != "00" and len(var) == 2:
        for val in aval_values(var, board):
            board.update({var:val})
            sol = backtracking(board)
            if sol is not None:
                return sol
            else:
                board.update({var:0})          
    return None


if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        solved_board = backtracking(board)
        
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        runtime = []
        max_time = 0
        min_time = 100
        total_time = 0
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue
          
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            solved_board = backtracking(board)
            
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')
            
        
        print("Finishing all boards in file.")