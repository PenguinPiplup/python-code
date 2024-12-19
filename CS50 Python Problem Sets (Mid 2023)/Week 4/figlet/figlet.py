import sys
import random
from pyfiglet import Figlet

figlet = Figlet()
avail_fonts = figlet.getFonts()

# Obtain number of command-line arguments
cla_count = len(sys.argv)

# Ensure proper usage
if cla_count != 1 and cla_count != 3:
    print("Invalid usage")
    sys.exit(1)
elif cla_count == 3:
    cla_arg1 = sys.argv[1]
    cla_arg2 = sys.argv[2]
    if cla_arg1 != "-f" and cla_arg1 != "--font":
        print("Invalid usage")
        sys.exit(1)
    if not cla_arg2 in avail_fonts:
        print("Invalid usage")
        sys.exit(1)
    font = Figlet(font=cla_arg2)
else:
    font_count = len(avail_fonts)
    result = random.randint(0, font_count - 1)
    font = Figlet(font=avail_fonts[result])

# Obtain input from user
user_input = input("Input: ")

# Print output
print(font.renderText(user_input))