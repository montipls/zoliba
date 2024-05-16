if __name__ == 'game.scene':
    import game
    from game import cards
    from game.vector import Vector
    import graphics
    from graphics import WINDOW_SIZE, CARD_COLUMNS_OFFSET

    COLUMN_COUNT = 7

    # finding x of whole column
    def find_column_x(column_index: int) -> float:
        return WINDOW_SIZE[0] / (COLUMN_COUNT + 1) * column_index

    # randomizing card columns
    def generate_columns(column_count: int) -> list:
        column_array = []

        for column_index in range(1, column_count + 1):
            column = []
            # getting x coordinate based on column index
            x = find_column_x(column_index)
            for index in range(column_index):
                # choosing random card from deck
                card_type = game.deck[-1]
                position = Vector(
                    x, CARD_COLUMNS_OFFSET + (index * cards.Card.PEEK_HEIGHT)
                )
                card = cards.Card(card_type[0:-1], card_type[-1], position)
                # removing card from deck
                game.deck.pop()
                # revealing top card
                if index + 1 == column_index:
                    card.reveal()
                # adding card to column
                column.append(card)
            column_array.append(column)
        return column_array

    def generate_deck() -> list:
        deck = []
        for card_type in game.deck:
            position = Vector(
                WINDOW_SIZE[0] / (COLUMN_COUNT + 1),
                graphics.CARD_STACKS_OFFSET
            )
            card = cards.Card(card_type[0:-1], card_type[-1], position)
            deck.append(card)
        return deck

    # generating all 7 columns and deck
    columns = generate_columns(COLUMN_COUNT)
    deck = generate_deck()

