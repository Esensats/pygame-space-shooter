import pygame as pg
from sys import exit

pg.init()
screen = pg.display.set_mode((800, 400))
pg.display.set_caption("Hello, world!")

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            exit()

    pg.display.update()
