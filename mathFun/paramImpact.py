# paramImpact.py
#
import matplotlib.pyplot as plt
import numpy as np

def f(x):
    #return 2*x # Linear
    return 2*x**2 # Nonlinear

if __name__ == "__main__":
    x = np.array(range(5))
    y = f(x)

    print(x)
    print(y)

    for i in range(5):
        if i < 5-1:
            slope = (y[i+1] - y[i]) / (x[i+1] - x[i])
            print("Slope: ", slope)

    plt.plot(x, y)
    plt.show()

    p2_delta = 0.0001

    x1 = 1
    x2 = x1 + p2_delta

    y1 = f(x1)
    y2 = f(x2)

    approximate_derivative = (y2 - y1) / (x2 - x1)
    print("approximate derivative: ", approximate_derivative)
