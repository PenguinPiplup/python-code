answer = input("Greeting: ").strip().title()
if (len(answer) == 0):
    print("$100")
elif answer[0] == "H":
    reduced = answer[:5]
    if reduced == "Hello":
        print("$0")
    else:
        print("$20")
else:
    print("$100")