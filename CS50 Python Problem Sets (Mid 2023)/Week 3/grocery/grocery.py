# Create dictionary to store values
grocery_list = {}

# Obtain user input
while True:
    try:
        item = input().strip().upper()
        if item in grocery_list:
            grocery_list[item] += 1
        else:
            grocery_list[item] = 1
    except EOFError:
        print()
        break

# Sort
list = []
for grocery in grocery_list:
    list.append(grocery)
list.sort()

# Print result
for grocery in list:
    print(grocery_list[grocery], grocery)