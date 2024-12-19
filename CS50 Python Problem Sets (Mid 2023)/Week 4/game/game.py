from random import randint

while True:
    try:
        level = int(input("Level: "))
        if level >= 1:
            break
    except ValueError:
        continue

ans = randint(1, level)

while True:
    try:
        guess = int(input("Guess: "))
        if guess < ans:
            print("Too small!")
        elif guess > ans:
            print("Too large!")
        else:
            print("Just right!")
            break
    except ValueError:
        continue