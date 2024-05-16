if __name__ == 'game.events':
    import pygame

    # declaring global variables
    quit_event = False
    key_events = {}
    mouse_events = []
    mouse_position = pygame.mouse.get_pos()
    lmbd = lmbu = rmbd = rmbu = False

    def update_events() -> None:
        # setting global variables to default
        global quit_event, key_events, mouse_events, mouse_position
        global lmbd, lmbu, rmbd, rmbu
        key_events = pygame.key.get_pressed()
        mouse_events = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()
        lmbd = lmbu = rmbd = rmbu = False

        # looping through pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_event = True
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_event = True
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    lmbd = True
                if event.button == 3:
                    rmbd = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    lmbu = True
                if event.button == 3:
                    rmbu = True