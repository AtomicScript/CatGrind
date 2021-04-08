import pygame, os

# //==  ** Attributes **  ==// #
WIDTH = 1024
HEIGHT = 768
SCREEN_SIZE = (WIDTH, HEIGHT)
SCREEN_CENTER = (WIDTH // 2, HEIGHT // 2)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
FPS = 40
# for the player
PLAYER_ACC = 3
PLAYER_FRICTION = -0.50
# for the Thief
THIEF_ACC = 0.5
THIEF_FRICTION = -0.30
# for bullet
BULLET_RATE = 150

# sounds
pygame.mixer.init()
error = pygame.mixer.Sound(os.path.join("sound/error.mp3"))
bought = pygame.mixer.Sound(os.path.join("sound/done.mp3"))
got_coin = pygame.mixer.Sound(os.path.join("sound/cash.mp3"))


list_sound = [error, bought, got_coin]
for sound in list_sound:
    sound.set_volume(0.2)


# to save lines of codes !!
def draw_text(text, size, color, x, y, screen):
    # none should be capital // i forgot
    font = pygame.font.Font(None, size)
    # we create the text object here
    text_object = font.render(text, True, color)
    # we create the rect of that object
    text_rect = text_object.get_rect()
    text_rect.x, text_rect.y = x, y
    # placing the rect onto the screen
    screen.blit(text_object, text_rect)


# check if it collides
def check_Collisions(a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
    return (a_x + a_width > b_x) and (a_x < b_x + b_width) and (a_y + a_height > b_y) and (a_y < b_y + b_height)


# creating buttons easily
class Buttons:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width = width
        self.height = height
        # create a rect object
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # drawing it onto the screen
    def button_draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)


# creating a player's health bar
class Health_bar:
    def __init__(self, player):
        self.length = 200
        self.player = player
        self.ratio = self.player.max_health / self.length
        self.rect = pygame.Rect(80, 20, self.player.health / self.ratio, 15)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
        pygame.draw.rect(screen, WHITE, (80, 20, self.length, 15), 2)

    def update(self):
        self.rect = pygame.Rect(80, 20, self.player.health / self.ratio, 15)


# creating a player's energy bars
class Energy_bar:
    def __init__(self, player):
        self.length = 200
        self.player = player
        self.ratio = self.player.max_energy / self.length
        self.rect = pygame.Rect(80, 40, self.player.energy / self.ratio, 15)

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)
        pygame.draw.rect(screen, WHITE, (80, 40, self.length, 15), 2)

    def update(self):
        self.rect = pygame.Rect(80, 40, self.player.energy / self.ratio, 15)


class Game_Buttons(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.player = player
        self.rect = pygame.Rect(x, y, 64, 64)

    # drawing it onto the screen
    def button_draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

    def click(self):
        print("clicked")


class energy_button(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.boost = 100
        self.cost = 10
        self.player = player
        self.image = pygame.image.load(os.path.join("image/energy_button.png"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        # drawing it onto the screen
    def button_draw(self, screen):
        screen.blit(self.image, self.rect)

    def click(self):
        if self.player.bag >= self.cost:
            self.player.player_state()
            if self.player.able_energy_potion:
                self.player.increase_energy(self.boost)
                self.player.bag -= self.cost
                bought.play()
            else:
                error.play()
        else:
            error.play()


class health_button(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.boost = 100
        self.cost = 10
        self.player = player
        self.image = pygame.image.load(os.path.join("image/health_button.png"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    # drawing it onto the screen
    def button_draw(self, screen):
        screen.blit(self.image, self.rect)

    def click(self):
        if self.player.bag >= self.cost:
            self.player.player_state()
            if self.player.able_heal_potion:
                self.player.heal(self.boost)
                self.player.bag -= self.cost
                bought.play()
            else:
                error.play()
        else:
            error.play()


class upgrade_button(pygame.sprite.Sprite):
    def __init__(self, x, y, player, coin, chest):
        super().__init__()
        self.boost = 100
        self.coin = coin
        self.chest = chest
        self.cost = 10
        self.control = 0
        self.level = "Level 0"
        self.player = player
        self.image = pygame.image.load(os.path.join("image/upgrade_level.png"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    # drawing it onto the screen
    def button_draw(self, screen):
        screen.blit(self.image,self.rect)

    def click(self):
        if self.player.bag >= self.cost:
            self.control += 1
            self.level = f"Level {self.control}"
            self.coin.standard += self.control
            self.chest.standard += self.control
            self.player.bag -= self.cost
            self.cost += round((self.cost - (self.cost * 0.20)))
            bought.play()
        else:
            error.play()


