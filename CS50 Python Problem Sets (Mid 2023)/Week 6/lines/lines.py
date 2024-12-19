import sys

def main():
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")
    elif not sys.argv[1].endswith(".py"):
        sys.exit("Not a Python file")

    try:
        with open(sys.argv[1]) as file:
            lines = file.readlines()
            counter = 0

            for line in lines:
                line = line.strip()
                if len(line) > 0:
                    if line[0] != "#":
                        counter += 1
    except FileNotFoundError:
        sys.exit("File does not exist")
    else:
        print(counter)


if __name__ == "__main__":
    main()