def factorial(n):
    if n < 0:
        return "Factorial is not defined for negative numbers."
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


# Main section that demonstrates the function with some examples.
if __name__ == '__main__':
    print(factorial(5))  # Example 1: Factorial of 5
    print(factorial(-3))  # Example 2: Factorial of a negative number (should return an error message)
