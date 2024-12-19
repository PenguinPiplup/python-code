string = "AEIOUaeiou"
list = []
for char in string:
    list.append(char)

output = input("Input: ")
for char in list:
    output = output.replace(char, "")
print("Output: " + output)