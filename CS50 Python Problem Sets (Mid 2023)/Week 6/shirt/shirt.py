import sys
from PIL import Image
from PIL import ImageOps

def main():
    # Sanitising user input
    arg_length = len(sys.argv)
    if arg_length < 3:
        sys.exit("Too few command-line arguments")
    elif arg_length > 3:
        sys.exit("Too many command-line arguments")
    elif not check_file(sys.argv[1]):
        sys.exit("Invalid input")
    elif not check_file(sys.argv[2]):
        sys.exit("Invalid output")
    elif check_file(sys.argv[1]) != check_file(sys.argv[2]):
        sys.exit("Input and output have different extensions")

    try:
        image = Image.open(sys.argv[1])
        shirt = Image.open("shirt.png")
        shirt = shirt.convert('RGBA')
        s_width, s_height = shirt.size
    except FileNotFoundError:
        sys.exit("Input does not exist")
    else:
        image = ImageOps.fit(image, size=(s_width, s_height), bleed=0.0, centering=(0.5, 0.5))
        image.paste(shirt, (0,0), shirt)
        image.save(sys.argv[2])


def check_file(file):
    file = file.lower()
    if file.endswith(".jpg") or file.endswith(".jpeg"):
        return 1
    elif file.endswith(".png"):
        return 2
    else:
        return 0


if __name__ == "__main__":
    main()