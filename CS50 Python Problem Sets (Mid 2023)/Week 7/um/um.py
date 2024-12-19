import re
import sys


def main():
    print(count(input("Text: ")))


def count(s):
    s = " " + s.strip() + " "
    list = re.findall('(\W)+(um){1}(\W)+', s, re.IGNORECASE)
    return len(list)


if __name__ == "__main__":
    main()