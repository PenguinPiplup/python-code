import datetime
import inflect
import re
import sys

p = inflect.engine()

def main():
    today = datetime.date.today()

    response = input("Date of Birth: ")
    if birth_date := re.search(r"^([0-9]{4})-([0-9]{2})-([0-9]{2})$", response):
        birth_year = int(birth_date.group(1))
        birth_month = int(birth_date.group(2))
        birth_day = int(birth_date.group(3))
        try:
            birthdate = datetime.date(year = birth_year, month = birth_month, day = birth_day)
        except ValueError:
            sys.exit("Invalid date")
        else:
            print(minutes_output(today, birthdate))
    else:
        sys.exit("Invalid date")


def minutes_output(today, birthdate):
    minutes = (today - birthdate).days * 24 * 60
    words = p.number_to_words(minutes, andword="")
    return(words.capitalize() + " minutes")


if __name__ == "__main__":
    main()