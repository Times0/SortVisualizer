from constants import *
from win import Win

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Sort visualizer")
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Win(win)
    game.run()
