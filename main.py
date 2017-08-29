import random


class App:
    def __init__(self):
        self.total = 0
        self.opponent_total = 0
        self.dice_count = 6
        self.put_away_dices = []
        self.turn_total = 0
        self.dice_declination = {1: "kostka", 2: "kostky", 3: "kostky", 4: "kostky", 5: "kostek", 6: "kostek"}
        self.zbyva_declination = {1: "zbývá", 2: "zbývají", 3: "zbývají", 4: "zbývají", 5: "zbývá", 6: "zbývá"}

    def roll_dices(self):
        result_of_roll = []
        for i in range(self.dice_count):
            result_of_roll.append(random.randrange(1, 7))
        print("Hodil jste %s" % (", ".join(str(v) for v in result_of_roll)))

        indexes = []
        for index, number in enumerate(result_of_roll):
            if number == 5:
                indexes.append(index)
        for index, result in enumerate(indexes):
            result_of_roll[result], result_of_roll[self.dice_count - 1 - index] = \
                result_of_roll[self.dice_count - 1 - index], result_of_roll[result]
        self.conclude(result_of_roll)

    def conclude(self, result_of_roll):
        before_turn = self.turn_total
        summary_of_result = {}
        for result in result_of_roll:
            summary_of_result[result] = 1 if result not in summary_of_result.keys() else summary_of_result[result] + 1

        for key, value in summary_of_result.items():
            if value >= 3:
                for i in range(value):
                    self.put_away_dices.append(key)
                    result_of_roll.remove(key)
                if key == 1:
                    self.turn_total += 100 * key * (2**(value-3))
                else:
                    self.turn_total += 10 * key * (2**(value-3))

            elif len(summary_of_result) == 6:
                print("Hodil jste řadu!")
                self.turn_total += 100
                break

            elif key == 1 and value <= 3:
                self.turn_total += value * 10
                for i in range(value):
                    self.put_away_dices.append(key)
                    result_of_roll.remove(key)

            elif key in self.put_away_dices:
                for i in range(value):
                    summary_of_putaway = {}
                    for dice in self.put_away_dices:
                        summary_of_putaway[dice] = 1 if dice not in summary_of_putaway.keys() else summary_of_putaway[
                                                                                                         dice] + 1
                    if summary_of_putaway[key] > 2:
                        self.turn_total += 10 * key * (2 ** (summary_of_putaway[key] - 3))
                        result_of_roll.remove(key)
                        self.put_away_dices.append(key)

            elif key == 5 and value <= 3:
                print("Máte %d bodů, zbývají vám kostky %s" % (self.turn_total, ", ".join(str(v) for v in result_of_roll)))
                inp = input("Chcete odložit pětku? A/N")
                if inp == "A" or inp == "a":
                    self.turn_total += 5
                    result_of_roll.remove(5)
                    self.put_away_dices.append("5")
                if value == 2 and inp == "A":
                    inp = input("Chcete odložit i druhou pětku? A/N")
                    if inp == "A" or inp == "a":
                        self.turn_total += 5
                        result_of_roll.remove(5)
                        self.put_away_dices.append("5")

        if before_turn == self.turn_total and 5 not in result_of_roll:
            print("Bohužel se Vám nepoštěstilo, ztrácíte body z tohoto kola")
            self.put_away_dices = []
            self.dice_count = 6
        else:
            if len(self.put_away_dices) == 6:
                self.put_away_dices = []
                self.dice_count = 6
            else:
                self.dice_count = 6 - len(self.put_away_dices)
            inp = input("Máte %d bodů. %s vám %d %s. Chcete házet znovu? A/N" % (self.turn_total,
                                                                                 self.zbyva_declination[self.dice_count],
                                                                                 self.dice_count,
                                                                                 self.dice_declination[self.dice_count]))
            if inp == "A" or inp == "a":
                self.roll_dices()
            else:
                self.total += self.turn_total


if __name__ == "__main__":
    dices = App()
    dices.roll_dices()
