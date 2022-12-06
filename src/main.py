from typing import List, Optional, Sequence, Tuple
import pygame as pg
import lib.color as clr
from lib.body import Bullet
from lib.general import Team, TeamColor
import lib.params as prm

pg.init()
WIN = pg.display.set_mode((prm.WIDTH, prm.HEIGHT))

from lib.file import Image, Font

pg.display.set_caption(prm.WINDOW_TITLE)

PLAYER_WIN_EVENT = pg.USEREVENT + 1


def draw_window(
    yellow: pg.Rect, red: pg.Rect, yel_bullets: List[Bullet], red_bullets: List[Bullet]
) -> None:
    # WIN.fill(CLR["BACKGROUND"])
    WIN.blit(Image.SPACE_BG, (0, 0))
    pg.draw.rect(WIN, clr.Alias.BORDER, prm.BORDER)
    WIN.blit(Image.YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(Image.RED_SPACESHIP, (red.x, red.y))
    for bullet in yel_bullets:
        pg.draw.rect(WIN, TeamColor.YELLOW_COLOR, bullet.rect)
    for bullet in red_bullets:
        pg.draw.rect(WIN, TeamColor.RED_COLOR, bullet.rect)

    pg.display.update()


def draw_winner(player_win_text: pg.surface.Surface):
    WIN.blit(
        player_win_text,
        (prm.WIDTH // 2 - player_win_text.get_width() // 2, prm.HEIGHT // 3),
    )
    pg.display.update()
    pg.time.delay(3000)


def main() -> None:
    yellow = pg.Rect(
        prm.WIDTH / 4 - prm.SPACESHIP_SIZE[0] / 2,
        prm.HEIGHT / 2 - prm.SPACESHIP_SIZE[1] / 2,
        *prm.SPACESHIP_SIZE,
    )
    red = pg.Rect(
        prm.WIDTH / 4 * 3 - prm.SPACESHIP_SIZE[0] / 2,
        prm.HEIGHT / 2 - prm.SPACESHIP_SIZE[1] / 2,
        *prm.SPACESHIP_SIZE,
    )

    yellow_vec = pg.math.Vector2(0, 0)
    red_vec = pg.math.Vector2(0, 0)

    yel_health = 10
    red_health = 10

    yel_bullets: List[Bullet] = []
    red_bullets: List[Bullet] = []

    player_win_text = None

    clock = pg.time.Clock()
    run = True
    while run:
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                run = False
                pg.quit()
            if evt.type == PLAYER_WIN_EVENT:
                string = "Yellow won" if evt.team == Team.YELLOW else "Red won"
                player_win_text = Font.MAIN_400.render(string, True, clr.Alias.TEXT)
                draw_winner(player_win_text)
                run = False
                break
            if evt.type == pg.KEYDOWN:
                if evt.key == pg.K_SPACE and len(yel_bullets) < prm.BULLET_LIMIT:
                    yel_bullet_pos = pg.math.Vector2(
                        (
                            yellow.x + prm.SPACESHIP_SIZE[0] - Bullet.DEFAULT_SIZE[0],
                            yellow.y
                            + prm.SPACESHIP_SIZE[1] // 2
                            - Bullet.DEFAULT_SIZE[1] // 2,
                        )
                    )
                    yel_bullet = Bullet(
                        yel_bullet_pos,
                        team=Team.YELLOW,
                    )
                    yel_bullets.append(yel_bullet)
                if evt.key == pg.K_KP0 and len(red_bullets) < prm.BULLET_LIMIT:
                    red_bullet_pos = pg.math.Vector2(
                        (
                            red.x,
                            red.y
                            + prm.SPACESHIP_SIZE[1] // 2
                            - Bullet.DEFAULT_SIZE[1] // 2,
                        )
                    )
                    red_bullet = Bullet(
                        red_bullet_pos,
                        team=Team.RED,
                    )
                    red_bullets.append(red_bullet)

        handle_movement(yellow, red, pg.key.get_pressed(), yellow_vec, red_vec)
        damaged_players = Bullet.handle_bullets(yel_bullets, red_bullets, yellow, red)
        if Team.YELLOW in damaged_players:
            yel_health -= 1
            if yel_health <= 0:
                player_win(Team.RED)
        if Team.RED in damaged_players:
            red_health -= 1
            if red_health <= 0:
                player_win(Team.YELLOW)

        draw_window(yellow, red, yel_bullets, red_bullets)
        clock.tick(prm.FPS)
    print("Restart")
    main()


def player_win(team: Team):
    player_win_event = pg.event.Event(PLAYER_WIN_EVENT, {"team": team})
    pg.event.post(player_win_event)
    return team


def handle_movement(
    yellow: pg.Rect,
    red: pg.Rect,
    keys_pressed: Sequence[bool],
    yellow_vec: pg.math.Vector2,
    red_vec: pg.math.Vector2,
) -> None:

    """Handles both players movement (velocity, acceleration, normalization),
    and keeps them in bounds of their playable areas."""

    yellow_vel = handle_movement_velocity(
        keys_pressed, yellow_vec, (pg.K_a, pg.K_d, pg.K_w, pg.K_s)
    )
    red_vel = handle_movement_velocity(
        keys_pressed, red_vec, (pg.K_KP4, pg.K_KP6, pg.K_KP8, pg.K_KP5)
    )

    yellow.x += int(yellow_vel.x * prm.PLAYER_SPEED)
    yellow.y += int(yellow_vel.y * prm.PLAYER_SPEED)
    red.x += int(red_vel.x * prm.PLAYER_SPEED)
    red.y += int(red_vel.y * prm.PLAYER_SPEED)

    # playable area check:

    if yellow.x < 0:
        yellow.x = 0
    if yellow.y < 0:
        yellow.y = 0
    if yellow.x + prm.SPACESHIP_SIZE[0] > prm.WIDTH / 2:
        yellow.x = prm.WIDTH // 2 - prm.SPACESHIP_SIZE[0]
    if yellow.y + prm.SPACESHIP_SIZE[1] > prm.HEIGHT:
        yellow.y = prm.HEIGHT - prm.SPACESHIP_SIZE[1]

    if red.x < prm.WIDTH // 2:
        red.x = prm.WIDTH // 2
    if red.y < 0:
        red.y = 0
    if red.x + prm.SPACESHIP_SIZE[0] > prm.WIDTH:
        red.x = prm.WIDTH - prm.SPACESHIP_SIZE[0]
    if red.y + prm.SPACESHIP_SIZE[1] > prm.HEIGHT:
        red.y = prm.HEIGHT - prm.SPACESHIP_SIZE[1]


def handle_movement_velocity(
    keys_pressed: Sequence[bool],
    vector: pg.math.Vector2,
    k: Tuple[int, int, int, int] = (pg.K_a, pg.K_d, pg.K_w, pg.K_s),
) -> pg.math.Vector2:

    """Handles input of a player, accounts for acceleration and normalization.

    keys_pressed is what pygame.key.get_pressed() returns (bools).

    k is a tuple which contains 4 of pygame's keys in the following order: "LEFT", "RIGHT", "UP", "DOWN".

    Returns:
        pygame.math.Vector2: velocity.
    """

    (left, right, up, down) = k
    if keys_pressed[left]:  # LEFT
        vector.x -= prm.PLAYER_ACCELERATION
        if vector.x < -prm.PLAYER_MAX_VEL:
            vector.x = -prm.PLAYER_MAX_VEL
    elif keys_pressed[right]:  # RIGHT
        vector.x += prm.PLAYER_ACCELERATION
        if vector.x > prm.PLAYER_MAX_VEL:
            vector.x = prm.PLAYER_MAX_VEL
    else:
        if vector.x < 0:
            vector.x += prm.PLAYER_ACCELERATION
            if vector.x > 0:
                vector.x = 0
        else:
            vector.x -= prm.PLAYER_ACCELERATION
            if vector.x < 0:
                vector.x = 0

    if keys_pressed[up]:  # UP
        vector.y -= prm.PLAYER_ACCELERATION
        if vector.y < -prm.PLAYER_MAX_VEL:
            vector.y = -prm.PLAYER_MAX_VEL
    elif keys_pressed[down]:  # DOWN
        vector.y += prm.PLAYER_ACCELERATION
        if vector.y > prm.PLAYER_MAX_VEL:
            vector.y = prm.PLAYER_MAX_VEL
    else:
        if vector.y < 0:
            vector.y += prm.PLAYER_ACCELERATION
            if vector.y > 0:
                vector.y = 0
        else:
            vector.y -= prm.PLAYER_ACCELERATION
            if vector.y < 0:
                vector.y = 0

    velocity = vector

    if velocity.length() > prm.PLAYER_MAX_VEL:
        velocity = velocity.normalize() * prm.PLAYER_MAX_VEL

    return velocity


if __name__ == "__main__":
    main()
