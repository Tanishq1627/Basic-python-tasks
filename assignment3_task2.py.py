import math

num = float(input("Enter a positive number: "))

if num <= 0:
    print("Please enter a number greater than 0 for log and square root.")
else:
    square_root = math.sqrt(num)
    natural_log = math.log(num)
    sine_value = math.sin(num)  

    print(f"Square root of {num} is: {square_root}")
    print(f"Natural logarithm (ln) of {num} is: {natural_log}")
    print(f"Sine of {num} radians is: {sine_value}")