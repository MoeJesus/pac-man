import pyxel
import enum
from player import Player, Direction


# Game state labels
class GameState(enum.Enum):
    STARTING = 0
    RUNNING = 1
    DYING = 2
    POWERED_UP = 3
    GAME_WIN = 4
    GAME_OVER = 5


class App:
    def __init__(self):
        pyxel.init(224, 288, display_scale = 3, title = "Pac-Man", fps = 60)
        pyxel.load("assets/resources.pyxres")
        self.current_game_state = GameState.STARTING
        self.player = Player(pyxel.width / 2 - 8, pyxel.height / 2 + (7.5 * 8))
        self.player_direction = self.player.direction
        self.score = self.player.score
        self.cookie_counter = self.player.cookie_counter
        self.power = self.player.powered
        self.frames = 0
        self.start_stage()
        pyxel.run(self.update, self.draw)

    # Sets everything up to start the game
    def start_stage(self):
        self.init_tilemap()

    # Sets all cookies to be collectable
    def init_tilemap(self):
        for y in range(36):
            for x in range(28):
                if pyxel.tilemaps[0].pget(x, y) == (1, 0):
                    pyxel.tilemaps[0].pset(x, y, (2, 0))
                elif pyxel.tilemaps[0].pget(x, y) == (1, 1):
                    pyxel.tilemaps[0].pset(x, y, (2, 1))

    # Sets that the starting time is appropriate
    def starting_game(self):
        self.frames += 1
        if self.frames >= 240:
            self.current_game_state = GameState.RUNNING
            self.player.dx = -1
            self.frames = 0
            
    # Sets the game state on whether the player is powered up or not
    def check_power(self):
        if self.power == True:
            self.current_game_state = GameState.POWERED_UP
        else:
            self.current_game_state = GameState.RUNNING

    # Checks to see if all the cookies are eaten
    def check_win(self):
        if self.cookie_counter >= 244:
            self.current_game_state = GameState.GAME_WIN

    def update(self):
        if self.current_game_state == GameState.STARTING:
            self.starting_game()
        if self.current_game_state == GameState.RUNNING or self.current_game_state == GameState.POWERED_UP:
            self.player.update_player()
            self.score, self.cookie_counter, self.power = self.player.eat_cookies(self.player.x, self.player.y)
            self.check_power()
            self.check_win()

    def draw(self):
        pyxel.cls(0)
        self.player.draw_player(self.player_direction)
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height, 0)
        pyxel.text(0, 0, str(self.score), 7)
        pyxel.text(100, 0, str(self.player.power_counter), 7)
        pyxel.text(150, 0, str(self.current_game_state), 7)

App()

# https://s3.amazonaws.com/media-p.slid.es/uploads/565973/images/3452983/tiles.png

#############################################
#                To Do List                 #
# Makes lives counter and add it to the HUD #
# Draw ghost sprites                        #
# Create the AI for the ghosts              #
#                                           #
#                                           #
#                                           #
#############################################