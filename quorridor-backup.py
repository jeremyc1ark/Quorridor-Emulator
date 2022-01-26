import itertools

board = []
message_board = []

class Corner:
    def __init__(self, wall_status, player_status, pos):
        self.player_status = player_status
        self.wall_status = wall_status
        self.pos = pos
        self.x, self.y = pos

class Board:
    def __init__(self):
        grid = 10*[10*['open']]
        for i in range(10):
            grid[i] = list(map(Corner, grid[i]))

        self.grid = grid
    
    def index(self, x, y):
        if x in range(10) and y in range(10):
            return self.grid[y][x]
    
    def _get_end_corners(self, corner):
        wall_status = corner.wall_status
        x, y = corner.pos
        if wall_status == 'vwall':
            return ((x, y+1), (x, y-1))
        elif wall_status == 'hwall':
            return ((x+1, y), (x-1, y))

    def _is_open(self, corner1, corner2):
        pos1 = corner1.pos
        pos2 = corner2.pos
        corner1_end_corners = self._get_end_corners(corner1)
        corner2_end_corners = self._get_end_corners(corner2)
        if pos1 in corner2_end_corners or pos2 in corner1_end_corners:
            return False
        return True
    
    def movable_directions_from_pos(self, pos):
        pos1, pos2 = pos
        corner1 = self.index(*pos1)
        corner2 = self.index(*pos2)
        x1, y1 = corner1.pos
        x2, y2 = corner2.pos
        nw, ne, se, sw = ((x1, y2), (x2, y2), (x2, y1), (x1, y1))
        side_dict = {
            'n': (nw, ne),
            'e': (ne, se),
            's': (se, sw),
            'w': (sw, nw)
        }
        sides = ['n', 'e', 's', 'w']
        return tuple(filter(lambda x: self._is_open(*side_dict[x]), sides))

    def _occupied_adjacent_corners(self, corner):
        x, y = corner.pos
        corner_list = [
            (x+1, y),
            (x-1, y),
            (x, y+1),
            (x, y-1)
        ]
        corner_list = list(map(lambda a: self.index(*a), corner_list))
        corners_of_concern = list(filter(lambda b: b.wall_status in ('hwall', 'vwall'), corner_list))
        return corners_of_concern
    
    def _get_end_corners(self, corner):
        x, y = corner.pos
        if corner.wall_status == 'hwall':
            return ((x-1, y), (x+1, y))
        elif corner.wall_status == 'vwall':
            return ((x, y-1), (x, y+1))
        return False
    
    def can_be_placed(self, corner, orientation):
        if corner.wall_status != open:
            return False
        if set(corner.pos).intersection(set([0, 9])):
            return False
        occupied_adjacent_corners = self._occupied_adjacent_corners(corner)
        orientation_ref = {
            'h': 'hwall',
            'v': 'vwall'
        }
        for c in occupied_adjacent_corners:
            if orientation_ref[orientation] == c.wall_status:
                if c.pos in self._get_end_corners(c):
                    return False
        return True
            
    
class Player:
    def __init__(self, name, pronoun, pos, turn):
        self.name = name
        self.walls = 10
        self.pos = pos
        self.turn = turn
        self.pronoun = pronoun
    
    def place_wall(self, pos, orientation):
        corner = board.index(*pos)
        if board.can_be_placed(corner, orientation):
            if orientation == 'h':
                corner.wall_status = 'hwall'
            elif orientation == 'v':
                corner.wall_status = 'vwall'
            self.walls -= 1
            self.turn = False
    
    def _double_move_possible(self, direction):
        movable_directions_from_pos = board.movable_directions_from_pos(self.pos)
        x1, y1 = self.pos[0]
        x2, y2 = self.pos[1]
        opponent_ref = {
            'n': ((x1, y2), (x2, y2+1)),
            'e': ((x2, y1), (x2+1, y2)),
            's': ((x1, y1-1), (x2, y1)),
            'w': ((x1-1, y1), (x1, y2))
        }
        opponent_corner = board.index(opponent_ref[direction])[0]
        if opponent_corner.player_status:
            if direction in board.movable_directions_from_pos(opponent_ref[direction]):


    def move(self, direction):
        x1, y1 = self.pos[0]
        x2, y2 = self.pos[1]
        if direction in board.movable_directions_from_pos(self.pos):
            if self._double_move_possible(direction):
                move_by = 2
            else:
                move_by = 1
            move_ref = {
                'n': ((x1, y1+1), (x2, y2+1)),
                'e': ((x1+1, y1), (x2+1, y2)),
                's': ((x1, y1-move_by), (x2, y2-move_by)),
                'w': ((x1-move_by, y1), (x2-move_by, y2))
            }
            if set([-1, 10]).intersection(itertools.chain(*move_ref[direction])):
                message_board.append("That move is not possible.")
            else:
                self.pos = move_ref[direction]
                self.turn = False
                new_pos1 = move_ref[direction][0]
                new_pos2 = move_ref[direction][1]
                board.index(new_pos1).player_status = True
                board.index(new_pos2).player_status = True
        else:
            message_board.append("That move is not possible.")
        


