import re
import sys

def main():
    print(convert(input("Hours: ")))


def convert(s):
    s = s.strip()
    if re_output := re.search(r"^([0-9:]+)\s{1}(AM|PM)(?:\sto\s){1}([0-9:]+)\s{1}(AM|PM)$", s):
        start_time, start_meridiem, end_time, end_meridiem = re_output.groups()


        # Start of process()
        def process(time, meridiem):
            time = time.split(":")

            # Calculate a constant that will be used later to adjust the timing to 24-hour version
            if meridiem == "AM":
                meridiem_adjust = 0
            else:
                meridiem_adjust = 12

            if time[0] == "12":
                meridiem_adjust -= 12

            # Ensure that input is not something like 13 PM
            if int(time[0]) < 1 or int(time[0]) > 12:
                raise ValueError

            # e.g. 09:00 AM
            if len(time) == 2:
                minute = int(time[1])
                if minute < 0 or minute >= 60:
                    raise ValueError
                else:
                    hour = int(time[0]) + meridiem_adjust
                    if hour >= 10:
                        hour = str(hour)
                    else:
                        hour = "0" + str(hour)

                    if minute >= 10:
                        minute = str(minute)
                    else:
                        minute = "0" + str(minute)

                return hour + ":" + minute

            # e.g. 9 AM
            else:
                hour = int(time[0]) + meridiem_adjust
                if hour >= 10:
                    return str(hour) + ":00"
                else:
                    return "0" + str(hour) + ":00"

        # End of process()


        try:
            start_time = process(start_time, start_meridiem)
            end_time = process(end_time, end_meridiem)
        except ValueError:
            raise ValueError
        else:
            return start_time + " to " + end_time

    else:
        raise ValueError


if __name__ == "__main__":
    main()