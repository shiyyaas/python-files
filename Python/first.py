#calculator

print("""
      Addition: "+"
      Subtraction: "-"
      Multiplication: "*"
      Division: "/"
""")

Choice = input("Choose an operation: ")
num1 = int(input("Enter 1st number: "))
num2 = int(input("Enter 2nd number: "))

if Choice == "+":
    res = num1 + num2
elif Choice == "-":
    res = num1 - num2
elif Choice == "*":
    res = num1 * num2
elif Choice == "/":
    res = num1 / num2
else:
    print("Invalid operation selected.")

print( f"{num1} {Choice} {num2} = {res}")
