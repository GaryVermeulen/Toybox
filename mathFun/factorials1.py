# factorials1.py
# Different factorial approaches
#

def factorial_iterative(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    result = 1
    for i in range(1, n + 1):
        result *= i

    return result

def factorial_recursive(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    if n == 0 or n ==1:
        return 1

    return n * factorial_recursive(n - 1)

def factorial_one_liner(n):
    factorial_oneline = lambda n: 1 if n <= 1 else n * factorial_oneline(n - 1)

    return factorial_oneline(n)

if __name__ == "__main__":

    n = 5

    print("For n = ", n)

    print("factorial_iterative: ", factorial_iterative(n))
    print("factorial_recursive: ", factorial_recursive(n))

    factorial_oneline = lambda n: 1 if n <= 1 else n * factorial_oneline(n - 1)
    print("factorial_oneliner: ", factorial_oneline(n))

    print("factorial_one_liner: ", factorial_one_liner(n))

    
    
