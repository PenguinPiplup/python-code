import inflect
p = inflect.engine()


def main():
    names = get_names()
    print_output(names)


def get_names():
    names = []
    while True:
        try:
            name = input("Name: ")
            if len(name) > 0:
                names.append(name)
        except EOFError:
            print()
            return names


def print_output(names):
    output = "Adieu, adieu, to " + p.join(names)
    print(output)



if __name__ == "__main__":
    main()
