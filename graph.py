from abc import ABC, abstractmethod
OBSTACLE = 'X'
AVAILABLE = 'A'
VISITED = 'V'

class Grid:
    def __init__(self, maxX: int, maxY: int, obstacles: set) -> None:
        self.maxX = maxX
        self.maxY = maxY
        self.obstacles = obstacles

    def __str__(self) -> None:
        tp = ''
        for x in range(self.maxX):
            for y in range(self.maxY):
                if (x,y) in self.obstacles:
                    tp += f'{OBSTACLE} '
                else:
                    tp += f'{AVAILABLE} '
            tp += '\n'
        return tp

class Traversal(ABC):
    def __init__(self, grid, st = (0,0) , target = None):
        self.grid = grid
        self.starting_point = st
        self.visited = set([st])

    def in_bound(self, x : int,y: int) -> bool:
        if (x < 0 or x >= self.grid.maxX) or (y <0 or y >= self.grid.maxY):
            return False
        return True

    def __str__(self):
        tp = ''
        for x in range(self.grid.maxX):
            for y in range(self.grid.maxY):
                if (x,y) in self.grid.obstacles:
                    tp += f'{OBSTACLE} '
                elif (x,y) in self.visited:
                    tp += f'{VISITED} '
                else:
                    tp += f'{AVAILABLE} '
            tp += '\n'
        return tp

    @abstractmethod
    def traverse(self):
        pass

class BFS(Traversal):
    def __init__(self, grid, st=(0,0) , target= None):
        super().__init__(grid, st, target)
        self.queue = [self.starting_point]

    def traverse(self):
        try:
            curr = self.queue.pop(0) # get 1st element
        except IndexError as e:
            yield None
        # print(curr)
        self.visited.add(curr)
        # print(self.visited)
        adj = [(curr[0] + 1, curr[1]), (curr[0], curr[1] + 1), (curr[0] - 1, curr[1]) , (curr[0] , curr[1] - 1)]
        for x in adj:
            if self.in_bound(x[0], x[1]) and not x in self.visited and x not in self.grid.obstacles and x not in self.queue:
                self.queue.append(x)
        yield curr

class DFS(Traversal):
    def __init__(self, grid, st=(0,0) , target= None):
        super().__init__(grid, st, target)
        self.stack = [self.starting_point]

    def traverse(self):
        try:
            curr = self.stack.pop(0) # get 1st element
        except IndexError as e:
            yield None
        self.visited.add(curr)
        adj = [(curr[0] + 1, curr[1]), (curr[0], curr[1] + 1), (curr[0] - 1, curr[1]) , (curr[0] , curr[1] - 1)]
        for x in adj:
            if self.in_bound(x[0], x[1]) and not x in self.visited and x not in self.grid.obstacles and x not in self.stack:
                self.stack.insert(0, x)
        yield curr

def test_grid():
    a = Grid(5,5, set([(1,1), (2,2) , (3,3)]))
    b = BFS(a)
    while 1:
        n = next(b.traverse())
        if n is None:
            break
        print(b)

if __name__ == '__main__':
    test_grid()
