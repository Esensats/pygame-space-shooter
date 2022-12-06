from enum import Enum
import pygame as pg
import lib.params as prm


class Team(Enum):
    YELLOW = 1
    RED = 2


class TeamColor:
    YELLOW_COLOR = (255, 255, 0)
    RED_COLOR = (255, 0, 0)


class Screen:
    WIDTH = prm.WIDTH
    HEIGHT = prm.HEIGHT

    @classmethod
    def collide_rect(cls, rect: pg.Rect):
        return pg.Rect(0, 0, Screen.WIDTH, Screen.HEIGHT).colliderect(rect)
