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
        # self.eaten = eaten
        # self.in_box = box
        self.id = id
        # self.turns, self.in_box = self.check_collisions()

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


    def draw_ghost(self, direction, powered, powered_counter):
        sprite_x = self.ghost_image[0]
        sprite_y = self.ghost_image[1]
        width = self.ghost_image[2]
        height = self.ghost_image[3]

        if powered:
            if powered_counter >= 240 or (powered_counter <= 220 and powered_counter > 200) or (powered_counter <= 180 and powered_counter > 160) or (powered_counter <= 140 and powered_counter > 120) or (powered_counter <= 100 and powered_counter > 80) or (powered_counter <= 60 and powered_counter > 40) or (powered_counter <= 20):
                sprite_x = ((pyxel.frame_count // 8 % 2) + 6) * 16
                sprite_y = 48
            else:
                sprite_x = ((pyxel.frame_count // 8 % 2) + 6) * 16
                sprite_y = 64
        else:
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
        #self.rect = pyxel.rectb(self.x + 4, self.y + 4, 8, 8, 4)
        #return self.rect

    def update_ghost(self):
        if pyxel.btn(pyxel.KEY_W):
            if not self.is_colliding(self.x, self.y - 2):
                self.direction = Direction.UP
                self.dx = 0
                self.dy = -1
        elif pyxel.btn(pyxel.KEY_S):
            if not self.is_colliding(self.x, self.y + 2):
                self.direction = Direction.DOWN
                self.dx = 0
                self.dy = 1
        elif pyxel.btn(pyxel.KEY_A):
            if not self.is_colliding(self.x - 3, self.y):
                self.direction = Direction.LEFT
                self.dx = -1
                self.dy = 0
        elif pyxel.btn(pyxel.KEY_D):
            if not self.is_colliding(self.x + 3, self.y):
                self.direction = Direction.RIGHT
                self.dx = 1
                self.dy = 0

        self.x, self.y = self.push_back(self.x, self.y, self.dx, self.dy)

    # Helper functions to easily check for collisions to walls
    def is_colliding(self, x, y):
        x1 = (pyxel.floor(x) + 4) // 8
        y1 = (pyxel.floor(y) + 4) // 8
        x2 = (pyxel.ceil(x) + 11) // 8
        y2 = (pyxel.ceil(y) + 11) // 8
        for yi in range(y1, y2 + 1):
            for xi in range(x1, x2 + 1):
                if pyxel.tilemaps[0].pget(xi, yi)[0] >= WALL_TILE_X:
                    return True
        return False

    def push_back(self, x, y, dx, dy):
        for _ in range(pyxel.ceil(abs(dy))):
            step = max(-1, min(1, dy))
            if self.is_colliding(x, y + step):
                break
            y += step
            dy -= step
        for _ in range(pyxel.ceil(abs(dx))):
            step = max(-1, min(1, dx))
            if self.is_colliding(x + step, y):
                break
            x += step
            dx -= step
        return x, y