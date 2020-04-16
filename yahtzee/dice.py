from random import randint
from collections import OrderedDict

class Dice:
    def __init__(self):
        self.amount_dice = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.scored = {"Aces": '', "Twos": '', "Threes": '', "Fours": '', "Fives": '', "Sixes": '', 'BONUS': 0,
                       'UPPER TOTAL': '', "3 of a Kind": '', "4 of a Kind": '', "Full House": '', "SM Straight": '',
                       "LG Straight": '', "YAHTZEE": '', "Chance": '', "YAHTZEE BONUS": 0, 'LOWER TOTAL': 0,
                       'GRAND TOTAL': 0}
        self.list_of_options = ["Aces", "Twos", "Threes", "Fours", "Fives", "Sixes", "3 of a Kind", "4 of a Kind",
                                "Full House", "SM Straight", "LG Straight", "YAHTZEE", "Chance", "YAHTZEE BONUS"]

    @staticmethod
    def roll(amount):
        dice = []
        for i in range(amount):
            dice.append(randint(1, 6))
        return dice

    def count(self, rolled):
        for dice in rolled:
            self.amount_dice[dice] += 1
        return self.amount_dice

    def options(self):
        option = {"Aces": '', "Twos": '', "Threes": '', "Fours": '', "Fives": '', "Sixes": '', "3 of a Kind": '',
                       "4 of a Kind": '', "Full House": '', "SM Straight": '', "LG Straight": '', "YAHTZEE": '',
                       "Chance": '', "YAHTZEE BONUS": 0}

        three_house = ''
        two_house = ''
        total_point = 0
        for name, amount in self.amount_dice.items():
            # aces, twos, threes, fours, fives, sixes
            if amount > 0:
                title = self.list_of_options[name - 1]
                total = name * amount
                if total == 1:
                    option[title] = total
                else:
                    option[title] = total
            # 3 of kind, 4 of kind, yahtzee
            if amount >= 3:
                total = int(name) * 3
                option[self.list_of_options[6]] = total
            if amount >= 4:
                total = name * 4
                option[self.list_of_options[7]] = total
            if amount == 5:
                if self.scored["YAHTZEE"] == 50:
                    if self.scored['YAHTZEE BONUS'] == 0:
                        option[self.list_of_options[13]] = 100
                    elif self.scored['YAHTZEE BONUS'] == 100:
                        option[self.list_of_options[13]] = 200
                    elif self.scored['YAHTZEE BONUS'] == 200:
                        option[self.list_of_options[13]] = 300
                    self.scored["YAHTZEE BONUS"] = ''

                else:
                    option[self.list_of_options[11]] = 50
            # full house
            if amount == 3:
                three_house = "yes"
            if amount == 2:
                two_house = "yes"
            # chance
            total_point += (int(name) * amount)
            option[self.list_of_options[12]] = total_point
        # full house
        if three_house == "yes" and two_house == "yes":
            option[self.list_of_options[8]] = 25
        # lg straight
        if self.amount_dice[1] >= 1 or self.amount_dice[6] >= 1:
            if self.amount_dice[2] >= 1 and self.amount_dice[3] >= 1 and self.amount_dice[4] >= 1 \
                    and self.amount_dice[5] >= 1:
                option[self.list_of_options[10]] = 40
        # sm straight
        if (self.amount_dice[1] >= 1 and self.amount_dice[2] >= 1 and self.amount_dice[3] >= 1
            and self.amount_dice[4]) or (
                self.amount_dice[2] >= 1 and self.amount_dice[3] >= 1 and self.amount_dice[4] >= 1
                and self.amount_dice[5]) or (
                self.amount_dice[3] >= 1 and self.amount_dice[4] >= 1 and self.amount_dice[5] >= 1
                and self.amount_dice[6]):

            option[self.list_of_options[9]] = 30

        for name, amount in option.items():
            if amount == '':
                option[name] = 0
        self.amount_dice = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        return option

    def score_sheet(self):
        count = 0
        upper_total = 0
        lower_total = 0
        for score in self.scored.values():
            count += 1
            if score != '':
                if count < 7:
                    upper_total += score
                if count > 8 and count < 17:
                    lower_total += score
        if upper_total >= 63:
            self.scored['BONUS'] = 35
            upper_total += 35
        total = upper_total + lower_total
        self.scored['UPPER TOTAL'] = upper_total
        self.scored['LOWER TOTAL'] = lower_total
        self.scored['GRAND TOTAL'] = total


        return self.scored
        # return f"{self.scored}, \n  {upper_total}, \n {lower_total}, \n {total}"

    def add_score(self, choice, amount):
        self.scored[choice] = amount
        return self.score_sheet()


    def score_show(self):
        visible_scores = {}
        for name, score in self.scored.items():
            if score != '':
                visible_scores.update({name: score})
        return visible_scores

game = Dice()

rolled_dice = [1, 1, 1, 1, 1]
print(game.count(rolled_dice))
print(game.options())
print(game.score_sheet())

