from itertools import combinations
from collections import deque


def max_number_divby3(num_l):
    """
    If the sum of the digits in a number is divisible by 3, then that number is also divisible by 3
    :param num_l: list of ints
    :return: int
    """
    num_l.sort(reverse=True)
    for i in reversed(range(1, len(num_l) + 1)):
        for combo_t in combinations(num_l, i):
            if sum(combo_t) % 3 == 0:
                return int(''.join(map(str, combo_t)))
    return 0


# A node is a coordinate point plus a distance
class Node(object):
    def __init__(self, pt, dist):
        self.pt = pt
        self.dist = dist


# future consideration:  refactor to eliminate the Cell class
class Cell:

    def __init__(self, x=0, y=0, dist=0):
        self.x = x
        self.y = y
        self.dist = dist


class Point(object):
    def __init__(self, x, y, layer=0):
        self.x = x
        self.y = y
        self.layer = layer
        self.up = x, y + 1, layer
        self.down = x, y - 1, layer
        self.right = x + 1, y, layer
        self.left = x - 1, y, layer

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def neighbors(self):
        return [self.up, self.down, self.right, self.left]

def is_inside(x, y, board_size):
    """
    returns True if the curr cell is inside the chess board-matrix
    :param x:
    :param y:
    :param board_size:
    :return:
    """
    if (1 <= x <= board_size and y >= 1 and y <= board_size):
        return True
    return False


def min_knight_moves(knightsrc, knightdest):
    """
    return minimum chess knight moves required on a chess board given starting point and destination
    :param knightsrc: int
    :param knightdest: int
    :return: int
    """
    knightpos = [0 for x in range(2)]
    targetpos = [0 for x in range(2)]
    board_size = 8
    # convert source & destination numbers to row and column coordinates that start from 1
    knightpos[0] = knightsrc % board_size + 1
    knightpos[1] = knightsrc // board_size + 1
    targetpos[0] = knightdest % board_size + 1
    targetpos[1] = knightdest // board_size + 1
    # all possible cardinal movements for the knight
    dx = [2, 2, -2, -2, 1, 1, -1, -1]
    dy = [1, -1, 1, -1, 2, -2, 2, -2]

    # push starting position of knight with 0 distance
    cells_queue = [Cell(knightpos[0], knightpos[1], 0)]

    # make all cells unvisited
    visited = [[False for i in range(board_size + 1)] for j in range(board_size + 1)]

    # visit starting state
    visited[knightpos[0]][knightpos[1]] = True

    # loop until we have one element in queue
    while len(cells_queue) > 0:

        curr_cell = cells_queue[0]
        cells_queue.pop(0)

        # if current cell is equal to target cell, return its distance
        if (curr_cell.x == targetpos[0] and curr_cell.y == targetpos[1]):
            return curr_cell.dist

        # iterate over all reachable cells
        for i in range(board_size):

            x = curr_cell.x + dx[i]
            y = curr_cell.y + dy[i]

            if is_inside(x, y, board_size) and not visited[x][y]:
                visited[x][y] = True
                cells_queue.append(Cell(x, y, curr_cell.dist + 1))


def is_valid(row, col, height, width):
    return (0 <= row < height) and (0 <= col < width)


def min_cubicle_path(grid_map):
    """
    :param grid_map:
    :return: int (# of steps)
    grid_map = [
        [0, 1, 1, 0],
        [0, 0, 0, 1],
        [1, 1, 0, 0],
        [1, 1, 1, 0]
    ])
    1's represent walls, 0's are passable
    solution solves for the shortest path from 0,0 (src) to height-1,width-1 (destination) and returns
    number of steps required (incl. src and destination), while eliminating at most one wall.

    Implementation via a BFS approach with a double layered graph.

    Graphs:
        - base graph (i.e. layer 0) represents paths, where no walls have been hit.
        - shadow graph (i.e. layer 1) represents paths, where exactly one wall has been hit.

    Discovery of nodes:
        - in layer 0 walls can be discovered.
        - in layer 1 walls are ignored (as a wall has already been hit)

    Marking nodes as visited
        - node discovered during the traversal of the base graph -> mark visited for layer 0 and layer 1
          (as it is strictly better to discover a node without hitting a wall first)
        - node discovered during traversal of the shadow graph -> mark visited for layer 1 only

    Transitions between layers:
        - from layer 0 to layer 1 is possible exactly and only when a wall is hit.
        - back from layer 1 to layer 0 is not possible.
    """

    height, width = (len(grid_map), len(grid_map[0]))
    src_point = Point(x=0, y=0)
    dest_point = Point(x=width - 1, y=height - 1)

    # visited[0] = layer 0; visited[1] = layer 1
    visited = [
        [[False for i in range(width)] for j in range(height)],
        [[False for i in range(width)] for j in range(height)]
    ]

    nodes_queue = deque([Node(src_point, 0)])
    while nodes_queue:
        curr = nodes_queue.popleft()
        pt = curr.pt

        if pt == dest_point:
            return curr.dist + 1

        for x, y, layer in pt.neighbors():
            if layer == 0:
                if is_valid(y, x, height, width) and not visited[0][y][x]:
                    visited[0][y][x] = True
                    visited[1][y][x] = True

                    # move up to layer 1 when hitting a wall
                    adj_cell = Node(Point(x=x, y=y, layer=grid_map[y][x]), curr.dist + 1)
                    nodes_queue.append(adj_cell)
            elif layer == 1:
                if is_valid(y, x, height, width) and grid_map[y][x] == 0 and not visited[1][y][x]:
                    visited[1][y][x] = True
                    adj_cell = Node(Point(x=x, y=y, layer=1), curr.dist + 1)
                    nodes_queue.append(adj_cell)
            else:
                raise ValueError('Invalid layer: {}'.format(layer))
