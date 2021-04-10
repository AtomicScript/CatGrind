import pygame, os
from settings import *
vec = pygame.math.Vector2


class Thief(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # //==  ** Basics **  ==// #
        self.health = 100.0
        self.alive = True
        self.stole = False
        # //==  ** movement related **  ==// #
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(500, 760)
        self.images = []
        self.adding_images()
        self.frame = 0
        self.walk_frame = 0
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.state_idle = True
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()

    def adding_images(self):
        # for walk
        walkB1 = pygame.image.load(os.path.join("image/player/TBwalk1.png")).convert_alpha()
        walkB2 = pygame.image.load(os.path.join("image/player/TBwalk2.png")).convert_alpha()
        walkR1 = pygame.image.load(os.path.join("image/player/TRwalk1.png")).convert_alpha()
        walkR2 = pygame.image.load(os.path.join("image/player/TRwalk2.png")).convert_alpha()
        walkF1 = pygame.image.load(os.path.join("image/player/TFwalk1.png")).convert_alpha()
        walkF2 = pygame.image.load(os.path.join("image/player/TFwalk2.png")).convert_alpha()
        walkL1 = pygame.image.load(os.path.join("image/player/TLwalk1.png")).convert_alpha()
        walkL2 = pygame.image.load(os.path.join("image/player/TLwalk2.png")).convert_alpha()

        images = [walkB1, walkB2, walkR1, walkR2, walkF1, walkF2, walkL1, walkL2]
        for image in images:
            self.images.append(image)

    def up(self):
        self.acc.y = -THIEF_ACC
        self.move_left = False
        self.move_right = False
        self.move_up = True
        self.move_down = False
        self.state_idle = False
        self.walk_frame += 1

    def right(self):
        self.acc.x = THIEF_ACC
        self.move_left = False
        self.move_right = True
        self.move_up = False
        self.move_down = False
        self.state_idle = False
        self.walk_frame += 1

    def down(self):
        self.acc.y = THIEF_ACC
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = True
        self.state_idle = False
        self.walk_frame += 1

    def left(self):
        self.acc.x = -THIEF_ACC
        self.move_left = True
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.state_idle = False
        self.walk_frame += 1

    def path(self):
        self.life()
        if self.alive:
            if not self.stole:

                self.acc = vec(0, 0)

                if self.pos.y > 710:
                    self.up()

                elif self.pos.x >= 896:
                    self.acc = vec(0, 0)

                else:
                    self.right()

            else:
                self.acc = vec(0, 0)
                if self.pos.x <= 500:
                    self.down()
                    if self.pos.y >= 790:
                        self.acc = vec(0, 0)

                else:
                    self.left()

            # //==  ** frame related  **  ==// #
            if self.walk_frame >= 3:
                self.walk_frame = 0

            # //==  ** Nerd area **  ==// #
            # adds the friction
            self.acc += self.vel * THIEF_FRICTION
            # acc adds to vel
            self.vel += self.acc
            # motion equation
            self.pos += self.vel + 0.5 * self.acc
            # setting the new position as rect center
            self.rect.center = self.pos
        else:
            self.pos = vec(500, 760)

    def animating_player(self):
        self.image.set_colorkey(BLACK)

        # //==  ** ANIMATING WHILE MOVING  **  ==// #
        if self.move_down:
            if self.walk_frame == 1:
                self.frame = 4
            else:
                self.frame = 5

        if self.move_right:
            if self.walk_frame == 1:
                self.frame = 2
            else:
                self.frame = 3

        if self.move_left:
            if self.walk_frame == 1:
                self.frame = 6
            else:
                self.frame = 7

        if self.move_up:
            if self.walk_frame == 1:
                self.frame = 0
            else:
                self.frame = 1

        # //==  ** SET THE IMAGE AS THE CURRENT FRAME WE ARE IN **  ==// #
        self.image = self.images[self.frame]

    def go_again(self):
        self.alive = True
        self.stole = False

    def life(self):
        if self.health > 0:
            self.alive = True
        else:
            self.alive = False
