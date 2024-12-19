import csv
import sys
from tabulate import tabulate

def main():
    arg_count = len(sys.argv)
    if arg_count < 2:
        sys.exit("Too few command-line arguments")
    elif arg_count > 2:
        sys.exit("Too many command-line arguments")
    elif not sys.argv[1].endswith(".csv"):
        sys.exit("Not a CSV file")

    try:
        prices = []
        with open(sys.argv[1]) as file:
            data = csv.DictReader(file)
            for dict in data:
                prices.append(dict)
    except FileNotFoundError:
        sys.exit("File does not exist")
    else:
        print(tabulate(prices, headers = "keys", tablefmt = "grid"))


if __name__ == "__main__":
    main()