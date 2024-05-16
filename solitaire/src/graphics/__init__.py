if __name__ == 'graphics':
    import pygame
    pygame.init()

    # declaring constants
    WINDOW_SIZE = (800, 800)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Solitaire')
    CARD_COLUMNS_OFFSET = 200
    CARD_STACKS_OFFSET = 80
    FONT = pygame.font.Font('../assets/font/hack.ttf', 18)
