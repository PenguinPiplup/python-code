while True:
    try:
        fraction = input("Fraction: ").strip().replace("/", " ").split()
        decimal = int(fraction[0]) / int(fraction[1])
        if decimal < 0:
            tmp = 3 / 0
        elif decimal <= 0.01:
            print("E")
            break
        elif decimal < 0.99:
            print(f"{round(decimal * 100)}%")
            break
        elif decimal <= 1.00:
            print("F")
            break
        else:
            tmp = 3 / 0

    except ZeroDivisionError:
        pass
    except ValueError:
        pass



