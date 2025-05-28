import pyxel


class HUD:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw_lives(self, lives):
        for i in range(lives):
            pyxel.blt((16 + 16 * i), 272, 0, 32, 0, 16, 16)