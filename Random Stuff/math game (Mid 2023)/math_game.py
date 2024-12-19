import sys
from math import floor
from random import randint
from time import sleep
from timeit import default_timer

# Global variables
repeat = 5
number_of_levels = 10
score = 0
time_limit = [15, 12, 10, 8.5, 7, 6, 5.5, 5, 4.5, 4]
win_status = 1
lose_status = 0


def main():
    # Print game introduction and instructions
    intro()

    # Go through levels 1 to 10
    for level_number in range(1, number_of_levels + 1):
        print(f"Welcome to level {level_number}! (Time limit: {time_limit[level_number - 1]} seconds)")
        sleep(0.7)

        # Come up with "repeat" number of math questions for each level
        for question_number in range(repeat):
            if not level(level_number):
                # End the game and print score if user answered question wrongly/ran out of time
                print(f"Unfortunately, you lost.\nFinal score: {floor(score)}")
                return 0

    # Print congratulatory message and score if user answered all questions correctly within time limit
    print(f"Congratulations! You won the game!\nFinal score: {floor(score)}")
    return 0


def intro():
    print("                             ", end='')
    fancy_print("Welcome to the math game\n\n", end='')
    sleep(0.2)

    fancy_print("Do you wish to skip the instructions for this game? ", end='')
    input_1 = input().strip().lower()
    if input_1[0:1] != 'y' or len(input_1) == 0:
        print_instructions()

    # Ensure that the player is ready to begin the game
    input_2 = "n"
    while input_2[0:1] == "n":
        input_2 = input("Are you ready to start? ").strip().lower()

    fancy_print("Let's begin!\n\n", end='')
    sleep(1)


def print_instructions():
    # Print instructions for the game
    fancy_print("\nIn this game, you will be shown simple math equations and your job is to deduce ", end='')
    fancy_print("whether they are correct, \nwithin the time limit provided.\n", end='')
    fancy_print("Before the time is up, you should type 'y', 'c', 't' or '1' if the equation is correct.\n", end='')
    fancy_print("You should type 'n', 'w', 'f' or '2' instead if the equation is wrong.\n", end='')
    print("(y = yes, c = correct, t = true, 1); (n = no, w = wrong, f = false, 2)\n")
    fancy_print("The amount of time given for each question will decrease as you progress through the levels.\n", end='')
    fancy_print(f"There are {number_of_levels} levels in total, and {repeat} questions within each level.\n", end='')
    fancy_print("\nThe amount of time given for each question is as follows: \n", end='')
    for i in range(number_of_levels):
        fancy_print(f"Level {i + 1} - {time_limit[i]} seconds\n", end='')
    fancy_print("\nAdditionally, your final score will vary depending on how quickly you answer each question.\n", end='')


def level(level_number):
    global score

    # Randomly generate two numbers and one operator (1 means '+', 2 means '-', 3 means 'x', 4 means '/')
    a = randint(1, 100)
    b = randint(1, 100)
    operator = randint(1, 4)

    # If 1, user must choose correct. If 0, user must choose wrong
    tickorcross = randint(1, 2) - 1

    # Trickyyyyy
    tricky = randint(1, level_number + 20)

    match operator:
        case 1:
            # Calculate correct value and generate wrong value
            correct = a + b
            wrong = randint(1, 200)
            if correct == wrong:
                wrong += 1
            if tricky > 16 and tricky % 2 == 1:
                wrong = correct + 10
            elif tricky > 16 and tricky % 2 == 0:
                wrong = correct - 10

            if tickorcross:
                print(f"{a} + {b} = {correct}")
            else:
                print(f"{a} + {b} = {wrong}")
        case 2:
            correct = a - b
            wrong = randint(-100, 100)
            if correct == wrong:
                wrong += 1
            if tricky > 16 and tricky % 2 == 1:
                wrong = correct + 10
            elif tricky > 16 and tricky % 2 == 0:
                wrong = correct - 10

            if tickorcross:
                print(f"{a} - {b} = {correct}")
            else:
                print(f"{a} - {b} = {wrong}")
        case 3:
            # b will be a number between 2 and 16 inclusive to make the game more manageable for 'x'
            b = b % 15 + 2
            correct = a * b
            wrong = randint(1, 1584)
            if correct == wrong:
                wrong += 1
            if tricky > 16 and tricky % 2 == 1:
                wrong = correct + 10
            elif tricky > 16 and tricky % 2 == 0:
                wrong = correct - 10

            if tickorcross:
                print(f"{a} x {b} = {correct}")
            else:
                print(f"{a} x {b} = {wrong}")
        case 4:
            # b will be a number between 2 and 12 inclusive to make the game more manageable for '/'
            b = b % 11 + 2
            correct = a * b
            correct, a = a, correct
            wrong = randint(1, 100)
            if correct == wrong:
                wrong += 1
            if tricky > 16 and tricky % 2 == 1:
                wrong = correct + 10
            elif tricky > 16 and tricky % 2 == 0:
                wrong = correct - 10

            if tickorcross:
                print(f"{a} / {b} = {correct}")
            else:
                print(f"{a} / {b} = {wrong}")

    # Get user answer and calculate time taken for user to answer
    before_time = default_timer()
    response = convert(input().strip().lower())
    after_time = default_timer()
    time_lapsed = after_time - before_time

    if response == tickorcross and time_lapsed <= time_limit[level_number - 1]:
        # Lousy algorithm to compute score based on level number and amount of time left
        score += level_number / 3 + 1
        extra_time = time_limit[level_number - 1] - time_lapsed
        extra_score = (extra_time * level_number / 3) / time_limit[level_number - 1]
        score += extra_score
        print(f"Score: {floor(score)}\n")
        return win_status
    elif response != tickorcross and tickorcross == 0:
        print("Wrong response. The equation was indeed wrong.")
        return lose_status
    elif response != tickorcross and tickorcross == 1:
        print("Wrong response. The equation was indeed correct.")
        return lose_status
    else:
        print(f"Correct response. However, you ran out of time. You took {time_lapsed:.2f} seconds, ", end='')
        print(f"more than the {time_limit[level_number - 1]} seconds provided.")
        return lose_status


def convert(user_input):
    if user_input[0:1] == 'y' or user_input[0:1] == 'c' or user_input[0:1] == 't' or user_input[0:1] == '1':
        return 1
    elif user_input[0:1] == 'n' or user_input[0:1] == 'w' or user_input[0:1] == 'f' or user_input[0:1] == '2':
        return 0
    else:
        print("Error: Please type 'y', 'c', 't' or '1' if equation is correct.")
        print("       Please type 'n', 'w', 'f' or '2' if equation is wrong.")
        return convert(input().strip().lower())


def fancy_print(fancy_text, end=''):
    for i in fancy_text:
        print(i, end='')
        sys.stdout.flush()
        sleep(0.04)


if __name__ == "__main__":
    main()
