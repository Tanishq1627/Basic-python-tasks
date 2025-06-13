def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

sample_number = 5
result = factorial(sample_number)

print(f"The factorial of {sample_number} is {result}")