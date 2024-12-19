def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    s = s.strip().upper()
    
    # Check that there are a minimum of 2 characters and maximum of 6 characters
    if 2 <= len(s) <= 6:
        pass
    else:
        return False

    # Ensure that vanity plate starts with two letters
    if s[:2].isalpha() == False:
        return False

    # Ensure that all remaining characters (if there are any) are either letters or numbers
    if s[2:].isalnum() == False and len(s) > 2:
        return False

    # Auto-approve vanity plate if it contains all letters (remaining vanity plates must contain numbers)
    if s.isalpha() == True:
        return True

    # Check that plate does not have 0 as its first number and letters do not follow numbers

    # Find location where number first appears
    tmp = 0
    for char in s:
        if char.isnumeric():
            break
        tmp += 1

    # Check that plate does not have 0 as its first number
    if s[tmp] == "0":
        return False
    # Check that letters do not follow numbers
    elif s[tmp:].isnumeric() == False:
        return False
    else:
        return True


if __name__ == "__main__":
    main()