if __name__ == 'game.cards':
    import pygame

    from game.vector import Vector

    class Card:
        # class constants
        FACE = pygame.image.load('../assets/card_sprites/card_face.png').convert_alpha()
        BACK = pygame.image.load('../assets/card_sprites/card_back.png').convert_alpha()
        BORDER = pygame.image.load('../assets/card_sprites/card_border.png').convert_alpha()
        BORDER_BOTTOM = pygame.image.load('../assets/card_sprites/card_border_bottom.png').convert_alpha()
        BORDER_TOP = pygame.image.load('../assets/card_sprites/card_border_top.png').convert_alpha()
        BORDER_MIDDLE = pygame.image.load('../assets/card_sprites/card_border_middle.png').convert_alpha()
        HOLLOW = pygame.image.load('../assets/card_sprites/card_hollow.png').convert_alpha()
        RECYCLE = pygame.image.load('../assets/card_sprites/card_recycle.png').convert_alpha()
        GHOST = pygame.image.load('../assets/card_sprites/card_ghost.png').convert_alpha()
        SUIT_SPRITES = {
            '1': pygame.image.load('../assets/suit_sprites/spades.png').convert_alpha(),
            '2': pygame.image.load('../assets/suit_sprites/hearts.png').convert_alpha(),
            '3': pygame.image.load('../assets/suit_sprites/clubs.png').convert_alpha(),
            '4': pygame.image.load('../assets/suit_sprites/diamonds.png').convert_alpha()
        }
        BIG_SUIT_SPRITES = {
            '1': pygame.image.load('../assets/big_suit_sprites/spades.png').convert_alpha(),
            '2': pygame.image.load('../assets/big_suit_sprites/hearts.png').convert_alpha(),
            '3': pygame.image.load('../assets/big_suit_sprites/clubs.png').convert_alpha(),
            '4': pygame.image.load('../assets/big_suit_sprites/diamonds.png').convert_alpha()
        }
        WIDTH = 60
        HEIGHT = 90
        PEEK_HEIGHT = 30
        RANK_POS = Vector(8, 5)
        SUIT_POS = Vector(36, 7)

        def __init__(self, rank: str, suit: str, position: Vector) -> None:
            self.rank = rank
            self.suit = suit
            self.color = 0 if self.suit in ['1', '3'] else 255
            self.position = position
            self.face_up = False
            self.sprite = Card.BACK

        # getting coords for rendering sprite
        def topleft(self) -> Vector:
            return self.position - Vector(Card.WIDTH, Card.HEIGHT) / 2
        
        # turning card up
        def reveal(self) -> None:
            self.face_up = True
            self.sprite = Card.FACE

        # turning card down
        def hide(self) -> None:
            self.face_up = False
            self.sprite = Card.BACK
    
    # same as topleft method but in a function
    def topleft(position: Vector) -> Vector:
        return position - Vector(Card.WIDTH, Card.HEIGHT) / 2
