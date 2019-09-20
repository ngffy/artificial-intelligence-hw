from queue import PriorityQueue

class State():
    def __init__(self, board, parent=None, g=0):
        self.board = board
        self.id = hash(tuple(self.board))

        if parent is not None:
            self.parent_id = parent.id
            self.priority = parent.priority + 1
        else:
            self.parent_id = 0
            self.priority = 0

        self.f = 0
        self.g = g
        self.h = 0

    def get_adjacent_slots(self, i):
        on_top_edge = i in range(0, 4)
        on_left_edge = i in range(0, 20, 4)
        on_right_edge = i in range(3, 24, 4)
        on_bot_edge = i in range(16, 20)

        adj_slots = []
        if not on_top_edge:
            adj_slots.append(i-4)
        if not on_left_edge:
            adj_slots.append(i-1)
        if not on_right_edge:
            adj_slots.append(i+1)
        if not on_bot_edge:
            adj_slots.append(i+4)

        return adj_slots

    def expand_state(self):
        empty_slot = self.board.index(0)
        adj_slots = self.get_adjacent_slots(empty_slot)

        neighbors = [list(self.board) for i in adj_slots]
        for n in neighbors:
            tmp = adj_slots.pop()
            n[empty_slot], n[tmp] = n[tmp], n[empty_slot]

        cost = lambda x: 1 if x < 10 else 2
        new_states = [State(n, self, cost(n[empty_slot])) for n in neighbors]
        return new_states

    def pretty_board(self):
        s = ""
        for i in range(0, 5):
            s += str(self.board[4*i:4*i+4])[1:-1] + "\n"
        return s[:-1]

    def __str__(self):
        funcs = "f: "+str(self.f)+" g: "+str(self.g)+" h: "+str(self.h)
        pid = "\nParent ID: "+str(self.parent_id)
        prior = "\npriority: "+str(self.priority)
        return "ID "+str(self.id)+":\n"+self.pretty_board()+"\n"+funcs+pid+prior

    def __eq__(self, other):
        return self.board == other.board

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

def heuristic_one(curr_state, goal_state):
    h = 0
    for i in range(0, 20):
        if curr_state.board[i] != goal_state.board[i]:
            h += 1
    return h

def heuristic_two(curr_state, goal_state):
    h = 0
    for i in range(0, 20):
        if curr_state.board[i] != goal_state.board[i]:
            final_loc = goal_state.board.index(curr_state.board[i])
            row_moves = abs(i // 4 - final_loc // 4)
            col_moves = abs(i % 4 - final_loc % 4)
            h += row_moves + col_moves
    return h

start = State([1,5,2,3,4,6,0,7,8,9,10,11,12,13,14,15,16,17,18,19])
goal = State([1,2,0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19])

open_list = PriorityQueue()
closed_list = []
open_list.put(start)

while not open_list.empty():
    curr = open_list.get()
    if curr in closed_list:
        continue

    print(curr)
    print()
    if curr == goal:
        print("Done")
        break
    else:
        neighbors = curr.expand_state()
        [open_list.put(n) for n in neighbors]
