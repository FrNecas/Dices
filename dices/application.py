import random


class App:
    def __init__(self):
        self.total = 0
        self.opponent_total = 0
        self.dice_count = 6
        self.put_away_dices = []
        self.turn_total = 0
        self.dice_declination = {1: "dice", 2: "dices", 3: "dices", 4: "dices", 5: "dices", 6: "dices"}
        # sets declination for sentences

    def roll_dices(self, player):
        result_of_roll = []
        for i in range(self.dice_count):
            result_of_roll.append(random.randrange(1, 7))
        if player == "user":
            print("You rolled %s" % (", ".join(str(v) for v in result_of_roll)))

        indexes = []
        for index, number in enumerate(result_of_roll):  # finds indexes of number 5 and puts them at the end of a list
            if number == 5:
                indexes.append(index)
        for index, result in enumerate(indexes):
            result_of_roll[result], result_of_roll[self.dice_count - 1 - index] = \
                result_of_roll[self.dice_count - 1 - index], result_of_roll[result]
        self.conclude(result_of_roll, player)

    def conclude(self, result_of_roll, player):
        before_turn = self.turn_total
        summary_of_result = {}
        for result in result_of_roll:  # makes a dict from a list
            summary_of_result[result] = 1 if result not in summary_of_result.keys() else summary_of_result[result] + 1

        for key, value in summary_of_result.items():  # concludes result according to game rules
            if value >= 3:
                for i in range(value):
                    if key != 1:  # condition to control whether 1 has been put away as 10 or 100
                        self.put_away_dices.append(key)
                    else:
                        self.put_away_dices.append("1")
                    result_of_roll.remove(key)
                if key == 1:
                    self.turn_total += 100 * key * (2**(value-3))
                else:
                    self.turn_total += 10 * key * (2**(value-3))  # calculation on points 10 * x (2**(a-3))

            elif len(summary_of_result) == 6:
                if player == "user":
                    print("You got a row and got 100 points!")
                self.turn_total += 100
                break

            elif key == 1 and value <= 3 and "1" not in self.put_away_dices:
                self.turn_total += value * 10
                for i in range(value):
                    self.put_away_dices.append(key)
                    result_of_roll.remove(key)

            elif "1" in self.put_away_dices and 1 in result_of_roll:  # condition for 3 put away 1s at once
                summary_of_putaway = {}
                for dice in self.put_away_dices:
                    summary_of_putaway[dice] = 1 if dice not in summary_of_putaway.keys() else summary_of_putaway[
                                                                                                   dice] + 1
                if summary_of_putaway["1"] > 2:
                    self.turn_total += 100 * (2 ** (summary_of_putaway["1"] - 3))
                    result_of_roll.remove(key)
                    self.put_away_dices.append("1")

            elif key in self.put_away_dices:  # checks dices already put away
                for i in range(value):
                    summary_of_putaway = {}
                    for dice in self.put_away_dices:
                        summary_of_putaway[dice] = 1 if dice not in summary_of_putaway.keys() else summary_of_putaway[
                                                                                                         dice] + 1
                    if summary_of_putaway[key] > 2:
                        self.turn_total += 10 * key * (2 ** (summary_of_putaway[key] - 3))
                        result_of_roll.remove(key)
                        self.put_away_dices.append(key)

        if 5 in summary_of_result.keys() and summary_of_result[5] <= 2:  # 5 condition is triggered
                                                                        # after everything else is calculated
            if player == "user":
                print("You have %d points and remaining dices %s" % (self.turn_total, ", ".join(str(v) for v in
                                                                                                result_of_roll)))
                inp = input("Do you want to put away 5? Y/N")
                if inp == "Y" or inp == "y":
                    self.turn_total += 5
                    result_of_roll.remove(5)
                    self.put_away_dices.append("5")
                if summary_of_result[5] == 2 and (inp == "Y" or inp == "y"):
                    inp = input("Do you want to put away 2nd 5? Y/N")
                    if inp == "Y" or inp == "y":
                        self.turn_total += 5
                        result_of_roll.remove(5)
                        self.put_away_dices.append("5")
            else:
                if len(result_of_roll) == 1:
                    self.turn_total += 5
                    result_of_roll.remove(5)
                    self.put_away_dices.append("5")
                if len(result_of_roll) == [5, 5]:
                    self.turn_total += 10
                    for i in range (2):
                        result_of_roll.remove(5)
                        self.put_away_dices.append("5")

        if len(self.put_away_dices) == 6:
            self.put_away_dices = []
            self.dice_count = 6
        else:
            self.dice_count = 6 - len(self.put_away_dices)

        if before_turn == self.turn_total and 5 not in result_of_roll:  # if nothing has changed you lose
            if player == "user":
                print("Unfortunately you were unlucky and you lose all points from this round")
                print(50 * "_")
            self.turn_total = 0
            self.put_away_dices = []
            self.dice_count = 6
        else:
            if player == "user":
                answered = False
                while not answered:
                    inp = input("You have %d points. You have %d %s remaining. Do you want to roll again? Y/N" % (
                        self.turn_total, self.dice_count, self.dice_declination[self.dice_count]))
                    print(50 * "_")
                    if inp == "Y" or inp == "y":
                        answered = True
                        self.roll_dices(player)
                    elif inp == "N" or inp == "n":
                        answered = True
                        self.total += self.turn_total
                        self.turn_total = 0
                        self.dice_count = 6
                        self.put_away_dices = []
                        return
                    else:
                        print("Wrong input")
            else:
                if self.dice_count in (4, 5, 6) or (len(self.put_away_dices) in (3, 4) and 100 >= self.turn_total >= 20):
                    self.roll_dices(player)
                elif self.turn_total >= 100:
                    self.opponent_total += self.turn_total
                    self.turn_total = 0
                    self.dice_count = 6
                    self.put_away_dices = []
                    return

def main():
    try:
        answered = False
        while not answered:
            try:
                final_points = int(input("On how many points would you like the game to end?"))
                answered = True
                print(50 * "=")
            except ValueError:
                print("Wrong input")
        dices = App()
        while dices.total < final_points and dices.opponent_total < final_points:
            dices.roll_dices("user")
            dices.roll_dices("bot")
            print("Your opponent has %d points, you have %d points" % (dices.opponent_total, dices.total))
            print(50 * "=")

    except KeyboardInterrupt:
        print("Terminated")

