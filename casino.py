from random import choice, randint
from typing import Dict, List, Set, Tuple
import collections
from datetime import datetime
import pandas as pd
import csv
import sys
import time
import functools
import os
from dice_img import dice_ascii
from coin_img import coin_ascii
from RPS_img import rock_paper_scissors_ascii

AGREE: Tuple[str] = (
    "y",
    "yeah",
    "1",
    "of course",
    "sure",
    "yes",
    "yeap",
    "right",
    "proceed",
    "agree",
    "agreed",
    "say when",
)

path = "payment_history.csv"


class Account:
    def __init__(self, money: int = 0) -> None:
        self.money = money
        self.loaned = 0

    def __add__(self, val2):
        return Account(self.money + val2.money)

    def __str__(self) -> str:
        return f"You got {self.money} money, you've loaned {self.loaned}"

    def deposit(self, cash_in: int) -> int:
        if cash_in < 0:
            print("You can't deposit negative amount")
        else:
            self.money += cash_in
        return self.money

    def loan(self, amount) -> int:
        if self.loaned < 0:
            print("You gotta pay your debt, before loaning again")
        else:
            self.loaned -= amount + amount // 10
            self.money += amount
        return self.money

    def payDebt(self) -> str:
        if self.loaned >= 0:
            return "You don't have any money loaned, to pay debt"
        else:
            self.money += self.loaned
            self.loaned = 0
            return "You don't have no loanes left"


