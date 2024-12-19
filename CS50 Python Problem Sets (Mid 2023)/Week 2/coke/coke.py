due = 50
while True:
    print(f"Amount Due: {due}")
    insert = int(input("Insert Coin: "))
    if insert in [5, 10, 25]:
        due -= insert

    if due <= 0:
        break

print(f"Change Owed: {0 - due}")