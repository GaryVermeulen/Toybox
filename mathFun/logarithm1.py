# logarithm1.py
# 

def ln_custom(x, iterations=100):
    if x <= 0:
        return float('nan')
    y = (x - 1) / (x + 1)
    total = 0
    for i in range(iterations):
        term = (2 * (y**(2 * i + 1))) / (2 * i + 1)
        total += term
        
    return total


def log_custom(x, base=10):
    return ln_custom(x) / ln_custom(base)

if __name__ == "__main__":

    print(ln_custom(10))

    print(round(log_custom(1, 2)))
