def main():
    response = input("What time is it? ").strip().lower()
    time = convert(response)
    if 7.00 <= time <= 8.00:
        print("breakfast time")
    elif 12.00 <= time <= 13.00:
        print("lunch time")
    elif 18.00 <= time <= 19.00:
        print("dinner time")


def convert(response):
    response = response.replace(":", " ").split()
    if len(response) == 3:
        if response[2] == "p.m.":
            return float(response[0]) + float(response[1]) / 60 + 12
        else:
            return float(response[0]) + float(response[1]) / 6
    elif len(response) == 2:
        return float(response[0]) + float(response[1]) / 60
    else:
        return 0.00


if __name__ == "__main__":
    main()