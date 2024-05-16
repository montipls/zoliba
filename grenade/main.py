import pygame

import vector, engine

WIDTH, HEIGHT = 256, 144
FLOOR = 20

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
clock = pygame.time.Clock()
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED | pygame.SRCALPHA)
pygame.display.set_caption("yes")

pygame.mixer.init()
footstep = pygame.mixer.Sound("assets/sfx/footstep.ogg")
explosion = pygame.mixer.Sound("assets/sfx/explosion.ogg")
sounds = [footstep, explosion]

bg = pygame.image.load("assets/bg.png")
floor = pygame.image.load("assets/floor.png")
fighters = [engine.Fighter(vector.Vector(100 + joy.get_id() * 5, 50), (0, WIDTH, HEIGHT - FLOOR), joy.get_id(), sounds) for joy in joysticks]

fix_points = [
    engine.Ball((20, 125), 15, 0.99),
    engine.Ball((60, 100), 20, 0.99),
    engine.Ball((93, 85), 15, 0.99),
    engine.Ball((130, 65), 20, 0.99),
    engine.Ball((178, 40), 18, 0.99),
    engine.Ball((195, 40), 20, 0.99)
]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    win.blit(bg, (0, 0))
    for pt in fix_points:
        pt.render(win)
    win.blit(floor, (0, HEIGHT - FLOOR - 2))
    

    for i, fighter in enumerate(fighters):
        try:
            fighter.check_for_explosion(fighters[abs(i-1)])
        except IndexError:
            fighter.check_for_explosion(None)
        fighter.check_for_bomb_reload()

        if pygame.mouse.get_pressed()[1]:
            x, y = pygame.mouse.get_pos()
            if y > HEIGHT - FLOOR - 1:
                y = HEIGHT - FLOOR - 1
            pygame.draw.line(win, (230, 90, 20), (engine.Fighter.reflection(fighter.head.position_current.tup(), HEIGHT - FLOOR)), engine.Fighter.reflection((x, y + 1), HEIGHT - FLOOR), 1)
            pygame.draw.line(win, (130, 100, 100), (fighter.head.position_current.tup()), (x, y), 1)

        fighter.move(joysticks)
        fighter.update(HEIGHT - FLOOR, fix_points)
        fighter.render(win, HEIGHT - FLOOR)

    clock.tick(120)
    pygame.display.update()
