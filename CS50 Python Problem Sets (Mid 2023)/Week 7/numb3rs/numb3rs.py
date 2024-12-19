import re
import sys


def main():
    print(validate(input("IPv4 Address: ")))


def validate(ip):
    ip_list = ip.strip().split(".")
    if len(ip_list) != 4:
        return False
    for mini_str in ip_list:
        try:
            number = int(mini_str)
        except ValueError:
            return False
        else:
            if number < 0 or number > 255:
                return False

    return True


if __name__ == "__main__":
    main()