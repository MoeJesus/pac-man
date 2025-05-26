import pyxel
import enum

# Global variable for where the tiles for the wall start
WALL_TILE_X = 8


# Player direction labels
class Direction(enum.Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.direction = Direction.LEFT
        self.player_image = [32, 48, 16, 16]  # u, v, w, h
        self.score = 0
        self.cookie_counter = 0
        self.powered = False
        self.power_counter = 0

    def draw_player(self, direction):
        sprite_x = self.player_image[0]
        sprite_y = self.player_image[1]
        width = self.player_image[2]
        height = self.player_image[3]

        if self.direction == Direction.UP:
            sprite_x = pyxel.frame_count // 4 % 4 * 16
            sprite_y = 32
        elif self.direction == Direction.DOWN:
            sprite_x = pyxel.frame_count // 4 % 4 * 16
            sprite_y = 32
            height = height * -1
        elif self.direction == Direction.LEFT:
            sprite_x = pyxel.frame_count // 4 % 4 * 16
            sprite_y = 16
            width = width * -1
        elif self.direction == Direction.RIGHT:
            sprite_x = pyxel.frame_count // 4 % 4 * 16
            sprite_y = 16
            
        pyxel.blt(self.x, self.y, 0, sprite_x, sprite_y, width, height)

    def update_player(self):
        if pyxel.btn(pyxel.KEY_UP):
            if not self.is_colliding(self.x, self.y - 2):
                self.direction = Direction.UP
                self.dx = 0
                self.dy = -1
        elif pyxel.btn(pyxel.KEY_DOWN):
            if not self.is_colliding(self.x, self.y + 2):
                self.direction = Direction.DOWN
                self.dx = 0
                self.dy = 1
        elif pyxel.btn(pyxel.KEY_LEFT):
            if not self.is_colliding(self.x - 3, self.y):
                self.direction = Direction.LEFT
                self.dx = -1
                self.dy = 0
        elif pyxel.btn(pyxel.KEY_RIGHT):
            if not self.is_colliding(self.x + 3, self.y):
                self.direction = Direction.RIGHT
                self.dx = 1
                self.dy = 0

        self.x, self.y = self.push_back(self.x, self.y, self.dx, self.dy)

        # If the player leaves the map on either end, they'll appear on the other side
        if self.x <= -16:
            self.x = pyxel.width
        elif self.x >= pyxel.width:
            self.x = -16

        # Checks to see if the player is powered up
        if self.powered == True and self.power_counter > 0:
            self.power_counter -= 1
        elif self.powered == True and self.power_counter <= 0:
            self.powered = False

    # Function for the player to eat cookies and add points
    def eat_cookies(self, x, y):
        x = x // 8 + .5
        y = y // 8 + 1
        if pyxel.tilemaps[0].pget(x, y) == (2, 0):
            pyxel.tilemaps[0].pset(x, y, (0, 0))
            self.score += 10
            self.cookie_counter += 1
        elif pyxel.tilemaps[0].pget(x, y) == (2, 1):
            pyxel.tilemaps[0].pset(x, y, (0, 0))
            self.score += 50
            self.cookie_counter += 1
            self.powered = True
            self.power_counter = 600
            # eaten_ghosts = [False, False, False, False]
        return self.score, self.cookie_counter, self.powered

    # Helper functions to easily check for collisions to walls
    def is_colliding(self, x, y):
        x1 = (pyxel.floor(x) + 4) // 8
        y1 = (pyxel.floor(y) + 4) // 8
        x2 = (pyxel.ceil(x) + 11) // 8
        y2 = (pyxel.ceil(y) + 11) // 8
        for yi in range(y1, y2 + 1):
            for xi in range(x1, x2 + 1):
                if pyxel.tilemaps[0].pget(xi, yi)[0] >= WALL_TILE_X or pyxel.tilemaps[0].pget(xi, yi) == (0, 1):
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