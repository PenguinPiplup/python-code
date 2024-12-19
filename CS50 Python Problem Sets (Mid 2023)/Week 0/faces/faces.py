def main():
    print(convert(input()))


def convert(input):
    input = input.replace(":)", "🙂")
    return input.replace(":(", "🙁")


main()