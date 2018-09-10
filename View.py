from tkinter import *
from Board import *

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 800
SCANLINE_SPACE = 2

BG_COLOR = '#550055'
SCANLINES_COLOR = '#005555'


class View(object):
    def __init__(self, root):
        self.root = root
        self.board = Board()
        self.root.config(background='black')
        self.root.wm_title('Video Toy')
        self.canvas = Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, background='black',
                             highlightthickness=0, cursor='dot')
        self.canvas.bind('<Button-1>', self.left_click)
        self.canvas.bind('<Button-2>', self.middle_click)
        self.canvas.bind('<Button-3>', self.right_click)
        self.render()
        self.canvas.pack()

    def update(self):
        self.board.update()

    def render(self):
        self.canvas.delete('all')
        # self.draw_scanlines(SCANLINE_SPACE)
        self.draw_board()

    def draw_scanlines(self, space):
        for i in range(int(WINDOW_HEIGHT / space)):
            self.canvas.create_line(0, i * space, WINDOW_WIDTH, i * space, fill=SCANLINES_COLOR)

    def draw_board(self):
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                x1 = self.board.vertices[x][y].disp_x
                y1 = self.board.vertices[x][y].disp_y
                if x > 0:
                    x2 = self.board.vertices[x - 1][y].disp_x
                    y2 = self.board.vertices[x - 1][y].disp_y
                    color = self.determine_color(self.board.vertices[x][y].height, self.board.vertices[x - 1][y].height)
                    self.canvas.create_line(x1, y1, x2, y2, fill=color)
                if y > 0:
                    x2 = self.board.vertices[x][y - 1].disp_x
                    y2 = self.board.vertices[x][y - 1].disp_y
                    color = self.determine_color(self.board.vertices[x][y].height, self.board.vertices[x][y - 1].height)
                    self.canvas.create_line(x1, y1, x2, y2, fill=color)

    def determine_color(self, h1, h2):
        # return '#0f0'
        m = (h1 + h2) / 2
        x = (m + 2) / 6
        color = self.lerp(x, 125, 255)
        hex = '%x' % int(color)
        if hex.__len__() < 2:
            hex = '0' + hex
        return '#' + hex + '00' + hex

    def left_click(self, event):
        vertice = self.board.find_closest_vertice(event.x, event.y)
        self.board.drop(vertice.x, vertice.y, 20)

    def right_click(self, event):
        #self.board.wave()
        vertice = self.board.find_closest_vertice(event.x, event.y)
        self.board.drop(vertice.x, vertice.y, 200)

    def middle_click(self, event):
        self.board.wave()
        #self.board.is_propagating = not self.board.is_propagating
        #self.board.STOP_EVERYTHING()

    def lerp(self, x, a, b):
        if x < 0:
            x = 0
        if x > 1:
            x = 1
        return a + x * (b - a)
