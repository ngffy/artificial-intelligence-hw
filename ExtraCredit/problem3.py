class State():
    def __init__(self, r=-1, u=0):
        self.reward = r
        self.utility = u

    def __str__(self):
        return "(" + str(self.reward) + ", " + str(int(self.utility)) + ")"

class StateGrid():
    def __init__(self):
        self.grid = [[State(),State(),State(),State()],
                [State(-30),State(),State(-20),State()],
                [State(),State(),State(-30),State()],
                [State(100),State(),State(20),State()]]
        self.policy = [['','','',''],
                ['','','',''],
                ['','','',''],
                ['','','','']]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def get_index(self, state):
        r = 0
        c = 0
        for i in range(0, self.rows):
            if state in self.grid[i]:
                r = i
                c = self.grid[i].index(state)
                break
        return (r,c)

    def expected_move_utilities(self, state):
        r,c = self.get_index(state)
        if r > 0:
            up = self.grid[r-1][c].utility
        else:
            up = state.utility
        if r < self.rows-1:
            down = self.grid[r+1][c].utility
        else:
            down = state.utility
        if c > 0:
            left = self.grid[r][c-1].utility
        else:
            left = state.utility
        if c < self.cols-1:
            right = self.grid[r][c+1].utility
        else:
            right = state.utility

        up_move = .8*up + .1*left + .1*right
        down_move = .8*down + .1*left + .1*right
        left_move = .8*left + .1*down + .1*up
        right_move = .8*right + .1*up + .1*down

        return {'up': up_move, 'down': down_move, 'left': left_move, 'right':
                right_move}

    def bellman(self, state):
        expected_values = self.expected_move_utilities(state).values()
        return state.reward + .9*max(expected_values)

    def update_utilities(self):
        new_utilities = [[0]*self.cols for i in range(0, self.rows)]
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                new_utilities[i][j] = self.bellman(self.grid[i][j])

        for i in range(0, self.rows):
            for j in range(0, self.cols):
                self.grid[i][j].utility = new_utilities[i][j]

    def update_policy(self):
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                state = self.grid[r][c]
                expected_values = self.expected_move_utilities(state)
                best_move = max(expected_values, key=expected_values.get)
                if best_move == 'up':
                    self.policy[r][c] = '↑'
                elif best_move == 'down':
                    self.policy[r][c] = '↓'
                elif best_move == 'left':
                    self.policy[r][c] = '←'
                elif best_move == 'right':
                    self.policy[r][c] = '→'
                else:
                    self.policy[r][c] = '?'

    def update(self):
        self.update_utilities()
        self.update_policy()

    def disp_grid(self):
        for row in self.grid:
            print(row[0],row[1],row[2],row[3])

    def disp_policy(self):
        for row in self.policy:
            print(row)

problem_grid = StateGrid()

for i in range(0,10):
    problem_grid.update()
    problem_grid.disp_grid()
    problem_grid.disp_policy()
