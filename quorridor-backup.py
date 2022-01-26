import itertools

board = []
message_board = []

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
    
    def movable_directions(self, pos):
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
    def __init__(self, name, pos, turn):
        self.name = name
        self.walls = 10
        self.pos = pos
        self.turn = turn
    
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
        moveable_directions = board.moveable_directions(self.pos)
        if set(moveable_directions) in (set('n', 's'), set('e', 'w')):
            x1, y1 = self.pos[0]
            x2, y2 = self.pos[1]
            opponent_ref = {
                'n': (x1, y2),
                'e': (x2, y1),
                's': (x2, y1),
                'w': (x1, y2)
            }
            if board.index(opponent_ref[direction]).player_status == True:
                return True
        else:
            return False

    def move(self, direction):
        x1, y1 = self.pos[0]
        x2, y2 = self.pos[1]
        if direction in board.movable_directions(self.pos):
            if self._double_move_possible(direction):
                move_by = 2
            else:
                move_by = 1
            move_ref = {
                'n': ((x1, y1+move_by), (x2, y2+move_by)),
                'e': ((x1+move_by, y1), (x2+move_by, y2)),
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
        

class Corner:
    def __init__(self, wall_status, player_status, pos):
        self.player_status = player_status
        self.wall_status = wall_status
        self.pos = pos
        self.x, self.y = pos

