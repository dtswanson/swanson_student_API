
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

operation = input("Enter operation (add/subtract/multiply/divide): ").strip().lower()
number1 = float(input("Enter first number: "))
number2 = float(input("Enter second number: "))

if operation == "add":
    result = add(number1, number2)
    print(f"The result of adding {number1} and {number2} is {result}")
elif operation == "subtract":
    result = subtract(number1, number2)
    print(f"The result of subtracting {number1} from {number2} is {result}")
elif operation == "multiply":
    result = multiply(number1, number2)
    print(f"The result of multiplying {number1} and {number2} is {result}")
elif operation == "divide":
    result = divide(number1, number2)
    print(f"The result of dividing {number1} by {number2} is {result}")
else:
    print("Invalid operation")