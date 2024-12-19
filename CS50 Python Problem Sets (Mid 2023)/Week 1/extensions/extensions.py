def main():
    file_name = input("File name: ").strip().lower().replace(".", " ")
    print(convert(file_name))


def convert(file_name):
    words = file_name.split()
    length = len(words)
    if length < 2:
        return "application/octet-stream"
    else:
        final_word = words[length - 1]
        match final_word:
            case "gif" | "png":
                return ("image/" + final_word)
            case "jpg" | "jpeg":
                return ("image/" + "jpeg")
            case "pdf" | "zip":
                return ("application/" + final_word)
            case "txt":
                return "text/plain"
            case _:
                return "application/octet-stream"


main()