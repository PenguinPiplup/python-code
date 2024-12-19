def main():
    fract = input("Fraction: ").strip()
    print(gauge(convert(fract)))


def convert(fract):
    fraction = fract.split("/")
    try:
        X = int(fraction[0])
        Y = int(fraction[1])
    except ValueError:
        raise ValueError("X or Y must be an integer")

    if Y == 0:
        raise ZeroDivisionError("Y cannot be 0")

    if X > Y:
        raise ValueError("X must be less than Y")

    decimal = X / Y
    if decimal < 0 or decimal > 1.00:
        return convert(input("Fraction: ").strip())
    else:
        return round(decimal * 100)


def gauge(percentage):
    if percentage <= 1:
        return("E")
    elif percentage < 99:
        return(f"{percentage}%")
    elif percentage <= 100:
        return("F")


if __name__ == "__main__":
    main()
