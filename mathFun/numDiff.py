# numDiff.py
# Numerical differentiation with numpy
#
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return 2*x**2

def tangent_line(x, aD, b):
    return aD * x + b


if __name__ == "__main__":
    x = np.arange(0, 5, 0.001)
    y = f(x)

    plt.plot(x, y)
    colors = ['k', 'g', 'r', 'b', 'c']

    for i in range(5):
    # The points and close enough points
        p2_delta = 0.001
        x1 = i
        x2 = x1 + p2_delta

        y1 = f(x1)
        y2 = f(x2)

        print("x1 & y1, and x2 & y2: ", (x1, y1), (x2, y2))

        # Dirivative approximation and y-intercept for the tangent line
        approximate_derivative = (y2 - y1)/(x2 - x1)
        print("approximate_derivative: ", approximate_derivative)
    
        b = y2 - approximate_derivative * x2
        print("b: ", b)

        to_plot = [x1 - 0.9, x1, x1 + 0.9]
        plt.scatter(x1, y1, c=colors[i])
        plt.plot(to_plot, [tangent_line(i, approximate_derivative, b) for i in to_plot])

        print(f'Approximate derivative for f(x); where x = {x1} is {approximate_derivative}\n')
    
    plt.show()

    
