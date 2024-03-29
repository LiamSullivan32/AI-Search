############################################################
# CMPSC 442: Uninformed Search
############################################################

student_name = "Michael Sullivan."

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import math
import random
import copy
from collections import deque


#69 without with 86.3, total = 17.3/25

#n_queens valid is 5

#num placements adds 4.5/5

############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    return math.comb(n**2, n)

def num_placements_one_per_row(n):
    return n ** n

def n_queens_valid(board):
    if len(board) == 1:
        return True
    
    seen = set()
    seen_down = set()
    seen_up = set()
    for i in range(len(board)):
        col = board[i]
        up = board[i] - i
        down = board[i] + i
        if up in seen_up or down in seen_down or col in seen:
            return False
        seen_up.add(up)
        seen_down.add(down)
        seen.add(col)
    return True


def dfs(board, depth, n):
    if depth < n:
        for i in range(n):
            new_board = board + [i]
            if n_queens_valid(new_board): 
                for j in dfs(new_board, depth+1, n):
                    yield j
    else:
        yield board
        return


def n_queens_solutions(n):
    for i in dfs([], 0, n):
        yield i.copy() #fa
    pass


############################################################
# Section 2: Lights Out
############################################################

#42/45

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.rows = len(board) - 1
        self.columns = len(board[0]) - 1

    def get_board(self):
        return self.board
    
    #correct 
    def perform_move(self, row, col):
        #witj: 21.6, without: 15.6
    
        neighbors = []
        toggled = self.board[row][col]
        if row < self.rows:
            neighbors.append([1,0])
        if row > 0:
            neighbors.append([-1,0])
        if col < self.columns:
            neighbors.append([0,1])
        if col > 0:
            neighbors.append([0,-1])
        self.board[row][col] = not toggled
        for move in neighbors:
            #simulating turning the lights off for each of the allowed moves
            self.board[row+move[0]][col+move[1]] = not self.board[row+move[0]][col+move[1]]

    def scramble(self):
        #No effect before and after commentiing out
        if self.get_board():
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if random.random() < 0.5:
                        self.perform_move(i,j)
        #self.perform_move(1,1)
        #self.perform_move(self.rows,self.columns)

    def is_solved(self):
        #entirely true
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == True:
                    return False
        return True

    #entirely correct
    def copy(self):
        #potential need for deepcopy
        return LightsOutPuzzle(copy.deepcopy(self.get_board()))


    def successors(self): 
        if self.get_board():
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    new_move = (i,j)
                    new_board = self.copy()#copys puzzle objects
                    #only performing move on lights on, potentially get rid of
                    new_board.perform_move(i, j)
                    yield (new_move, new_board)
        else:
            return None

    def find_solution(self):
        visited = []
        queue = deque()

        init_board = tuple(tuple(row) for row in self.get_board())
        queue.append((self.copy(),[]))#path and the board
        visited = set([init_board])
        while queue:
            current_puzzle, current_path = queue.popleft()
            print(current_path)
            if current_puzzle.is_solved():
                return current_path
            for succ_path, board in current_puzzle.successors():
                succ_board = tuple(tuple(row) for row in board.get_board())
                if succ_board not in visited:
                    new_path = current_path + [succ_path]
                    visited.add(succ_board)
                    queue.append((board, new_path))
        return None

def create_puzzle(rows, cols):
    board = [[False for x in range(cols)] for y in range(rows)]#may need to sway rows and columns
    return LightsOutPuzzle(board)

############################################################
# Section 3: Linear Disk Movement
############################################################

#27.6

def initialize_distict_disks(length, n):
    if n > length:
        return False
    puzzle_row = [0 for _ in range(length)]
    for i in range(n):
        puzzle_row[i] = i + 1
    return puzzle_row


def initialize_disks(length, n):
    if n > length:
        return False
    puzzle_row = [1 for _ in range(n)] + [0 for _ in range(length-n)]
    return puzzle_row 

def perform_move(row, start, finish):
    temp = row[start]
    row[start] = row[finish]
    row[finish] = temp
    return row

def is_solved(row, length, n):
    print(row)
    for i in range(length - n):
        if row[i] != 0:
            print("false")
            return False
    for i in range(length - n, length):
        if row[i] != 1:
            print("fale 2")
            return False
    return True


def successor_rows(row):
    length = len(row)
    successors = []
    for index in range(length-1):#potential cause for error
        if row[index] == 1:
            #here we have a disk, now we check if we can move the disk
            if row[index+1] == 0:
                new_row = perform_move(row.copy(), index, index+1)
                successors.append(((index, index+1), new_row))
            else:
                if index + 2 < length and row[index+2] == 0:
                    new_row = perform_move(row.copy(), index, index+2)
                    successors.append(((index, index+2), new_row))
    return successors

def successor_rows_distinct(row):
    length = len(row)
    successors = []
    for index in range(length):
        #move index to index + 1 if index + 1 if index+ 1 is zero or is 
        moves = ((index, index+1), (index, index+2), (index, index-1), (index, index-2))
        for i in moves:
            if i[0] >= length or i[1] >= length or i[0] < 0 or i[1] < 0:
                continue
            if row[i[0]] == 0 or row[i[1]] != 0:
                continue
            if abs(i[0] - i[1]) == 2 and row[min(i[0], i[1])+1] == 0:
                print("here")
                continue
            new_row = perform_move(row.copy(), i[0], i[1])
            #successors.append(((i[0], i[1]), new_row))
            yield ((i[0], i[1]), new_row)
    #return successors
    return None
            
            

    #successors.sort(key=lambda entry: entry[0][0], reverse=True)
    return successors

def solve_identical_disks(length, n):
    row = initialize_disks(length, n)
    if row:
        queue = deque()
        init = tuple(row)
        queue.append((row.copy(), []))
        visited = set([init])#potentially dont use copy
        while queue:
            current_row, current_path = queue.popleft()
            if is_solved(current_row, length, n):
                return current_path
            succ_rows = successor_rows(current_row)
            for move, new_row in successor_rows(current_row):
                new_row_tuple = tuple(new_row)
                if new_row_tuple not in visited:
                    visited.add(new_row_tuple)
                    new_path = current_path + [move]
                    queue.append((new_row, new_path))
        return None
    return None


def is_solved_distinct(row, length, n):
    print(row)
    for i in range(n):
        if row[length-1-i] != i + 1:
            return False
    for i in range(length - n):
        if row[i] != 0:
            return False

    return True


def solve_distinct_disks(length, n):
    row = initialize_distict_disks(length, n)
    if row:
        queue = deque()
        init = tuple(row)
        queue.append((row.copy(), []))
        visited = set([init])#potentially dont use copy
        while queue:
            current_row, current_path = queue.popleft()
            if current_path == [(1, 3), (0, 1), (2, 0), (3, 2), (1, 3)]:
                print(current_row)
                print("g")
            if is_solved_distinct(current_row, length, n):
                return current_path
            for move, new_row in successor_rows_distinct(current_row):
                new_row_tuple = tuple(new_row)
                if new_row_tuple not in visited:
                    visited.add(new_row_tuple)
                    new_path = current_path + [move]
                    queue.append((new_row, new_path))
        return None
    return None
            #in order to modify the orignial function, we must favor lower rows in moving up first


   
if __name__=="__main__":

    print(solve_distinct_disks(5,3))