import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("image/wall.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0


class SideWallOne(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("image/sideleft.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0


class SideWallTwo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("image/sideright.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0




