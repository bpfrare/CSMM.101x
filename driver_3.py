import argparse
import timeit
from math import sqrt
from collections import deque, MutableSet
from heapq import heappush, heappop
import sys
if sys.platform != "win32":
    import resource    

class Board:
    board = []

    def __init__(self, board):
        '''
        0 1 2
        3 4 5
        6 7 8
        '''
        self.board = board
        # The size of board
        # self.size = int(sqrt(len(board)))
        self.size = 3
        self.zeroIndex = board.index('0')
        self.hash = hash(''.join(self.board))

    def move(self, direction):
        '''
        Move zero to direction
        '''
        temp_board = self.board[:]
        temp = temp_board[self.zeroIndex + direction]
        temp_board[self.zeroIndex + direction] = temp_board[self.zeroIndex]
        temp_board[self.zeroIndex] = temp
        return Board(temp_board)
  
    def up(self):
        '''
        Move Zero to up
        '''
        return self.move(-self.size)

    def down(self):
        '''
        Move Zero to down
        '''
        return self.move(self.size)

    def left(self):
        '''
        Move Zero to left
        '''
        return self.move(-1)

    def right(self):
        '''
        Move Zero to left
        '''
        return self.move(1)
    
    def __eq__(self, other):
        return self.hash == other.hash

    def __hash__(self):
        return self.hash

    def __str__(self):
        aux = ''
        for i in range(self.size):
            print(''.join(self.board[i*self.size: i*self.size + self.size]))
        return aux

class State:

    def __init__(self, board, parent, children, direction=None, depth=0):
        self.parent = parent
        self.children = children
        self.board = board
        self.direction = direction
        self.depth = depth
        self.hash = self.board.hash

    def neighbors(self, reverse=False):
        '''
        Add all UDLR possible
        We always visit child nodes in the "UDLR"
        '''
        states = []
        # Go UP if can
        if (self.board.zeroIndex not in [0, 1, 2]):
            states.append(State(self.board.up(), self, [], "Up", self.depth + 1))
        # Go Down if can
        if (self.board.zeroIndex not in [6, 7, 8]):
            states.append(State(self.board.down(), self, [], "Down", self.depth + 1))
        # Go Left if can
        if (self.board.zeroIndex not in [0, 3, 6]):
            states.append(State(self.board.left(), self, [], "Left", self.depth + 1))
        # Go Right if can
        if (self.board.zeroIndex not in [2, 5, 8]):
            states.append(State(self.board.right(), self, [], "Right", self.depth + 1))
        if reverse:
            return reversed(states)
        else:
            return states

    def __hash__(self):
        return self.board.hash

    def __eq__(self, other):
        return self.hash == other.hash

class Solver:

    goal = None
    nodes_expanded = -1
    
    max_search_depth = 0
    time_start = None
    ram = None

    def __init__(self, initialBoard):
        self.initialBoard = initialBoard
        self.goal = Board(sorted(list(initialBoard.board)))
        self.time_start = timeit.default_timer()

    def bfs(self):
        frontier = deque([State(self.initialBoard, None, None)])
        explored = set()
        while frontier:
            state = frontier.popleft()
            explored.add(state)
            # Updade Status
            self.nodes_expanded += 1
            # success
            if state.board == self.goal:
                return state

            # Add next
            for neighbor in state.neighbors():
                if neighbor not in explored and neighbor not in frontier:
                    frontier.append(neighbor)
                    if self.max_search_depth < neighbor.depth:
                        self.max_search_depth = neighbor.depth
        # Failure
        return False

    def dfs(self):
        frontier = deque([State(self.initialBoard, None, None)])
        explored = set()
        while frontier:
            state = frontier.pop()
            explored.add(state)
            # Updade Status
            self.nodes_expanded += 1
            # success
            if state.board == self.goal:
                return state

            # Add next
            for neighbor in state.neighbors(reverse=True):
                if neighbor not in explored and neighbor not in frontier:
                    frontier.append(neighbor)
                    if self.max_search_depth < neighbor.depth:
                        self.max_search_depth = neighbor.depth
        # Failure
        return False

    def ast(self):
        frontier = deque([State(self.initialBoard, None, None)]) # HEap.new(State(self.initialBoard, None, None))
        explored = set()
        while frontier:
            state = heappop(frontier)
            explored.add(state)
            # Updade Status
            self.nodes_expanded += 1
            # success
            if state.board == self.goal:
                return state

            # Add next
            for neighbor in state.neighbors(reverse=True):
                if neighbor not in explored and neighbor not in frontier:
                    # Updade status
                    if self.max_search_depth < neighbor.depth:
                        self.max_search_depth = neighbor.depth
                    heappush(frotier, neighbor)
                elif neighbor in frontier:
                    pass
                    #frontier.decreaseKey(neighbor)
                    
        # Failure
        return False



    def output(self, state):
        s = state
        path_to_goal = []
        depth = []
        while s:
            path_to_goal.append(s.direction)
            depth.append(s.depth)
            s = s.parent
        path_to_goal = path_to_goal[-2::-1]
        depth = depth[-2::-1]
        try:
            depth = depth[-1]
        except IndexError:
            depth = 0
        with open("output.txt", 'w') as arq:
            print("path_to_goal:", path_to_goal, file=arq)
            print("cost_of_path:", len(path_to_goal), file=arq)
            print("nodes_expanded:", self.nodes_expanded, file=arq)
            print("search_depth:", depth, file=arq)
            print("max_search_depth:", self.max_search_depth, file=arq)
            print("running_time:", timeit.default_timer() - self.time_start, file=arq)
            if sys.platform != "win32":
                print("max_ram_usage:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, file=arq)
                

def main(method, board):
    solver = Solver(Board(board))
    if method == 'bfs':
        solver.output(solver.bfs())
    elif method == 'dfs':
        solver.output(solver.dfs())
 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("method", help="method: [bfs, dfs, ast]")
    parser.add_argument("board", help="board: 1,2,5,3,4,0,6,7,8")
    args = parser.parse_args()
    main(args.method, args.board.split(","))
