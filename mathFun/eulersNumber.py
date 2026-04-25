# eulersNumber.py
#

import math
import numpy as np


def calculate_e_series(iterations=20):
    e_approx = 1.0
    factorial = 1.0
    for i in range(1, iterations):
        factorial *= i  # Update factorial: 1!, 2!, 3!...
        e_approx += 1.0 / factorial
    return e_approx

def geometric_series(a, r):
    term = a
    while True:
        yield term
        term *= r



if __name__ == "__main__":

    print("Euler's number...")
    print(f"Approximation (Series): {calculate_e_series()}")
    print("Using math: ", math.e)
    print("Using numpy: ", np.e)

    print("Infinite series...")
    gen = geometric_series(1, 0.5)
    total_sum = 0
    for _ in range(100):
        last_num = total_sum
        total_sum += next(gen)
        print(total_sum)
        
        if total_sum == last_num:
            break
    
