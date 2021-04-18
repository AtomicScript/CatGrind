# //==  ** imports  **  ==// #
import pygame, os, random
from settings import *

# vec
vec = pygame.math.Vector2


# //==  ** Bullet class **  ==// #
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_face, player_x, player_y):
        super().__init__()
        self.image = pygame.image.load(os.path.join("image/bullet.png"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = player_x, player_y
        self.face = player_face
        self.dx = 0
        self.dy = 0
        self.vel = 10
        self.life = 1000
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.dx = 0
        self.dy = 0

        # left movement
        if self.face == "Left":
            self.dx = -self.vel
        # Right movement
        if self.face == "Right":
            self.dx = self.vel

        # up movement
        if self.face == "Behind":
            self.dy = -self.vel

        # down movement
        if self.face == "Front":
            self.dy = self.vel

        self.rect.x += self.dx
        self.rect.y += self.dy

        if pygame.time.get_ticks() - self.spawn_time > self.life:
            self.kill()

        self.restrict()

    def restrict(self):
        if self.rect.y < 155:
            self.kill()
        if self.rect.x < 80:
            self.kill()
        if self.rect.x > 945:
            self.kill()
        if self.rect.y > 710:
            self.kill()


# //==  ** Ruby class  **  ==// #
class Ruby(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.standard = 1
        self.image = pygame.image.load(os.path.join("image/ruby.png"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.randint(128, 900), random.randint(200, 700)

    def spawn(self):
        self.rect.x, self.rect.y = random.randint(128, 900), random.randint(200, 700)
        self.update()

    def player_coin(self, player):
        if (check_Collisions(player.rect.x, player.rect.y, player.image.get_width(),
                             player.image.get_height(), self.rect.x, self.rect.y,
                             self.image.get_width(), self.image.get_height())):
            player.bag += self.standard
            self.spawn()


# //==  ** Chest class **  ==// #
class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.standard = 1
        self.frame = 0
        self.images = []
        self.chest_images()
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    # player and chest interaction
    def player_interaction(self, player):
        if (check_Collisions(player.rect.x, player.rect.y, player.image.get_width(),
                             player.image.get_height(), self.rect.x, self.rect.y,
                             self.image.get_width(), self.image.get_height())):

            key = pygame.key.get_pressed()

            # side
            if player.pos.x <= 890 and player.pos.y > 666:
                player.pos.x = 884

            # top
            if player.pos.x >= 897 and player.pos.y >= 656:
                player.pos.y = 654

            self.open()

            if key[pygame.K_e or pygame.key == ord('e')]:
                for coin in range(player.bag):
                    player.score += (5 * self.standard)

                player.bag = 0

        else:
            self.close()
            self.update()

    # enemy and chest interaction
    def enemy_interaction(self, enemy, actual_player):
        if (check_Collisions(enemy.rect.x, enemy.rect.y, enemy.image.get_width(),
                             enemy.image.get_height(), self.rect.x, self.rect.y,
                             self.image.get_width(), self.image.get_height())):

            if enemy.pos.x <= 890 and enemy.pos.y > 666:
                enemy.pos.x = 870

            if enemy.pos.x > 897 and enemy.pos.y >= 656:
                enemy.pos.y = 654

            self.open()
            enemy.acc = vec(0, 0)

            if enemy.alive:
                if actual_player.score > 0:
                    actual_player.score = (actual_player.score - (actual_player.score * 0.30))
                enemy.stole = True

            else:
                enemy.stole = False

        else:
            self.close()

    def chest_images(self):
        closed = pygame.image.load("image/close_chest.png").convert_alpha()
        opened = pygame.image.load("image/opened_chest.png").convert_alpha()
        images = [closed, opened]
        for image in images:
            self.images.append(image)

    def close(self):
        self.frame = 0
        self.image = self.images[self.frame]
        self.update()

    def open(self):
        self.frame = 1
        self.image = self.images[self.frame]
        self.update()


# //==  ** Potion PARENT class **  ==// #
class Potions(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.boost = 0
        self.player = ""
        self.group = ""
        self.rect = pygame.Rect(80, 40, 10, 10)
        self.rect.x, self.rect.y = random.randint(128, 900), random.randint(100, 730)

    def spawn(self):
        self.rect.x, self.rect.y = random.randint(128, 900), random.randint(100, 730)
        self.update()

    def collide(self):
        if (check_Collisions(self.player.rect.x, self.player.rect.y, self.player.image.get_width(),
                             self.player.image.get_height(), self.rect.x, self.rect.y,
                             self.image.get_width(), self.image.get_height())):
            self.effect()

    def effect(self):
        pass


# //==  ** Small Potion child class **  ==// #
class Small_energy_potion(Potions):
    def __init__(self, player, group):
        super().__init__()
        self.boost = 50
        self.cost = 50
        self.player = player
        self.group = group
        self.image = pygame.image.load(os.path.join("image/energy.png"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.randint(128, 900), random.randint(200, 710)

    def effect(self):
        self.player.increase_energy(self.boost)


# //==  ** Small Potion child class **  ==// #
class Small_heal_potion(Potions):
    def __init__(self, player, group):
        super().__init__()
        self.boost = 50
        self.cost = 50
        self.player = player
        self.group = group
        self.image = pygame.image.load(os.path.join("image/heart.png"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.randint(300, 900), random.randint(300, 710)

    def effect(self):
        self.player.heal(self.boost)
