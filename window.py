import random
import time

import pygame.sprite
from PygameUIKit import Group
from PygameUIKit.button import ButtonText

from constants import *
from colour import Color
import pygame.color
from sorting import insertion_sort_yield, bubble_sort_yield, quicksort
from PygameUIKit.dropdown import ComboBox

yield_sorters = {
    "Bubble Sort": bubble_sort_yield,
    "Insertion Sort": insertion_sort_yield,
}

list_sorters = {
    "Quick Sort": quicksort
}


def swap(L, move):
    i, j = move
    L[i], L[j] = L[j], L[i]


class Sorter:
    def __init__(self, win):
        self.game_is_on = True
        self.is_sorting = False
        self.is_end = False
        self.win = win
        self.the_list_to_sort = list()
        start = Color("blue")
        self.generator = bubble_sort_yield(self.the_list_to_sort)
        self.n = 1000
        self.start_grad = list(start.range_to(Color("red"), self.n + 1))
        self.grad = self.start_grad.copy()
        self.reset_list(self.n)

        # UI
        self.ui_group = Group()
        self.combo_box = ComboBox(list(yield_sorters.keys()) + list(list_sorters.keys()),
                                  ui_group=self.ui_group, font_color=pygame.Color("white"))
        self.btn_start = ButtonText(ui_group=self.ui_group, text="Start", onclick_f=self.start_sorting,
                                    rect_color=pygame.Color("darkgreen"), border_radius=5)
        self.btn_shuffle = ButtonText(ui_group=self.ui_group, text="Shuffle", onclick_f=lambda: self.reset_list(self.n),
                                      rect_color=pygame.Color("blue"), border_radius=5)

    def run(self):
        clock = pygame.time.Clock()
        while self.game_is_on:
            self.win.fill(pygame.Color(33, 37, 43))
            clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                self.ui_group.handle_event(event)
                if event.type == pygame.QUIT:
                    self.game_is_on = False

            if self.is_sorting:
                try:
                    # we slow down the animation for quick sort because it's too fast
                    speed = self.n // 5 if self.combo_box.get_value() != "Quick Sort" else self.n // 100
                    for _ in range(speed):
                        swap(self.the_list_to_sort, next(self.generator))
                except StopIteration:
                    self.is_end = True
            if self.is_end:
                self.end_animation()
            self.draw(self.win)

    def draw(self, win):
        n = len(self.the_list_to_sort)
        BOT = 700
        LEFT = 60
        RIGHT = 1400
        max_height = 500
        for i, l in enumerate(self.the_list_to_sort):
            L = l * max_height / len(self.the_list_to_sort)
            left = LEFT + i * (RIGHT - LEFT) / n
            top = BOT - L
            width = (RIGHT - LEFT) / n + 1
            height = L
            r, g, b = self.grad[l].rgb[0] * 255, self.grad[l].rgb[1] * \
                      255, self.grad[l].rgb[2] * 255
            pygame.draw.rect(win, (r, g, b), [left, top, width, height], 0)

        # UI
        self.btn_start.draw(win, 50, 50)
        self.btn_shuffle.draw(win, 50, 100)
        self.combo_box.draw(win, 50, 150)
        pygame.display.flip()

    def end_animation(self):
        self.is_sorting = False
        # if variable is not defined, create it
        if not hasattr(self, 'start_time'):
            start = Color("lightgreen")
            self.new_grad = list(start.range_to(Color("darkgreen"), len(self.the_list_to_sort) + 1))
            self.i = 0
            self.start_time = time.time()

        for _ in range(self.n // 100):
            if self.i == len(self.the_list_to_sort) + 1:
                self.is_end = False
                return
            self.grad[self.i] = self.new_grad[self.i]
            self.i += 1

    def reset_list(self, n):
        self.is_sorting = False
        self.is_end = False
        self.i = 0

        self.grad = self.start_grad.copy()
        self.the_list_to_sort = [i for i in range(1, n)]
        random.shuffle(self.the_list_to_sort)

    def start_sorting(self):
        txt = self.combo_box.get_value()

        if txt in yield_sorters:
            self.generator = yield_sorters[txt](self.the_list_to_sort)
        else:
            moves_list = list_sorters[txt](self.the_list_to_sort)
            self.generator = iter(moves_list)

        self.is_sorting = True

    def set_generator(self, f):
        self.generator = f(self.the_list_to_sort)


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sorting Algorithms")
    window = Sorter(win)
    window.run()
    pygame.quit()
