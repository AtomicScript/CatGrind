# //==  ** Importing  **  ==// #
import sys
from player import *
from world import *
from elements import *
from enemy import *
from score import Score


class Evade:
    def __init__(self):
        # //==  ** Start pygame**  ==// #
        pygame.init()
        # //==  ** clock and loops **  ==// #
        self.clock = pygame.time.Clock()
        # //==  ** to keep the loop running **  ==// #
        self.start = True
        # //==  ** count time to keep track **  ==// #
        self.count_time = 0
        # //==  ** chance in game **  ==// #
        self.chance = 100
        # //==  ** Screen **  ==// #
        self.screen = pygame.display.set_mode(SCREEN_SIZE)                  # size
        pygame.display.set_caption("CatGrind - Atom")                       # caption
        self.background_screen = pygame.display.set_mode((WIDTH, HEIGHT))   # background screen size
        self.background_image = pygame.image.load("image/background.png")   # background screen image

        # //==  ** Button classes **  ==// #
        # for the menu // refer back to settings to see the Buttons class
        self.start_button = Buttons(270, 350, 510, 60)
        self.help_button = Buttons(50, 70, 80, 50)
        self.info_button = Buttons(270, 450, 510, 60)
        self.exit_button = Buttons(270, 550, 510, 60)
        self.menu_button = Buttons(900, 100, 20, 20)
        # for the game over // refer back to settings to see the Buttons class
        self.replay_button = Buttons(270, 480, 510, 60)
        self.back_button = Buttons(270, 580, 510, 60)
        self.exit_button2 = Buttons(270, 680, 510, 60)

        # //==  ** MOUSE GET POSITION **  ==// #
        self.mx, self.my = pygame.mouse.get_pos()

        # //==  ** CLASSES **  ==// #
        self.player = Player(self.screen)
        self.thief = Thief()
        self.health_bar = Health_bar(self.player)
        self.energy_bar = Energy_bar(self.player)
        self.Ruby = Ruby()
        self.chest = Chest(896, 672)
        self.score = Score()

        # for the menu // refer back to settings to see the Buttons class
        self.button1 = energy_button(620, 10, self.player)
        self.button2 = health_button(720, 10, self.player)
        self.button3 = upgrade_button(820, 10, self.player, self.Ruby, self.chest)

        # //==  ** Sprite Groups **  ==// #
        self.all_sprites = pygame.sprite.Group()
        self.map_sprite = pygame.sprite.Group()
        self.wall_sprite_down = pygame.sprite.Group()
        self.side_sprite = pygame.sprite.Group()
        self.coin_sprite = pygame.sprite.Group()
        self.enemy_sprite = pygame.sprite.Group()
        self.potions_sprite = pygame.sprite.Group()
        self.bullet = self.player.bullet_group

        # map 1
        self.dungeon_map = Dungeon(self.map_sprite)

        # //==  ** BOOSTS classes **  ==// #
        self.mini_heal_potion = Small_heal_potion(self.player, self.potions_sprite)
        self.mini_energy_potion = Small_energy_potion(self.player, self.potions_sprite)

    # //==  ** Menu Loop **  ==// #
    def menu(self):
        while self.start:
            self.menu_event()
            self.menu_draw()
            pygame.display.update()
            self.clock.tick(FPS)

    # //==  ** menu events type here **  ==// #
    def menu_event(self):
        # We need to get the position in the game loop not just init
        self.mx, self.my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    self.start = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if mouse got pressed
                if pygame.mouse.get_pressed()[0]:
                    # and the position of the mouse is the start button rect
                    if self.start_button.rect.collidepoint(self.mx, self.my):
                        # then start the game
                        self.start_new_game()
                        self.in_game()
                    if self.info_button.rect.collidepoint(self.mx, self.my):
                        # then go to option screen
                        self.stat()
                    if self.help_button.rect.collidepoint(self.mx, self.my):
                        # then go to option screen
                        self.help_screen()
                    if self.exit_button.rect.collidepoint(self.mx, self.my):
                        # then go to exit the game
                        pygame.quit()
                        try:
                            sys.exit()
                        finally:
                            self.start = False

    # //==  ** menu draw type here **  ==// #
    def menu_draw(self):
        self.screen.fill(BLACK)
        self.background_screen.blit(self.background_image, [0, 0])
        # texts
        draw_text("CatGrind Main Menu", 100, WHITE, 220, 100, self.screen)
        draw_text("Created by: Andromeda#2302 // SaloonaSenpai", 20, WHITE, 370, 730, self.screen)
        # buttons
        self.help_button.button_draw(self.screen, LighBlue)
        draw_text("H E L P ", 20, BLACK, 70, 90, self.screen)
        self.start_button.button_draw(self.screen, GREEN)
        draw_text("S T A R T", 85, BLACK, 390, 350, self.screen)
        self.info_button.button_draw(self.screen, WHITE)
        draw_text("S T A T S", 85, BLACK, 390, 450, self.screen)
        self.exit_button.button_draw(self.screen, RED)
        draw_text("E X I T", 85, BLACK, 420, 550, self.screen)

    # //==  ** game loop here  ==// #
    def in_game(self):
        while self.player.alive:
            self.game_event()
            self.game_draw()
            self.game_update()
            self.clock.tick(FPS)
        self.score.save_score(self.player.name, self.player.score, self.player.bag)
        self.game_over()

    # //==  ** game events type here **  ==// #
    def game_event(self):
        self.mx, self.my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.score.save_score(self.player.name, self.player.score, self.player.bag)
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    self.start = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if mouse got pressed
                if pygame.mouse.get_pressed()[0]:
                    # and the position of the mouse is the start button rect
                    if self.button1.rect.collidepoint(self.mx, self.my):
                        self.button1.click()
                    if self.button2.rect.collidepoint(self.mx, self.my):
                        self.button2.click()
                    if self.button3.rect.collidepoint(self.mx, self.my):
                        self.button3.click()
                    if self.menu_button.rect.collidepoint(self.mx, self.my):
                        self.score.save_score(self.player.name, self.player.score, self.player.bag)
                        self.menu()

    # //==  ** Game draw here **  ==// #
    def game_draw(self):
        # //==  ** Screen fill **  ==// #
        self.screen.fill(BLACK)
        # //==  ** Sprite Draw **  ==// #
        self.map_sprite.draw(self.screen)
        self.health_bar.draw(self.screen)
        self.energy_bar.draw(self.screen)
        self.button1.button_draw(self.screen)
        self.button2.button_draw(self.screen)
        self.button3.button_draw(self.screen)
        self.enemy_sprite.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.coin_sprite.draw(self.screen)
        self.potions_sprite.draw(self.screen)
        self.bullet.draw(self.screen)

        # //==  ** Texts **  ==// #
        self.menu_button.button_draw(self.screen, RED)
        draw_text("health: ", 25, WHITE, 10, 20, self.screen)
        draw_text("energy: ", 25, WHITE, 10, 40, self.screen)
        draw_text(f"{self.button3.level} ", 20, WHITE, 920, 15, self.screen)
        draw_text(f"Coins: {round(self.player.bag)} ", 20, WHITE, 920, 35, self.screen)
        draw_text(f"Score: {self.player.score} ", 20, WHITE, 920, 55, self.screen)
        draw_text(f"Energy Cost: {self.button1.cost} ", 20, WHITE, 300, 15, self.screen)
        draw_text(f"Health Cost: {self.button2.cost} ", 20, WHITE, 300, 35, self.screen)
        draw_text(f"Upgrade Cost: {self.button3.cost} ", 20, WHITE, 300, 55, self.screen)

    # //==  ** menu update here **  ==// #
    def game_update(self):
        self.health_bar.update()
        self.energy_bar.update()
        self.player.control()
        self.player.animating_player()
        self.chest.player_interaction(self.player)
        self.bullet.update()
        self.enemy_bullet_collide()
        self.enemy_chance()
        self.thief.animating_player()
        self.chest.enemy_interaction(self.thief, self.player)
        self.Ruby.player_coin(self.player)
        pygame.display.flip()
        pygame.display.update()

    # //==  ** enemy chance **  ==// #
    def enemy_chance(self):
        self.count_time += 1
        self.random_number()
        # there is a 90% chance of enemy spawnning
        if self.chance <= 90:
            self.enemy_sprite.add(self.thief)
            if self.thief.alive:
                self.thief.path()
            else:
                self.thief.kill()

        elif self.chance > 90:
            if self.chance < 94:
                self.potions_sprite.add(self.mini_energy_potion)
                if pygame.sprite.collide_rect(self.player, self.mini_energy_potion):
                    self.mini_energy_potion.effect()
                    self.mini_energy_potion.kill()
                    self.chance = 100
            else:
                self.mini_energy_potion.kill()

            if self.chance >= 94:
                if self.chance < 100:
                    self.potions_sprite.add(self.mini_heal_potion)
                    if pygame.sprite.collide_rect(self.player, self.mini_heal_potion):
                        self.mini_heal_potion.effect()
                        self.mini_heal_potion.kill()
                        self.chance = 100
                else:
                    self.mini_heal_potion.kill()

    # //==  ** collision between enemy sprite and bullet **  ==// #
    def enemy_bullet_collide(self):
        for bullet in self.bullet:
            if pygame.sprite.collide_rect(bullet, self.thief):
                self.thief.health -= 10

    # //==  ** generate a random number **  ==// #
    def random_number(self):
        if self.count_time == 2000:
            self.chance = random.randint(1, 100)
            self.count_time = 0
            self.thief.health = 100.0
            self.thief.go_again()
            # random their location
            self.mini_energy_potion.spawn()
            self.mini_heal_potion.spawn()

    # //==  ** generate a new game **  ==// #
    # //==  ** allows the ability to restart the game and start it **  ==// #
    def start_new_game(self):
        self.player.alive = True
        self.player.health = 500.0
        self.player.energy = 100.0
        self.player.score = 0
        self.player.bag = 0
        self.all_sprites.add(self.player)
        self.coin_sprite.add(self.Ruby)
        self.coin_sprite.add(self.chest)
        self.dungeon_map.add_map()

    # //==  ** Game over loop  **  ==// #
    def game_over(self):
        while self.start:
            self.over_event()
            self.over_draw()
            self.over_update()
            self.clock.tick(FPS)

    # //==  ** Game over event type here **  ==// #
    def over_event(self):
        # We need to get the position in the game loop not just init
        self.mx, self.my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    self.start = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if mouse got pressed
                if pygame.mouse.get_pressed()[0]:
                    # and the position of the mouse is the start button rect
                    if self.replay_button.rect.collidepoint(self.mx, self.my):
                        # then start the game
                        self.start_new_game()
                        self.in_game()
                    if self.back_button.rect.collidepoint(self.mx, self.my):
                        # then go to menu screen
                        self.menu()
                    if self.exit_button2.rect.collidepoint(self.mx, self.my):
                        # then go to exit the game
                        pygame.quit()
                        try:
                            sys.exit()
                        finally:
                            self.start = False

    # //==  ** Game over draw here **  ==// #
    def over_draw(self):
        self.screen.fill(BLACK)
        self.background_screen.blit(self.background_image, [0, 0])
        # texts
        draw_text("Game over", 200, WHITE, 150, 250, self.screen)
        draw_text("Created by: Andromeda#2302 // SaloonaSenpai", 20, WHITE, 370, 750, self.screen)
        # buttons
        self.replay_button.button_draw(self.screen, GREEN)
        draw_text("Play again!", 60, BLACK, 420, 490, self.screen)
        self.back_button.button_draw(self.screen, WHITE)
        draw_text("Back to menu page", 60, BLACK, 355, 590, self.screen)
        self.exit_button2.button_draw(self.screen, RED)
        draw_text("Exit the game", 60, BLACK, 390, 690, self.screen)

    # //==  ** Game over update type here **  ==// #
    def over_update(self):
        # will add things later to get highscore and returns it
        pygame.display.flip()

    # //==  ** stat over loop  **  ==// #
    def stat(self):
        while self.start:
            self.stat_event()
            self.stat_draw()
            self.stat_update()
            self.clock.tick(FPS)

    # //==  ** stat event type here **  ==// #
    def stat_event(self):
        # We need to get the position in the game loop not just init
        self.mx, self.my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    self.start = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if mouse got pressed
                if pygame.mouse.get_pressed()[0]:
                    # and the position of the mouse is the start button rect
                    if self.replay_button.rect.collidepoint(self.mx, self.my):
                        # then start the game
                        self.start_new_game()
                        self.in_game()
                    if self.back_button.rect.collidepoint(self.mx, self.my):
                        # then go to menu screen
                        self.menu()
                    if self.exit_button2.rect.collidepoint(self.mx, self.my):
                        # then go to exit the game
                        pygame.quit()
                        try:
                            sys.exit()
                        finally:
                            self.start = False

    # //==  ** stat  draw here **  ==// #
    def stat_draw(self):
        self.screen.fill(BLACK)
        self.background_screen.blit(self.background_image, [0, 0])
        # texts
        draw_text("Game stat", 100, WHITE, 350, 50, self.screen)
        draw_text("Created by: Andromeda#2302 // SaloonaSenpai", 20, WHITE, 370, 750, self.screen)
        # score test here!
        draw_text(f"Highscore: {self.score.highscore}", 40, YELLOW, 200, 150, self.screen)
        self.score.stat_screen(self.screen)
        # buttons
        self.back_button.button_draw(self.screen, WHITE)
        draw_text("Back to menu page", 60, BLACK, 355, 590, self.screen)
        self.exit_button2.button_draw(self.screen, RED)
        draw_text("Exit the game", 60, BLACK, 390, 690, self.screen)

    # //==  ** Game over update type here **  ==// #
    def stat_update(self):
        # will add things later to get highscore and returns it
        pygame.display.flip()

    # //==  ** stat over loop  **  ==// #
    def help_screen(self):
        while self.start:
            self.help_event()
            self.help_draw()
            self.score.find_highscore()
            pygame.display.flip()
            self.clock.tick(FPS)

    # //==  ** stat event type here **  ==// #
    def help_event(self):
        # We need to get the position in the game loop not just init
        self.mx, self.my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    self.start = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if mouse got pressed
                if pygame.mouse.get_pressed()[0]:
                    # and the position of the mouse is the start button rect
                    if self.replay_button.rect.collidepoint(self.mx, self.my):
                        # then start the game
                        self.start_new_game()
                        self.in_game()
                    if self.back_button.rect.collidepoint(self.mx, self.my):
                        # then go to menu screen
                        self.menu()
                    if self.exit_button2.rect.collidepoint(self.mx, self.my):
                        # then go to exit the game
                        pygame.quit()
                        try:
                            sys.exit()
                        finally:
                            self.start = False

    # //==  ** stat  draw here **  ==// #
    def help_draw(self):
        self.screen.fill(BLACK)
        self.background_screen.blit(self.background_image, [0, 0])
        # texts
        draw_text("Help", 100, WHITE, 350, 50, self.screen)
        draw_text("Created by: Andromeda#2302 // SaloonaSenpai", 20, WHITE, 370, 750, self.screen)
        # buttons
        button = Buttons(100,130, 800,400)
        button.button_draw(self.screen, NotBlue)
        help_image = pygame.image.load("image/help.png")
        help_image_rect = help_image.get_rect()
        help_image_rect.x, help_image_rect.y = 100, 130
        self.screen.blit(help_image, help_image_rect)
        draw_text("Game info", 40, WHITE, 600, 150, self.screen)
        text1 = "Goal of the game is to collect rubies, deposit them into the chest"
        text2 = "Beware of the thief that comes and steals from the chest! "
        text3 = "clicking on yellow potion will refill your energy! careful of the cost!!"
        text4 = "clicking on health potion will refill your health! careful of the cost!!"
        text5 = "clicking on upgrade potion will upgrade your level! careful of the cost!!"
        text6 = "upgrading levels allows double coins and double score!"
        text7 = "if energy is 0 your health will get lower!"
        draw_text(text1, 14, WHITE, 550, 200, self.screen)
        draw_text(text2, 14, WHITE, 550, 220, self.screen)
        draw_text(text3, 14, WHITE, 550, 240, self.screen)
        draw_text(text4, 14, WHITE, 550, 260, self.screen)
        draw_text(text5, 14, WHITE, 550, 280, self.screen)
        draw_text(text6, 14, WHITE, 550, 300, self.screen)
        draw_text(text7, 14, WHITE, 550, 320, self.screen)


        self.back_button.button_draw(self.screen, WHITE)
        draw_text("Back to menu page", 60, BLACK, 355, 590, self.screen)
        self.exit_button2.button_draw(self.screen, RED)
        draw_text("Exit the game", 60, BLACK, 390, 690, self.screen)
