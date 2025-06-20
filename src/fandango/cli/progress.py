#!/usr/bin/env python

import os
import random
import time

from ansi_styles import ansiStyles as styles

FITNESS: list[float] = []

COLUMNS, LINES = os.get_terminal_size()


def progress():
    columns = COLUMNS
    s = f"💃 {styles.color.ansi256(styles.rgbToAnsi256(128, 0, 0))}Fandango {styles.color.close}"
    columns -= len("   Fandango ")
    columns //= 3
    for column in range(0, int(columns)):
        individual = int(column / columns * len(FITNESS))
        fitness = FITNESS[individual]
        if fitness == 0:
            emoji = "💀"
        elif fitness < 50:
            emoji = "🥵"
        elif fitness < 99:
            emoji = "🙂"
        else:
            emoji = "🤩"

        emoji = " "
        percentage = fitness / 100

        if fitness == 0:
            red, green, blue = 0, 0, 0
        else:
            red = int((1.0 - percentage) * 255)
            green = int(percentage * 255)
            blue = 0

        s += styles.bgColor.ansi256(styles.rgbToAnsi256(red, green, blue))
        s += " " + emoji + " "
        s += styles.bgColor.close

    print(f"\r{s}", end="")
    return


def clear():
    s = " " * (COLUMNS - 1)
    print(f"\r{s}\r", end="")


if __name__ == "__main__":
    FITNESS = [0] * 500

    while not all(individual == 100 for individual in FITNESS):
        while True:
            individual = random.randint(0, len(FITNESS) - 1)
            if FITNESS[individual] < 100:
                break

        FITNESS[individual] = min(FITNESS[individual] + 10, 100)
        FITNESS.sort(reverse=True)
        progress()
        time.sleep(0.001)
    clear()
