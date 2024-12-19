months = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
}


def main():
    while True:
        date = input("Date: ").strip().title().split()
        if print_iso(date):
            break


def print_iso(date):
    # In "January 1, 1970" format
    if len(date) > 1:
        if date[1].isnumeric() == True:
            return False
        try:
            tmp = int(date[1].replace(",", " "))
        except ValueError:
            return False
        else:
            if date[0] in months and tmp <= 31:
                if tmp < 10:
                    print(f"{date[2]}-{months[date[0]]}-0{tmp}")
                    return True
                else:
                    print(f"{date[2]}-{months[date[0]]}-{tmp}")
                    return True

    # In "1/1/1970" format
    else:
        date = date[0].replace("/", " ").split()
        try:
            tmp0 = int(date[0])
            tmp1 = int(date[1])
        except ValueError:
            return False
        else:
            if tmp1 > 31 or tmp0 > 12:
                return False
            if tmp0 < 10:
                date[0] = "0" + date[0]
            if tmp1 < 10:
                date[1] = "0" + date[1]
            print(f"{date[2]}-{date[0]}-{date[1]}")
            return True
    return False


main()