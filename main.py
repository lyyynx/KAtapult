from game import TwoPlayerTankGame
from pyaxidraw import axidraw

if __name__ == "__main__":
    ad = axidraw.AxiDraw()
    ad.interactive()

    ad.options.model = 4  # minikit
    ad.options.pen_pos_up = 70
    ad.update_options()

    ad.connect()

    game = TwoPlayerTankGame(output=None)

    game.start_game()
