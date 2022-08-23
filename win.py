import random
import time

import pygame.sprite
from constants import *


class Win:
    def __init__(self, win):
        self.game_is_on = True
        self.win = win
        self.s_list = list()
        self.color = WHITE
        self.init_list(50)

    def run(self):
        clock = pygame.time.Clock()
        moves = quicksort(self.s_list)
        print(len(moves))
        i = 0

        while self.game_is_on:
            self.win.fill(BLACK)
            dt = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_on = False
            if i < len(moves):
                self.swap(moves, i)
                i += 1
            if i == len(moves):
                self.color = GREEN
            self.draw(self.win)

    def draw(self, win):
        BOT = 700
        LEFT = 60
        RIGHT = 1400
        max_height = 500
        n = len(self.s_list)
        for i, l in enumerate(self.s_list):
            L = l * max_height / len(self.s_list)
            left = LEFT + i * (RIGHT - LEFT) / n
            top = BOT - L
            width = (RIGHT - LEFT) / n - 1
            height = L
            pygame.draw.rect(win, self.color, [left, top, width, height])
        pygame.display.flip()

    def init_list(self, n):
        self.s_list = [i for i in range(1, n)]
        random.shuffle(self.s_list)

    def swap(self, swaps, num):
        i, j = swaps[num]
        self.s_list[i], self.s_list[j] = self.s_list[j], self.s_list[i]


def bubble_sort(og_l):
    moves = []
    L = og_l[:]
    n = len(L)
    for i in range(n):
        for j in range(n - i - 1):
            if L[j] > L[j + 1]:
                L[j], L[j + 1] = L[j + 1], L[j]
                moves.append((j, j + 1))
    return moves


def tri_insertion(og_l):
    L = og_l[:]
    n = len(L)
    moves = []
    for i in range(1, n):
        e = L[i]
        j = i - 1
        while j >= 0 and e < L[j]:
            L[j + 1] = L[j]
            moves.append((j + 1, j))
            j -= 1
        L[j + 1] = e
    return moves


def quicksort(og_l):
    L = og_l[:]
    n = len(L)
    return qs(0, n - 1, L, [])


def qs(left, right, nums, changes):
    if len(nums) == 1:  # Terminating Condition for recursion. VERY IMPORTANT!
        return
    if left < right:
        pi, swaps = partition(left, right, nums)
        changes.extend(swaps)
        qs(left, pi - 1, nums, changes)
        qs(pi + 1, right, nums, changes)
    return changes


def partition(left, right, nums):
    swaps = []
    pivot, ptr = nums[right], left
    for i in range(left, right):
        if nums[i] <= pivot:
            if i != ptr:
                nums[i], nums[ptr] = nums[ptr], nums[i]
                swaps.append((i, ptr))
            ptr += 1
    if right != ptr:
        nums[ptr], nums[right] = nums[right], nums[ptr]
        swaps.append((ptr, right))
    return ptr, swaps
