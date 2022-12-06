"""Stores all the constants related to files (images, fonts, audio...) of the game"""

import pygame as pg
import os
import lib.params as prm


class Image:
    YELLOW_SPACESHIP_IMAGE = pg.image.load(
        os.path.join("src", "assets", "img", "spaceship_yellow.png")
    ).convert_alpha()

    YELLOW_SPACESHIP = pg.transform.rotate(
        pg.transform.scale(YELLOW_SPACESHIP_IMAGE, prm.SPACESHIP_SIZE), 90
    )

    RED_SPACESHIP_IMAGE = pg.image.load(
        os.path.join("src", "assets", "img", "spaceship_red.png")
    ).convert_alpha()

    RED_SPACESHIP = pg.transform.rotate(
        pg.transform.scale(RED_SPACESHIP_IMAGE, prm.SPACESHIP_SIZE), -90
    )

    SPACE_IMAGE = pg.image.load(
        os.path.join("src", "assets", "img", "space.png")
    ).convert()
    SPACE_BG = pg.transform.scale(SPACE_IMAGE, (prm.WIDTH, prm.HEIGHT))


class Font:
    MAIN_400 = pg.font.SysFont("", 32)
