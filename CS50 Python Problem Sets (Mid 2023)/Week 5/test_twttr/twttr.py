def main():
    output = shorten(input("Input: "))
    print("Output: " + output)


def shorten(response):
    string = "AEIOUaeiou"
    list = []
    for char in string:
        list.append(char)

    for char in list:
        response = response.replace(char, "")
    return response


if __name__ == "__main__":
    main()