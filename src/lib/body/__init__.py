from __future__ import annotations
from typing import List
import pygame as pg

from lib.general import Team


class Bullet:
    DEFAULT_SIZE = (10, 5)
    SPEED = 8

    def __init__(self, pos: pg.math.Vector2, team: Team, size=DEFAULT_SIZE):
        self.team = team
        self.rect = pg.Rect(pos.x, pos.y, size[0], size[1])

    def move(self):
        if self.team == Team.YELLOW:
            self.rect.x += Bullet.SPEED
        else:
            self.rect.x -= Bullet.SPEED

    def collide_player(self, player: pg.Rect):
        return self.rect.colliderect(player)

    @classmethod
    def handle_bullets(
        cls,
        yel_bullets: List[Bullet],
        red_bullets: List[Bullet],
        yellow: pg.Rect,
        red: pg.Rect,
    ) -> List[Team]:
        """Handles bullets movement, collisions with players

        Args:
            yel_bullets (List[Bullet]): list of yellow's bullets
            red_bullets (List[Bullet]): list of red's bullets
            yellow (pg.Rect): yellow's rect
            red (pg.Rect): red's rect

        Returns:
            List[Team]: list of damaged players in this frame, empty list if none.
        """
        damaged_players: List[Team] = []

        for bullet in yel_bullets:
            bullet.move()
            if bullet.collide_player(red):
                yel_bullets.remove(bullet)
                damaged_players.append(Team.RED)

        for bullet in red_bullets:
            bullet.move()
            if bullet.collide_player(yellow):
                red_bullets.remove(bullet)
                damaged_players.append(Team.YELLOW)

        return damaged_players
