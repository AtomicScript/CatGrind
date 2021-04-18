from settings import *

class Score:
    def __init__(self):
        self.highscore = ""
        self.data = []
        self.score_file = "score/score.txt"
        self.split_score()
        self.names_list = []
        self.score_list = []
        self.coins_list = []
        self.find_highscore()

    # save score

    def save_score(self, name, score, coin):
        self.score = score
        full_score = f"{name}:{self.score}:{coin},"
        try:
            file = open(self.score_file, "a")
            file.write(full_score)
            file.close()

        except IOError:
            print("Unable to save the score")

        except ValueError:
            print("Value Error")

# find the high score
    def split_score(self):
        self.highscore = 0
        try:
            file = open(self.score_file, "r")
            data = file.read()
            # split the data into a list and that list is the self.data
            self.data = data.split(",")
            file.close()

        except IOError:
            print("Unable to save the score")

        except ValueError:
            print("Value Error")

    def find_highscore(self):
        for scores in self.data:
            try:
                new_score = scores.split(":")
                self.names_list.append(new_score[0])
                extra_score = float(new_score[1])
                self.score_list.append(extra_score)
                extra_coin = int(new_score[2])
                self.coins_list.append(extra_coin)
                max_highscore = max(self.score_list)
                max_highscore_index = self.score_list.index(max_highscore)
                name = self.names_list[int(max_highscore_index)]
                coin = self.coins_list[int(max_highscore_index)]
                self.highscore = f"{name} {max_highscore} {coin}"

                # how to find 4 highest

            except IndexError:
                print("the comma generated a new score that causes the index error")

    def stat_screen(self, screen):
        draw_text(f"Stat #:Name:Score:Coins", 30, YELLOW, 200, 210, screen)
        draw_text(f"Stat 1:{self.data[-2]}", 30, YELLOW, 200, 260, screen)
        draw_text(f"Stat 2:{self.data[-3]}", 30, YELLOW, 200, 310, screen)
        draw_text(f"Stat 3:{self.data[-4]}", 30, YELLOW, 200, 360, screen)
        draw_text(f"Stat 4:{self.data[-5]}", 30, YELLOW, 200, 410, screen)
        draw_text(f"Stat 5:{self.data[-6]}", 30, YELLOW, 200, 460, screen)


shit = Score()
shit.find_highscore()
