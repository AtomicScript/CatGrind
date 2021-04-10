import pygame


class Side(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("image/block.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0


class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("image/wall_wall.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0


class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("image/floorfull.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0


class HalfFloor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("image/halffloor.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0


class Dungeon:
    def __init__(self, group):
        self.group = group

    def add_map(self):
        # Adds walls onto the WIDTH
        count = 32
        for wall in range(30):
            wall1 = Side()
            wall1.rect.x = count
            count += 32
            wall1.rect.y = 96
            self.group.add(wall1)

        count = 128
        for floor in range(7):
            floor = HalfFloor()
            floor.rect.x = 928
            floor.rect.y = count
            count += 128
            self.group.add(floor)

        count = 32
        for wallWall in range(30):
            wallWall = Wall()
            wallWall.rect.x = count
            count += 32
            wallWall.rect.y = 128
            self.group.add(wallWall)

        count = 32
        for floor in range(7):
            floor = Floor()
            floor.rect.x = count
            floor.rect.y = 160
            count += 128
            self.group.add(floor)

        count = 32
        for floor in range(7):
            floor = Floor()
            floor.rect.x = count
            floor.rect.y = 288
            count += 128
            self.group.add(floor)

        count = 32
        for floor in range(7):
            floor = Floor()
            floor.rect.x = count
            floor.rect.y = 416
            count += 128
            self.group.add(floor)

        count = 32
        for floor in range(7):
            floor = Floor()
            floor.rect.x = count
            floor.rect.y = 544
            count += 128
            self.group.add(floor)

        count = 32
        for floor in range(7):
            floor = Floor()
            floor.rect.x = count
            floor.rect.y = 672
            count += 128
            self.group.add(floor)

        # Adds walls onto the HEIGHT
        count = 128
        for side in range(19):
            side = Side()
            side2 = Side()
            side2.rect.y = count
            side2.rect.x = 960
            side.rect.x = 32
            side.rect.y = count
            count += 32
            self.group.add(side)
            self.group.add(side2)

        count = 32
        for wall in range(12):
            wall1 = Side()
            wall1.rect.x = count
            wall1.rect.y = 735
            count += 32
            self.group.add(wall1)

        ang = 608
        for wall in range(12):
            wall1 = Side()
            wall1.rect.x = ang
            wall1.rect.y = 736
            ang += 32
            self.group.add(wall1)




