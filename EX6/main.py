import matplotlib.pyplot as plt
from enum import Enum

# S - Starting position
# X - Wall
# O - Open Space
# E - Ending

class Type(Enum):
    CLEAR = 0
    START = 1
    WALL = 2
    ENDING = 3


class Node:
    type: Type
    utility: float

    def __init__(self, type, utility):
        self.type = type
        self.utility = utility

    def __str__(self):
        return f"{self.type} ({self.utility})"

    def __repr__(self):
        return f"{self.type} ({self.utility})"


class Action(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Edge():
    action: Action
    weight: float
    to: Node

    def __init__(self, action, weight, to):
        self.action = action
        self.weight = weight
        self.to = to

    def __str__(self):
        return f"{self.action} -({self.weight})-> {self.to}"

    def __repr__(self):
        return f"{self.action} -({self.weight})-> {self.to}"


def is_position_valid(pos):
    return 3 > pos[0] >= 0 and 4 > pos[1] >= 0


def get_empty_map(base_utility):
    return [[Node(Type.CLEAR, base_utility), Node(Type.CLEAR, base_utility), Node(Type.CLEAR, base_utility), Node(Type.CLEAR, base_utility)], [Node(Type.CLEAR, base_utility), Node(Type.CLEAR, base_utility), Node(Type.CLEAR, base_utility), Node(Type.CLEAR, base_utility)], [Node(Type.CLEAR, base_utility), Node(Type.CLEAR, base_utility), Node(Type.CLEAR, base_utility), Node(Type.CLEAR, base_utility)]]


def add_starting_pos(map, pos):
    if is_position_valid(pos):
        if map[pos[0]][pos[1]].type == Type.CLEAR:
            result = ""

            for i in range(len(map)):
                for j in range(len(map[i])):
                    if map[i][j].type == Type.START:
                        map[i][j].type = Type.CLEAR

                        result += f"Removed starting position from ({j}, {i})"
                        break

            map[pos[0]][pos[1]].type = Type.START

            return result + f"Starting position added in ({pos[1]}, {pos[0]})"
        else:
            return "Position already occupied!"
    else:
        return "Position invalid!"


def add_wall(map, pos):
    if is_position_valid(pos):
        if map[pos[0]][pos[1]].type == Type.CLEAR:
            map[pos[0]][pos[1]].type = Type.WALL

            return f"Wall added in ({pos[1]}, {pos[0]})"
        else:
            return "Position already occupied!"
    else:
        return "Position invalid!"


def clear_space(map, pos):
    if is_position_valid(pos):
        map[pos[0]][pos[1]].type = Type.CLEAR

        return f"Cleared space ({pos[1]}, {pos[0]})"
    else:
        return "Position invalid!"


def add_ending(map, pos, utility):
    if is_position_valid(pos):
        if map[pos[0]][pos[1]].type == Type.CLEAR:
            map[pos[0]][pos[1]].type = Type.ENDING
            map[pos[0]][pos[1]].utility = utility

            return f"Ending with associated score {utility} added in ({pos[1]}, {pos[0]})"
        else:
            return "Position already occupied!"
    else:
        return "Position invalid!"


def set_utility(map, pos, utility):
    if is_position_valid(pos):
        map[pos[0]][pos[1]].utility = utility

        return f"Set utility {utility} in ({pos[1]}, {pos[0]})"
    else:
        return "Position invalid!"


def print_matrix(m):
    for line in m:
        print(line)


def action_to_vector(action: Action):
    if action == Action.UP:
        return [-1, 0]
    elif action == Action.RIGHT:
        return [0, 1]
    elif action == Action.DOWN:
        return [1, 0]
    elif action == Action.LEFT:
        return [0, -1]


def get_action_mapping(action:Action):
    if action == Action.UP:
        return [[Action.UP, 0.8], [Action.LEFT, 0.1], [Action.RIGHT, 0.1]]
    elif action == Action.RIGHT:
        return [[Action.RIGHT, 0.8], [Action.UP, 0.1], [Action.DOWN, 0.1]]
    elif action == Action.DOWN:
        return [[Action.DOWN, 0.8], [Action.LEFT, 0.1], [Action.RIGHT, 0.1]]
    elif action == Action.LEFT:
        return [[Action.LEFT, 0.8], [Action.UP, 0.1], [Action.DOWN, 0.1]]


def get_action_result(map, pos, action: Action):
    v = action_to_vector(action)
    if is_position_valid([pos[0] + v[0], pos[1] + v[1]]):
        resulting_node = map[pos[0] + v[0]][pos[1] + v[1]]

        if resulting_node.type != Type.WALL:
            return resulting_node
    return None


def build_graph(map):
    G = {}

    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j].type != Type.WALL:
                G[map[i][j]] = []

                for action_taken in [Action.UP, Action.RIGHT, Action.LEFT, Action.DOWN]:
                    for action_and_weight in get_action_mapping(action_taken):
                        result = get_action_result(map, [i, j], action_and_weight[0])

                        if not result is None:
                            G[map[i][j]].append(Edge(action_and_weight[0], action_and_weight[1], result))

    return G

base_utility = float(input("Set base utility\n"))

map = get_empty_map(base_utility)

print_matrix(map)
command = input("S {x} {y} - ADD STARTING POSITION\nX {x} {y} ADD WALL\nE {x} {y} {utility} - ADD ENDING\nC {x} {y} - CLEAR SPACE\nU {x} {y} {utility} - SET TILE UTILITY\nG - BUILD GRAPH\n").upper().split()
while command[0] != "G":
    if command[0] == "S":
        print(add_starting_pos(map, [int(command[2]), int(command[1])]))
    elif command[0] == "X":
        print(add_wall(map, [int(command[2]), int(command[1])]))
    elif command[0] == "E":
        print(add_ending(map, [int(command[2]), int(command[1])], float(command[3])))
    elif command[0] == "C":
        print(clear_space(map, [int(command[2]), int(command[1])]))
    elif command[0] == "U":
        print(set_utility(map, [int(command[2]), int(command[1])], float(command[3])))
    else:
        print(f"{command[0]} is not a valid command")

    print_matrix(map)
    command = input("S {x} {y} - ADD STARTING POSITION\nX {x} {y} ADD WALL\nE {x} {y} {utility} - ADD ENDING\nC {x} {y} - CLEAR SPACE\nU {x} {y} {utility} - SET TILE UTILITY\nG - BUILD GRAPH\n").upper().split()

G = build_graph(map)
print(G)