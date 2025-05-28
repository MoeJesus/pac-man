import pyxel
import enum

# Global variable for where the tiles for the wall start
WALL_TILE_X = 8


# Ghost direction labels
class Direction(enum.Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class Ghost:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.center_x = self.x + 7
        self.center_y = self.y + 7
        # self.target = target
        self.dx = 0
        self.dy = 0
        self.ghost_direction = Direction.UP
        # self.dead = dead
        # self.in_box = box
        self.id = id
        # self.turns, self.in_box = self.check_collisions()
        # self.rect = self.draw_ghost()

        if self.id == 0: # Blinky
            self.ghost_image = [32, 48, 16, 16]
            self.direction = Direction.LEFT
        elif self.id == 1: # Pinky
            self.ghost_image = [32, 64, 16, 16]
            self.direction = Direction.DOWN
        elif self.id == 2: # Inky
            self.ghost_image = [32, 80, 16, 16]
            self.direction = Direction.UP
        elif self.id == 3: # Clyde
            self.ghost_image = [32, 96, 16, 16]
            self.direction = Direction.UP


    def draw_ghost(self, direction):
        sprite_x = self.ghost_image[0]
        sprite_y = self.ghost_image[1]
        width = self.ghost_image[2]
        height = self.ghost_image[3]

        if self.direction == Direction.UP:
            sprite_x = ((pyxel.frame_count // 8 % 2) + 2) * 16
        elif self.direction == Direction.DOWN:
            sprite_x = ((pyxel.frame_count // 8 % 2) + 4) * 16
        elif self.direction == Direction.LEFT:
            sprite_x = pyxel.frame_count // 8 % 2 * 16
            width = width * -1
        elif self.direction == Direction.RIGHT:
            sprite_x = pyxel.frame_count // 8 % 2 * 16
            
        pyxel.blt(self.x, self.y, 0, sprite_x, sprite_y, width, height)

    def update_ghost(self):
            if pyxel.btn(pyxel.KEY_UP):
                self.direction = Direction.UP
            elif pyxel.btn(pyxel.KEY_DOWN):
                self.direction = Direction.DOWN
            elif pyxel.btn(pyxel.KEY_LEFT):
                self.direction = Direction.LEFT
            elif pyxel.btn(pyxel.KEY_RIGHT):
                self.direction = Direction.RIGHT