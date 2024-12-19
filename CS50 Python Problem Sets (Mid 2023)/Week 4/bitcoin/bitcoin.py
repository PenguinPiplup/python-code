import sys
import requests

def main():
    if len(sys.argv) == 1:
        sys.exit("Missing command-line argument")
    else:
        try:
            amount = float(sys.argv[1])
            response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").json()
        except requests.RequestException:
            sys.exit("Error: could not retrieve data")
        except ValueError:
            sys.exit("Command-line argument is not a number")

    rate = response["bpi"]["USD"]["rate"]
    rate = float(rate.replace(",", ""))
    total = round(rate * amount, 4)
    print(formatting(total))


def formatting(float):
    a = str(float).replace(".", " ").split()

    b = a[0]
    len_b = len(b)
    if len_b > 3:
        b = b[:len_b - 3] + "," + b[len_b - 3:]

    c = a[1]
    if len(a[1]) < 4:
        for _ in range(4 - len(a[1])):
            c += "0"

    return "$" + b + "." + c


if __name__ == "__main__":
    main()