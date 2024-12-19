from random import randint
import sys


def main():
    level = get_level()
    score = 0

    # 10 questions
    for _ in range(10):
        a = generate_integer(level)
        b = generate_integer(level)
        correct = a + b
        iteration = 0

        while iteration < 3:
            answer = input(f"{a} + {b} = ")

            try:
                answer = int(answer)
            except ValueError:
                answer = -1

            if correct == answer:
                score += 1
                iteration = 3
            else:
                print("EEE")
                iteration += 1
                if iteration == 3:
                    print(f"{a} + {b} = {correct}")

    print(f"Score: {score}")


def get_level():
    while True:
        try:
            level = int(input("Level: "))
            if 1 <= level <= 3:
                return level
        except ValueError:
            continue


def generate_integer(level):
    # 1, 10, 100
    i = 10 ** (level - 1)

    if level == 1:
        j = 1
    else:
        j = 0

    return randint(i - j, 10 * i - 1)


if __name__ == "__main__":
    main()