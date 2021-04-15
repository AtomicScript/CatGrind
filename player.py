# //==  ** Import  **  ==// #
import pygame, os
from settings import *
from elements import Bullet

# vec
vec = pygame.math.Vector2


# //==  ** Player class **  ==// #
class Player(pygame.sprite.Sprite):
    # attributes for the player
    def __init__(self, screen):
        super().__init__()
        # //==  ** Basics **  ==// #
        self.health = 500.0
        self.energy = 100.0
        self.max_health = 1000.0
        self.max_energy = 100.0
        self.score = 0.0
        self.bag = 0
        self.x, self.y = 100, 100
        self.alive = True
        self.screen = screen
        self.able_heal_potion = True
        self.able_energy_potion = False
        self.bullet_group = pygame.sprite.Group()
        self.last_shot = 0

        # //==  ** movement related **  ==// #
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(WIDTH/2, HEIGHT/2)

        # //==  ** Animating related  **  ==// #
        self.idle = []  # F:: N - E - S - W
        self.walk = []  # F:: N - E - S - W x 2
        self.adding_images()
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.state_idle = True
        self.state_face = "Front"
        self.frame = 0
        self.walk_frame = 0
        self.current_Frame = self.idle[self.frame]

        # //==  ** RECT RELATED  **  ==// #
        self.image = self.current_Frame
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    # control movement of the player
    def control(self):
        self.acc = vec(0, 0)    # acceleration should be 0 unless we pressed a key
        keys = pygame.key.get_pressed()
        # //==  ** Left movement **  ==// #
        if keys[pygame.K_LEFT or pygame.key == ord('a')]:
            self.acc.x = -PLAYER_ACC
            self.move_left = True
            self.move_right = False
            self.move_up = False
            self.move_down = False
            self.state_idle = False
            self.state_face = "Left"
            self.walk_frame += 1
            self.decrease_energy(0.05)

        # //==  ** Right movement **  ==// #
        if keys[pygame.K_RIGHT or pygame.key == ord('d')]:
            self.acc.x = PLAYER_ACC
            self.move_left = False
            self.move_right = True
            self.move_up = False
            self.move_down = False
            self.state_idle = False
            self.state_face = "Right"
            self.walk_frame += 1
            self.decrease_energy(0.05)

        # //==  ** Up movement **  ==// #
        if keys[pygame.K_UP or pygame.key == ord('w')]:
            self.acc.y = -PLAYER_ACC
            self.move_left = False
            self.move_right = False
            self.move_up = True
            self.move_down = False
            self.state_idle = False
            self.state_face = "Behind"
            self.walk_frame += 1
            self.decrease_energy(0.05)

        # //==  ** Down movement **  ==// #
        if keys[pygame.K_DOWN or pygame.key == ord('s')]:
            self.acc.y = PLAYER_ACC
            self.move_left = False
            self.move_right = False
            self.move_up = False
            self.move_down = True
            self.state_idle = False
            self.state_face = "Front"
            self.walk_frame += 1
            self.decrease_energy(0.05)

        if keys[pygame.K_SPACE]:
            self.shoot()

        # //==  ** frame related  **  ==// #
        if self.walk_frame >= 3:
            self.walk_frame = 0

        # //==  ** Nerd area **  ==// #
        # adds the friction
        self.acc += self.vel * PLAYER_FRICTION
        # acc adds to vel
        self.vel += self.acc
        # motion equation
        self.pos += self.vel + 0.5 * self.acc
        # setting the new position as rect center
        self.rect.center = self.pos

        # //==  ** Makes sure while moving they cant get out **  ==// #
        self.restriction_screen()

    # restricting player from moving off the screen
    def restriction_screen(self):
        if self.pos.x >= 945:
            self.pos.x = 945
        if self.pos.x <= 80:
            self.pos.x = 80
        if self.pos.y >= 710:
            self.pos.y = 710
        if self.pos.y <= 155:
            self.pos.y = 155

    # adding images to the lists
    def adding_images(self):
        # for idle
        idleB = pygame.image.load(os.path.join("image/player/behind-idle.png")).convert_alpha()
        idleR = pygame.image.load(os.path.join("image/player/right-idle.png")).convert_alpha()
        idleF = pygame.image.load(os.path.join("image/player/front-idle.png")).convert_alpha()
        idleL = pygame.image.load(os.path.join("image/player/left-idle.png")).convert_alpha()
        add = [idleB, idleR, idleF, idleL]
        for x in add:
            self.idle.append(x)

        walkB1 = pygame.image.load(os.path.join("image/player/behind-walk1.png")).convert_alpha()
        walkB2 = pygame.image.load(os.path.join("image/player/behind-walk2.png")).convert_alpha()
        walkR1 = pygame.image.load(os.path.join("image/player/right-walk1.png")).convert_alpha()
        walkR2 = pygame.image.load(os.path.join("image/player/right-walk2.png")).convert_alpha()
        walkF1 = pygame.image.load(os.path.join("image/player/front-walk1.png")).convert_alpha()
        walkF2 = pygame.image.load(os.path.join("image/player/front-walk2.png")).convert_alpha()
        walkL1 = pygame.image.load(os.path.join("image/player/left-walk1.png")).convert_alpha()
        walkL2 = pygame.image.load(os.path.join("image/player/left-walk2.png")).convert_alpha()

        add1 = [walkB1, walkB2, walkR1, walkR2, walkF1, walkF2, walkL1, walkL2]
        for x in add1:
            self.walk.append(x)

    # beginner level trying to understand frames better
    def animating_player(self):
        self.image.set_colorkey(BLACK)

        # //==  ** Facing what direction  **  ==// #
        if self.state_face == "Front":
            self.frame = 2
        elif self.state_face == "Behind":
            self.frame = 0
        elif self.state_face == "Right":
            self.frame = 1
        elif self.state_face == "Left":
            self.frame = 3

        # //==  ** SET THE CURRENT FRAME AS THE SELF.FRAME **  ==// #
        self.current_Frame = self.idle[self.frame]

        # //==  ** ANIMATING WHILE MOVING  **  ==// #
        if self.move_down:
            if self.walk_frame == 1:
                self.current_Frame = self.walk[4]
            else:
                self.current_Frame = self.walk[5]

        if self.move_right:
            if self.walk_frame == 1:
                self.current_Frame = self.walk[2]
            else:
                self.current_Frame = self.walk[3]

        if self.move_left:
            if self.walk_frame == 1:
                self.current_Frame = self.walk[6]
            else:
                self.current_Frame = self.walk[7]

        if self.move_up:
            if self.walk_frame == 1:
                self.current_Frame = self.walk[0]
            else:
                self.current_Frame = self.walk[1]

        # //==  ** SET THE IMAGE AS THE CURRENT FRAME WE ARE IN **  ==// #
        self.image = self.current_Frame

    # make sure that the health doesnt reach below zero
    def damage(self, damage):
        if self.health > 0:
            self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False

    # make sure that the health doesnt reach above max
    def heal(self, heal):
        if self.health < self.max_health:
            self.health += heal
        if self.health >= self.max_health:
            self.health = self.max_health

    # make sure that the energy doesnt reach above max while increasing it
    def increase_energy(self, energy):
        if self.energy < self.max_energy:
            self.energy += energy
        if self.energy >= self.max_energy:
            self.energy = self.max_energy

    # decrease the enemy
    def decrease_energy(self, energy):
        if self.energy > 0:
            self.energy -= energy
        if self.energy <= 0:
            self.energy = 0
            self.damage(0.25)

    # player state if they are able
    def player_state(self):
        if self.health < self.max_health:
            self.able_heal_potion = True
        if self.health >= self.max_health:
            self.able_heal_potion = False
        if self.energy < self.max_energy:
            self.able_energy_potion = True
        if self.energy >= self.max_energy:
            self.able_energy_potion = False

    # shoot 
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > BULLET_RATE:
            self.last_shot = now
            bullet = Bullet(self.state_face, self.rect.x, self.rect.y)
            self.bullet_group.add(bullet)




