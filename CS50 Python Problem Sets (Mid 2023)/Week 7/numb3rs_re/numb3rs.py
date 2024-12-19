import re
import sys


def main():
    print(validate(input("IPv4 Address: ")))


def validate(ip):
    if re.search(r"^([0-9]{1,3}\.{1}){3}[0-9]{1,3}$", ip):
        splitted = ip.split(".")
        for number in splitted:
            if int(number) > 255:
                return False
        return True
    else:
        return False


if __name__ == "__main__":
    main()