answer = input("What is the Answer to the Great Question of Life, the Universe and Everything? ").strip()
if answer == "42":
    print("Yes")
elif answer.lower().replace("-", " ") == "forty two":
    print("Yes")
else:
    print("No")