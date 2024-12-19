def main():
    answer = input("Greeting: ")
    print(f"${value(answer)}")


def value(greeting):
    greeting = greeting.strip().title()
    if (len(greeting) == 0):
        return 100
    elif greeting[0] == "H":
        reduced = greeting[:5]
        if reduced == "Hello":
            return 0
        else:
            return 20
    else:
        return 100


if __name__ == "__main__":
    main()