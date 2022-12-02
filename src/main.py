import pygame as pg
import os

WIDTH, HEIGHT = 720, 480
WIN = pg.display.set_mode((WIDTH, HEIGHT))

FPS = 60
SPEED = 5

SPACESHIP_SIZE = (45, 45)

YELLOW_SPACESHIP_IMAGE = pg.image.load(
    os.path.join("src", "assets", "img", "spaceship_yellow.png")
).convert_alpha()

YELLOW_SPACESHIP = pg.transform.rotate(
    pg.transform.scale(YELLOW_SPACESHIP_IMAGE, SPACESHIP_SIZE), 90
)

RED_SPACESHIP_IMAGE = pg.image.load(
    os.path.join("src", "assets", "img", "spaceship_red.png")
).convert_alpha()

RED_SPACESHIP = pg.transform.rotate(
    pg.transform.scale(RED_SPACESHIP_IMAGE, SPACESHIP_SIZE), -90
)

COLOR = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "GRAY": (127, 127, 127),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
}

CLR = {
    "BACKGROUND": COLOR["WHITE"],
}

BORDER_THICKNESS = 5
BORDER = pg.Rect(WIDTH / 2 - BORDER_THICKNESS / 2, 0, BORDER_THICKNESS, HEIGHT)

pg.display.set_caption("Pygame space shooter")
pg.init()


def draw_window(yellow, red):
    WIN.fill(CLR["BACKGROUND"])
    pg.draw.rect(WIN, COLOR["GRAY"], BORDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    pg.display.update()


def main():
    yellow = pg.Rect(
        WIDTH / 4 - SPACESHIP_SIZE[0] / 2,
        HEIGHT / 2 - SPACESHIP_SIZE[1] / 2,
        *SPACESHIP_SIZE
    )
    red = pg.Rect(
        WIDTH / 4 * 3 - SPACESHIP_SIZE[0] / 2,
        HEIGHT / 2 - SPACESHIP_SIZE[1] / 2,
        *SPACESHIP_SIZE
    )

    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                run = False

        handleMovement(yellow, red, pg.key.get_pressed())

        draw_window(yellow, red)
    pg.quit()


def handleMovement(yellow, red, keys_pressed):
    vel = {
        "yellow": {
            "x": 0,
            "y": 0,
        },
        "red": {
            "x": 0,
            "y": 0,
        },
    }

    if keys_pressed[pg.K_a]:  # LEFT
        yellow.x -= SPEED
    if keys_pressed[pg.K_d]:  # RIGHT
        yellow.x += SPEED
    if keys_pressed[pg.K_w]:  # UP
        yellow.y -= SPEED
    if keys_pressed[pg.K_s]:  # DOWN
        yellow.y += SPEED

    if keys_pressed[pg.K_RIGHT]:
        red.x += SPEED
    if keys_pressed[pg.K_LEFT]:
        red.x -= SPEED
    if keys_pressed[pg.K_UP]:
        red.y -= SPEED
    if keys_pressed[pg.K_DOWN]:
        red.y += SPEED

    if yellow.x < 0:
        yellow.x = 0
    if yellow.y < 0:
        yellow.y = 0
    if yellow.x + SPACESHIP_SIZE[0] > WIDTH / 2:
        yellow.x = WIDTH / 2 - SPACESHIP_SIZE[0]
    if yellow.y + SPACESHIP_SIZE[1] > HEIGHT:
        yellow.y = HEIGHT - SPACESHIP_SIZE[1]

    if red.x < WIDTH / 2:
        red.x = WIDTH / 2
    if red.y < 0:
        red.y = 0
    if red.x + SPACESHIP_SIZE[0] > WIDTH:
        red.x = WIDTH - SPACESHIP_SIZE[0]
    if red.y + SPACESHIP_SIZE[1] > HEIGHT:
        red.y = HEIGHT - SPACESHIP_SIZE[1]


if __name__ == "__main__":
    main()
