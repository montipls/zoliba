if __name__ == 'game.interaction':
    import game
    from game import scene, events, cards
    from game.vector import Vector
    from game.cards import Card
    from graphics import CARD_COLUMNS_OFFSET, WINDOW_SIZE, CARD_STACKS_OFFSET

    # defaults
    hovering_cards = {}
    hovering_index = None
    selected_column = None
    selected_stack = None
    deck_hover = False
    # globally accessible mode
    mode = 'pick'

    # returns list of cards revealed in a column
    def revealed_cards(column: list) -> int:
        return list(filter(lambda card: card.face_up, column))
 
    def pull_from_deck() -> None:
        scene.deck[-1].position = Vector(WINDOW_SIZE[0] / (scene.COLUMN_COUNT + 1) * 2, CARD_STACKS_OFFSET)
        scene.deck[-1].reveal()
        game.pull.append(scene.deck[-1])
        scene.deck.pop()

    def recycle_deck() -> None:
        for card in reversed(game.pull):
            card.position = Vector(WINDOW_SIZE[0] / (scene.COLUMN_COUNT + 1), CARD_STACKS_OFFSET)
            card.hide()
            scene.deck.append(card)
            game.pull.remove(card)

    def deck_interaction() -> None:
        global deck_hover
        h_margin = Card.WIDTH / 2
        v_margin = Card.HEIGHT / 2
        x = WINDOW_SIZE[0] / (scene.COLUMN_COUNT + 1)
        y = CARD_STACKS_OFFSET
        deck_hover = False
        if x - h_margin <= events.mouse_position[0] <= x + h_margin:
            if y - v_margin <= events.mouse_position[1] <= y + v_margin:
                if mode == 'pick':
                    deck_hover = True
                    if events.lmbd:
                        if len(scene.deck) != 0:
                            pull_from_deck()
                            return
                        recycle_deck()

    # returns column index
    def detect_column_select() -> int | None:
        h_margin = Card.WIDTH / 2
        v_margin = Card.HEIGHT / 2
        for column_index, column in enumerate(scene.columns):
            # setting default position for empty columns
            if len(column) == 0:
                column_end = CARD_COLUMNS_OFFSET + Card.PEEK_HEIGHT + v_margin
            else:
                column_end = column[-1].position[1] + Card.PEEK_HEIGHT + v_margin
            # checking if mouse is on top of a column
            column_x = scene.find_column_x(column_index + 1)
            if column_x - h_margin <= events.mouse_position[0] <= column_x + h_margin:
                if CARD_COLUMNS_OFFSET - v_margin <= events.mouse_position[1] <= column_end:
                    return column_index
        return None
    
    # returns stack index
    def detect_stack_select() -> int | None:
        h_margin = Card.WIDTH / 2
        v_margin = Card.HEIGHT / 2
        for stack_index in range(4):
            x = WINDOW_SIZE[0] / (scene.COLUMN_COUNT + 1) * (scene.COLUMN_COUNT - stack_index)
            y = CARD_STACKS_OFFSET
            if x - h_margin <= events.mouse_position[0] <= x + h_margin:
                if y - v_margin <= events.mouse_position[1] <= y + v_margin:
                    return stack_index
        return None

    def detect_card_hover() -> tuple[dict, int | None]:
        # setting event to default
        hovering = {}
        h_margin = Card.WIDTH / 2
        v_margin = Card.HEIGHT / 2
        for column_index, column in enumerate(scene.columns):
            # skipping if column is empty
            if len(column) == 0:
                continue
            # checking if mouse is on top of a card
            column_x = scene.find_column_x(column_index + 1)
            if column_x - h_margin <= events.mouse_position[0] <= column_x + h_margin:
                start_index = len(column) - len(revealed_cards(column))
                if column[start_index].position[1] - v_margin <= events.mouse_position[1] <= column[-1].position[1] + v_margin:
                    # hovering more cards for multiple selection
                    column_start = events.mouse_position[1] - CARD_COLUMNS_OFFSET + Card.HEIGHT / 2
                    top_card_index = min(len(column) - 1, column_start // Card.PEEK_HEIGHT)
                    card_list = [column[index] for index in range(int(top_card_index), len(column))]
                    hovering = zip(card_list, ['column' for _ in range(len(card_list))])
                    return (dict(hovering), column_index)
                
        # doing same thing for stacks
        for stack_index, stack in enumerate(game.stacks):
            # skipping if stack is empty
            if len(stack) == 0:
                continue
            # checking if mouse is on top of a card
            h_margin = Card.WIDTH / 2
            v_margin = Card.HEIGHT / 2
            x = WINDOW_SIZE[0] / (scene.COLUMN_COUNT + 1) * (scene.COLUMN_COUNT - stack_index)
            y = CARD_STACKS_OFFSET
            if x - h_margin <= events.mouse_position[0] <= x + h_margin:
                if y - v_margin <= events.mouse_position[1] <= y + v_margin:
                    hovering = {stack[-1]: 'stack'}
                    return (hovering, stack_index)
        
        # same thing for top pulled card
        if len(game.pull) != 0:
            h_margin = Card.WIDTH / 2
            v_margin = Card.HEIGHT / 2
            x = WINDOW_SIZE[0] / (scene.COLUMN_COUNT + 1) * 2
            y = CARD_STACKS_OFFSET
            if x - h_margin <= events.mouse_position[0] <= x + h_margin:
                if y - v_margin <= events.mouse_position[1] <= y + v_margin:
                    hovering = {game.pull[-1]: 'pull'}
                    return (hovering, 0)
        return (hovering, None)
    
    # solve card placing
    def place_column_cards(hovering_cards: list, column_index: int) -> None:
        for card in list(hovering_cards.keys()):
            x = scene.find_column_x(column_index + 1)
            y = CARD_COLUMNS_OFFSET + (len(scene.columns[column_index]) * cards.Card.PEEK_HEIGHT)
            card.position = Vector(x, y)
            scene.columns[column_index].append(card)
            if hovering_cards[card] == 'column':
                scene.columns[hovering_index].remove(card)
            elif hovering_cards[card] == 'stack':
                game.stacks[hovering_index].remove(card)
            elif hovering_cards[card] == 'pull':
                game.pull.pop()

    def place_stack_cards(hovering_cards: list, stack_index: int) -> None:
        for card in list(hovering_cards.keys()):
            x = WINDOW_SIZE[0] / (scene.COLUMN_COUNT + 1) * (scene.COLUMN_COUNT - stack_index)
            y = CARD_STACKS_OFFSET
            card.position = Vector(x, y)
            game.stacks[stack_index].append(card)
            if hovering_cards[card] == 'column':
                scene.columns[hovering_index].remove(card)
            elif hovering_cards[card] == 'stack':
                game.stacks[hovering_index].remove(card)
            elif hovering_cards[card] == 'pull':
                game.pull.pop()

    # should be checking before each move
    def validate_column_move(cards: list, column_index: int) -> bool:
        if len(scene.columns[column_index]) == 0:
            if list(cards.keys())[0].rank != 'K':
                return False
            bottom_card = list(cards.keys())[0]
        else:
            bottom_card = scene.columns[column_index][-1]
        for card in list(cards.keys()):
            if card == bottom_card:
                continue
            if card.color == bottom_card.color:
                return False
            # calculating value of bottom card
            if bottom_card.rank in game.rank_map.keys():
                bottom_value = game.rank_map[bottom_card.rank] 
            else:
                bottom_value = int(bottom_card.rank)
            # calculating value of next card
            if card.rank in game.rank_map.keys():
                value = game.rank_map[card.rank] 
            else:
                value = int(card.rank)
            if bottom_value - value != 1:
                return False
            bottom_card = card
            continue
        return True
    
    def validate_stack_move(cards: list, stack_index: int) -> bool:
        if len(list(cards.keys())) > 1:
            return False
        if len(game.stacks[stack_index]) == 0:
            if list(cards.keys())[0].rank != 'A':
                return False
            return True
        else:
            bottom_card = game.stacks[stack_index][-1]
            if bottom_card.suit != list(cards.keys())[0].suit:
                return False
            # calculating value of bottom card
            if bottom_card.rank in game.rank_map.keys():
                bottom_value = game.rank_map[bottom_card.rank] 
            else:
                bottom_value = int(bottom_card.rank)
            # calculating value of next card
            if list(cards.keys())[0].rank in game.rank_map.keys():
                value = game.rank_map[list(cards.keys())[0].rank] 
            else:
                value = int(list(cards.keys())[0].rank)
            if value - bottom_value != 1:
                return False
            return True

    # always reveal card on top
    def flip_top() -> None:
        for column in scene.columns:
            if len(column) != 0:
                if not column[-1].face_up:
                    column[-1].reveal()

    # update all card events
    def refresh_card_events() -> None:
        global hovering_cards, selected_column, hovering_index, mode, selected_stack
        if mode == 'pick':
            hovering_cards, hovering_index = detect_card_hover()
        elif mode == 'place':
            selected_column = detect_column_select()
            selected_stack = detect_stack_select()

    # manage mouse input from user
    def manage_mode_changes() -> None:
        global mode
        if events.lmbd:
            if mode == 'pick':
                if hovering_index != None:
                    mode = 'place'
            elif mode == 'place':
                if selected_column != None:
                    if not (selected_column == hovering_index and list(hovering_cards.values())[0] == 'column'):
                        if validate_column_move(hovering_cards, selected_column):
                            place_column_cards(hovering_cards, selected_column)
                            mode = 'pick'
                        else:
                            mode = 'pick'
                elif selected_stack != None:
                    if validate_stack_move(hovering_cards, selected_stack):
                        place_stack_cards(hovering_cards, selected_stack)
                        mode = 'pick'
                    else:
                        mode = 'pick'
                else:
                    mode = 'pick'
