""" Stores pretty much all important parameters of the game,
excluding images (they are in lib.img) """

import pygame as pg

WIDTH, HEIGHT = 1280, 720
WINDOW_TITLE = "Pygame space shooter"
FPS = 60

PLAYER_ACCELERATION = 0.125
PLAYER_SPEED = 8
PLAYER_MAX_VEL = 1  # Instead change PLAYER_SPEED

SPACESHIP_SIZE = (
    45,
    45,
)  # Ship's bounding box, not the img size. Related to spaceship sizes from lib.img

BORDER_THICKNESS = 5
BORDER = pg.Rect(WIDTH / 2 - BORDER_THICKNESS / 2, 0, BORDER_THICKNESS, HEIGHT)

BULLET_LIMIT = 3
