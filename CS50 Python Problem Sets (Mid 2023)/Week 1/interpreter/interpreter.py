problem = input("Expression: ").strip().split()

match problem[1]:
    case "+":
        ans = int(problem[0]) + int(problem[2])
    case "-":
        ans = int(problem[0]) - int(problem[2])
    case "*":
        ans = int(problem[0]) * int(problem[2])
    case "/":
        ans = int(problem[0]) / int(problem[2])

print(f"{ans:.1f}")