# Testing functions for right now
# Board
def _is_open(self, corner1, corner2):
    pos1 = corner1.pos
    pos2 = corner2.pos
    corner1_end_corners = self._get_end_corners(corner1)
    corner2_end_corners = self._get_end_corners(corner2)
    if pos1 in corner2_end_corners or pos2 in corner1_end_corners:
        return False
    return True

def movable_directions_from_pos(self, pos):
    pos1, pos2 = pos
    corner1 = self.index(*pos1)
    corner2 = self.index(*pos2)
    x1, y1 = corner1.pos
    x2, y2 = corner2.pos
    nw, ne, se, sw = ((x1, y2), (x2, y2), (x2, y1), (x1, y1))
    side_dict = {
        'n': (nw, ne),
        'e': (ne, se),
        's': (se, sw),
        'w': (sw, nw)
    }
    sides = ['n', 'e', 's', 'w']
    return list(filter(lambda x: self._is_open(*side_dict[x]), sides))

# Player
def _double_move_possible(self, direction):
    x1, y1 = self.pos[0]
    x2, y2 = self.pos[1]
    opponent_ref = {
        'n': ((x1, y2), (x2, y2+1)),
        'e': ((x2, y1), (x2+1, y2)),
        's': ((x1, y1-1), (x2, y1)),
        'w': ((x1-1, y1), (x1, y2))
    }
    opponent_corner = board.index(opponent_ref[direction])[0]
    if opponent_corner.player_status:
        possible_moves_from_opponent_pos = board.movable_directions_from_pos(opponent_ref[direction])
        if direction in possible_moves_from_opponent_pos:
            return list(f'{direction}{direction}')
        else:
            dir_dict = {
                'n': ['e', 'w'],
                'e': ['n', 's'],
                's': ['e', 'w'],
                'w': ['n', 's']
            }
            possible_moves = dir_dict[direction]
            possible_moves = list(filter(lambda x: x in possible_moves_from_opponent_pos, possible_moves))
            if possible_moves:
                possible_moves = list(map(lambda x: f'{direction}{x}', possible_moves))
                return possible_moves
            else:
                return False
    else:
        return False

def all_possible_moves_in_char_format(self):
    movable_directions_from_pos = board.movable_directions_from_pos(self.pos)
    possible_moves = []
    for direction in movable_directions_from_pos:
        double_move = self.double_move_is_possible(direction)
        if double_move:
            possible_moves.append(double_move)
        else:
            possible_moves.append(direction)
    return list(itertools.chain(*possible_moves))

def _combine_coords(c1, c2):
    x1, y1 = c1
    x2, y2 = c2
    return (x1+x2, y1+y2)

def all_possible_moves(self):
    lower = self.pos[0]
    upper = self.pos[1]
    move_ref = {
        'n': (0, 1),
        'e': (1, 0),
        's': (0, -1),
        'w': (-1, 0)
    }
    dir_list = self.all_possible_moves_in_char_format()
    pos_set = set()
    for dir in dir_list:
        move_by = (0, 0)
        for char in dir:
            move_by = self._combine_coords(move_by, move_ref[char])
        pos_set.add((self._combine_coords(lower, move_by), self._combine_coords(upper, move_by)))
    return pos_set

def move(self, proposed_pos):
    possible_moves = self.all_possible_moves()
    if proposed_pos in possible_moves:
        self.pos = proposed_pos
        self.turn = False
        message_board.append(f'{self.name} has moved {self.pronoun} piece to {self.pos}.')
    else:
        message_board.append(f'{self.name}, you cannot move your piece to {proposed_pos}')
