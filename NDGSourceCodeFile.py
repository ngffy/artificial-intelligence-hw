from queue import PriorityQueue

class State():
    # By default, the f, g, h, and priority values are decided by BFS
    def __init__(self, board, parent=None, g=0):
        self.board = board
        self.id = hash(self.board)

        if parent is not None:
            self.parent_id = parent.id
            self.priority = parent.priority + 1
        else:
            self.parent_id = 0
            self.priority = 0

        self.g = g
        self.h = 0
        self.f = self.g + self.h

    # Allows setting new values for f, g, h, and priority if using A*
    def set_priority(self, goal, heuristic):
        self.h = heuristic(self, goal)
        self.f = self.g + self.h
        self.priority = self.f

    # Returns a list of the indices of tiles that can be moved
    def get_movable_tiles(self, i):
        on_top_edge = i in range(0, 4)
        on_left_edge = i in range(0, 20, 4)
        on_right_edge = i in range(3, 24, 4)
        on_bot_edge = i in range(16, 20)

        movable_tiles = []
        if not on_top_edge:
            movable_tiles.append(i-4)
        if not on_left_edge:
            movable_tiles.append(i-1)
        if not on_right_edge:
            movable_tiles.append(i+1)
        if not on_bot_edge:
            movable_tiles.append(i+4)

        return movable_tiles

    def expand_state(self):
        empty_slot = self.board.index(0)
        movable_tiles = self.get_movable_tiles(empty_slot)

        neighbors = [list(self.board) for i in movable_tiles]
        for n in neighbors:
            tile_slot = movable_tiles.pop()
            n[empty_slot], n[tile_slot] = n[tile_slot], n[empty_slot]

        cost = self.g + (1 if n[empty_slot] < 10 else 2)
        new_states = [State(tuple(n), self, cost) for n in neighbors]

        return new_states

    def pretty_board(self):
        s = ""
        for i in range(0, 20, 4):
            s += f"%2d %2d %2d %2d\n" % self.board[i:i+4]
        return s[:-1]

    def __str__(self):
        funcs = "f: "+str(self.f)+" g: "+str(self.g)+" h: "+str(self.h)
        pid = "\nParent ID: "+str(self.parent_id)
        prior = "\npriority: "+str(self.priority)
        return "ID "+str(self.id)+":\n"+self.pretty_board()+"\n"+funcs+pid+prior

    # == is overloaded to allow easy comparison to the goal state
    def __eq__(self, other):
        return self.board == other.board

    # All the inequality operators are overloaded so the priority queue works
    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    # Defined so State objects can be put in sets
    def __hash__(self):
        return hash(self.board)

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

# Recursively traces the given state back up to the start state and returns
# list of intermediate states
def unwind(state, start, visited):
    if state != start:
        for v in visited:
            if v.id == state.parent_id:
                return unwind(v, start, visited) + [state]
    return [state]

def search(start, goal, heuristic=None):
    open_list = PriorityQueue()
    closed_list = set()
    open_list.put(start)

    added_to_open = 1
    added_to_closed = 0

    while not open_list.empty():
        curr = open_list.get()
        if curr in closed_list:
            continue

        if curr == goal:
            break

        closed_list.add(curr)
        added_to_closed += 1

        if added_to_closed >= 300000:
            print("Checked about 300,000 states and did not find the goal")
            return

        neighbors = curr.expand_state()
        for n in neighbors:
            if heuristic is not None:
                n.set_priority(goal, heuristic)
            open_list.put(n)
            added_to_open += 1

    path = unwind(curr, start, closed_list)

    for s in path:
        print(s)
        print()

    print("Moves:", len(path)-1)
    print("States added to open list:", added_to_open)
    print("States added to closed list:", added_to_closed)
    print()

start = State((1,5,2,3,4,6,0,7,8,9,10,11,12,13,14,15,16,17,18,19))
goal = State((1,2,0,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19))

print("RUNNING BREADTH FIRST SEARCH")
search(start, goal)

print("RUNNING A* SEARCH WITH HEURISTIC ONE")
search(start, goal, heuristic_one)

print("RUNNING A* SEARCH WITH HEURISTIC TWO")
search(start, goal, heuristic_two)
