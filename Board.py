from random import randint
from Vertice import *

SCALE = 2

BOARD_WIDTH = 12 * SCALE + 1
BOARD_HEIGHT = 12 * SCALE + 1
TILE_WIDTH = 64 / SCALE
TILE_HEIGHT = 32 / SCALE
OFFSET_X = 25
OFFSET_Y = 400

RAIN = False
RAIN_TIMER = 3
RAIN_FORCE = 25


class Board(object):
    def __init__(self):
        self.vertices = [[Vertice(x, y) for y in range(BOARD_HEIGHT)] for x in range(BOARD_WIDTH)]
        # self.random_vertices_heights()
        self.calculate_vertices_coordinates()
        self.is_propagating = True
        self.timer = 0

    def update(self):
        if RAIN:
            self.timer += 1
            if self.timer > RAIN_TIMER:
                self.rain()
                self.timer = 0

        if self.is_propagating:
            self.propagate_wave()
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                self.vertices[x][y].update()

        self.calculate_vertices_coordinates()

    def calculate_vertices_coordinates(self):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                self.vertices[x][y].disp_x = TILE_WIDTH * (x + y) + OFFSET_X
                self.vertices[x][y].disp_y = (TILE_HEIGHT * (y - x)) - self.vertices[x][y].height + OFFSET_Y

    def find_closest_vertice(self, x, y):
        closest_dist = self.dist(x, y, self.vertices[0][0].disp_x, self.vertices[0][0].disp_y)
        closest_vertice = self.vertices[0][0]
        for i in range(BOARD_WIDTH):
            for j in range(BOARD_HEIGHT):
                dist = self.dist(x, y, self.vertices[i][j].disp_x, self.vertices[i][j].disp_y)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_vertice = self.vertices[i][j]
        return closest_vertice

    def drop(self, x, y, intensity):
        self.vertices[x][y].velocity -= intensity
        if x < BOARD_WIDTH - 1: self.vertices[x + 1][y].velocity -= intensity / 1.8
        if x > 0: self.vertices[x - 1][y].velocity -= intensity / 1.8
        if y < BOARD_HEIGHT - 1: self.vertices[x][y + 1].velocity -= intensity / 1.8
        if y > 0: self.vertices[x][y - 1].velocity -= intensity / 1.8

    def wave(self):
        for x in range(BOARD_WIDTH):
            self.drop(x, 0, -100)

    def rain(self):
        x = randint(0, BOARD_WIDTH-1)
        y = randint(0, BOARD_HEIGHT-1)
        self.drop(x, y, RAIN_FORCE)

    def STOP_EVERYTHING(self):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                self.vertices[x][y].velocity = 0
                self.vertices[x][y].acceleration = 0
                self.vertices[x][y].height /= 2

    def propagate_wave(self):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                h = self.vertices[x][y].height
                delta = 0
                if x < BOARD_WIDTH - 1:
                    delta += self.vertices[x + 1][y].height - h
                if x > 0:
                    delta += self.vertices[x - 1][y].height - h
                if y < BOARD_HEIGHT - 1:
                    delta += self.vertices[x][y + 1].height - h
                if y > 0:
                    delta += self.vertices[x][y - 1].height - h
                delta *= SPREAD_FACTOR
                self.vertices[x][y].velocity += delta

    def dist(self, x1, y1, x2, y2):
        return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
