import pygame
import sys

from graphics import renderer
from game import events
from game import interaction

# game loop
while True:
    interaction.flip_top()
    interaction.refresh_card_events()
    interaction.deck_interaction()
    interaction.manage_mode_changes()
    events.update_events()
    renderer.redraw_window()
    # checking for quit event
    if events.quit_event:
        pygame.quit()
        sys.exit()