class Casino:
    def __init__(self, account: Account):
        self.account = account
        self.money = account.money

    def __str__(self) -> str:
        return f"This is a casino, your bank account is {self.account.money}\n what do you wanna play?"

    @staticmethod
    def print_history() -> None:
        os.system("cls" if os.name == "nt" else "clear")

        def generator():
            df = pd.read_csv(path)
            for _, row in df.iterrows():
                yield ", ".join(map(str, row.values))

        generator_object = generator()
        for row in generator_object:
            print(row)

    def update_history(self, curr_game, bet) -> None:
        with open(path, "a") as csvfile:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            data: Dict[str, int] = {
                "time": dt_string,
                "game": curr_game,
                "money_spent": bet,
                "balance": self.money,
            }
            fieldnames: List[str] = ["time", "game", "money_spent", "balance"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(data)

    # Generator opens csv () file, yield through it returning values from balance column in csvfile
    # BTW it returns cash in str formats
    @staticmethod
    def cash_generator():
        df = pd.read_csv(path, usecols=["balance"])
        for _, row in df.iterrows():
            yield " ".join(map(str, row.values))

    def biggest_cash(self) -> int:
        cash_history: Set[int] = set()
        generator_object = self.cash_generator()
        for row in generator_object:
            cash_history.add(int(row))

        return max(cash_history)

    def most_common_cash(self) -> str:
        cash_hashmap: Dict[str, int] = dict()
        generator_object = self.cash_generator()
        for row in generator_object:
            if row not in cash_hashmap:
                cash_hashmap[row] = 1
            else:
                cash_hashmap[row] += 1

        most_common_cash: Tuple["int", int] = sorted(
            cash_hashmap.items(), key=lambda x: x[1]
        )[-1]
        return f"Your most common cash amount is {most_common_cash[0]} you had it {most_common_cash[1]} times"

    def dice_game(self, bet: int, predict: int) -> str:
        if self.money <= 0:
            return "You ain't got no money pal"
        elif self.money < bet:
            return f"Your bet {bet} you've to bet less than {self.money}"
        dice: int = randint(1, 6)
        if predict == dice:
            self.money = bet * 6 + self.money
        else:
            self.money -= bet

        self.update_history("dice", bet)
        os.system("cls" if os.name == "nt" else "clear")
        print(dice_ascii(dice))
        return f"Dice rolled {dice} your prediction was {predict} and your balance is {self.money}"

    def flip_coin(self, bet: int, predict: str) -> str:
        class NoMoneyError(Exception):
            def __init__(self, message):
                self.message = message

        if bet > self.money:
            raise NoMoneyError("You bet too much")

        heads: List[str] = ["heads", "h", "head", "1", "0"]
        tails: List[str] = ["tails", "t", "tail", "2"]
        coin: int = choice(["heads", "tails"])

        if (
            predict.lower() in tails
            and coin == "tails"
            or predict.lower() in heads
            and coin == "heads"
        ):
            self.money = bet + self.money
        else:
            self.money -= bet
        self.update_history("flip_coin", bet)
        os.system("cls" if os.name == "nt" else "clear")
        print(coin_ascii(coin))
        return f"Your prediction was {predict}, coin dropped {coin}, your balance is {self.money}"

    def rock_paper_scissors(self, bet: int, predict: str) -> str:
        options_power = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
        robots_choice = choice(["rock", "paper", "scissors"])
        if options_power[predict] == robots_choice:
            self.money = bet * 2 + self.money
            self.update_history("rock_paper_scissors", bet)
            os.system("cls" if os.name == "nt" else "clear")
            print(rock_paper_scissors_ascii(predict, robots_choice))
            return f"You've won, you {predict} enemy {robots_choice}, your balance {self.money}"
        elif robots_choice == predict:
            self.update_history("rock_paper_scissors", bet)
            os.system("cls" if os.name == "nt" else "clear")
            print(rock_paper_scissors_ascii(predict, robots_choice))
            return f"It's draw, you {predict} enemy {robots_choice}, your balance {self.money}"
        else:
            self.money -= bet
            self.update_history("rock_paper_scissors", bet)
            os.system("cls" if os.name == "nt" else "clear")
            print(rock_paper_scissors_ascii(robots_choice, predict))
            return f"You've lost, you {predict} enemy {robots_choice}, your balance {self.money}"

    def slotMachine(self) -> str:
        food: List[str] = ["🍎", "🍊", "🍌", "🍓", "💎"]
        spin_cost: int = 100
        jackpot_line: str = "/Jackpot\\"
        money_before: int = self.money

        def spin() -> List[str]:
            user_results: List[List[str]] = [
                [choice(food), choice(food), choice(food)],
                [choice(food), choice(food), choice(food)],
                [choice(food), choice(food), choice(food)],
            ]
            return user_results

        def ending(jackpot="---------") -> None:
            os.system("cls" if os.name == "nt" else "clear")
            self.money -= spin_cost
            self.update_history("slotMachine", spin_cost)
            print(f" /{jackpot}\\")
            print("/-----------\\")
            time.sleep(0.1)
            print(f"| {"| ".join(user_results[0])}|")
            time.sleep(0.1)
            print(f"|---|---|---|\n| {"| ".join(user_results[1])}| ")
            time.sleep(0.1)
            print(f"|---|---|---|\n| {"| ".join(user_results[2])}| ")
            time.sleep(0.1)
            print("-------------")

        while input(f"Wanna spin {spin_cost}$ per spin yes or no\n").lower() in AGREE:
            if self.money < spin_cost:
                return "You don't have enough money"

            user_results = spin()
            results = set()
            for result_list in user_results:
                for result in result_list:
                    results.add(result)

            horizontal: List[List[int]] = [
                [user_results[0][i] for i in range(3)],
                [user_results[1][i] for i in range(3)],
                [user_results[2][i] for i in range(3)],
            ]

            vertical: List[List[int]] = [
                [user_results[i][0] for i in range(3)],
                [user_results[i][1] for i in range(3)],
                [user_results[i][2] for i in range(3)],
            ]

            if len(collections.Counter(results)) == 1:
                if horizontal[0][0] == "💎":
                    self.money = spin_cost * 10000 + self.money
                    ending(jackpot_line)
                elif horizontal[0][0] == "🍓":
                    self.money = spin_cost * 3000 + self.money
                    ending(jackpot_line)
                else:
                    self.money = spin_cost * 1500 + self.money
                    ending(jackpot_line)

            for i in range(3):
                if horizontal[i][0] == horizontal[i][1] == horizontal[i][2]:
                    if horizontal[i][0] == "💎":
                        self.money = spin_cost * 60 + self.money
                    elif horizontal[i][0] == "🍓":
                        self.money = spin_cost * 30 + self.money
                    else:
                        self.money = spin_cost * 15 + self.money
                elif vertical[i][0] == vertical[i][1] == vertical[i][2]:
                    if vertical[i][0] == "💎":
                        self.money = spin_cost * 60 + self.money
                    elif vertical[i][0] == "🍓":
                        self.money = spin_cost * 30 + self.money
                    else:
                        self.money = spin_cost * 15 + self.money
            ending()
            print(f"Your cash is {self.money}")
        return f"You earned {self.money - money_before}"


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        before = time.time()
        func(*args, **kwargs)
        after = time.time()
        return f"Function {func.__name__} finished just in {after - before:.2f} seconds"

    return wrapper


@timer
def game_on():
    class WrongNumberError(Exception):
        def __init__(self, message):
            self.message = message

    with open(path, "r") as file:
        last_cash = int(file.readlines()[-1].split(",")[-1])
    if len(sys.argv) == 2:
        user = Account(int(sys.argv[1]))
        print(f"Your cash amount is {sys.argv[1]}$")
    else:
        user_cash_choice = int(
            input("Do you wanna restore previous cash (1), or store new(2)?\n")
        )

        if user_cash_choice == 1:
            user = Account(last_cash)
            print(f"Your last cash amount is {last_cash}$")
        else:
            user = Account(
                int(input("How much bucks do u wanna put on your account:\n"))
            )

    casino = Casino(user)
    play_count = 0

    while input(f"Wanna play{" again " if play_count > 0 else ""}?\n") in AGREE:
        os.system("cls" if os.name == "nt" else "clear")
        play_choice = int(
            input(
                "What would you like to play:\n"
                "1: Dice\n"
                "2: Flip Coin\n"
                "3: Slot Machine\n"
                "4: Rock Paper Scissors\n"
                "5: Print History\n"
                "6: Max Cash Ever Got\n"
                "7: Average Cash Amount\n"
                "Enter your choice: "
            )
        )
        if play_choice == 1:
            print(f"Your cash amount is {casino.money}$")
            bet = int(input("How much do you wanna bet: \n"))
            predict = int(input("What do you think dice will drop: \n"))
            print(casino.dice_game(bet, predict))
            play_count += 1
        elif play_choice == 2:
            print(f"Your cash amount is {casino.money}$")
            bet = int(input("How much do you wanna bet: \n"))
            predict = input("Choose side of a coin, heads or tails: \n")
            print(casino.flip_coin(bet, predict))
            play_count += 1
        elif play_choice == 3:
            print(casino.slotMachine())
            play_count += 1
        elif play_choice == 4:
            print(f"Your cash amount is {casino.money}$")
            bet = int(input("How much do you wanna bet: \n"))
            predict = input("Rock, paper or scissors\n").lower()
            print(casino.rock_paper_scissors(bet, predict))
            play_count += 1
        elif play_choice == 5:
            casino.print_history()
            play_count += 1
        elif play_choice == 6:
            print(f"Most cash you ever got is {casino.biggest_cash()}$")
            play_count += 1
        elif play_choice == 7:
            print(casino.most_common_cash())
            play_count += 1
        else:
            print("You pick the wrong number")
            raise WrongNumberError(f"You picked {play_choice} there are 7 choices")


if __name__ == "__main__":
    print(game_on())
