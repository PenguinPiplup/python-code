import re
import sys


def main():
    print(parse(input("HTML: ")))


def parse(s):
    # Extract link from src=" "
    if link := re.search(r"src=\"{1}([^\"]+)\"{1}", s):
        extracted = link.group(1)

        # Check if link is a youtube link
        if link_identifier := re.search(r"^(?:https?://)?(?:www\.)?youtube\.com/embed/(.+)$", extracted):
            return "https://youtu.be/" + link_identifier.group(1)
        else:
            return None
    else:
        return None


if __name__ == "__main__":
    main()