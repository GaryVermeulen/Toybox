# exponent1.py
# Putzing around with math
#


# Rules

# Product
# x^a*x^b = x^a+b
def product(x, a, b):
    #c = x**(a + b)
    return x**(a + b)

# Quotient
# x^a/x^b = x^a-b
def quotient(x, a, b):
    #c = x**(a - b)
    return x**(a - b)

# Power of power
# (x^a)^b = x^ab
def powerOfPower(x, a, b):
    return x**(a*b)

# Power of product
def powerOfProduct(x, y, a, b):
    return x**a*y**b

# Power of one
def powerOfOne(x):
    return x**1

# Power of zero
def powerOfZero(x):
    return x**0

# Power of negative one
def powerOfNegativeOne(x):
    return 1/x

# Change sign of exponents
def changeSign(x, a):
    return 1/(x**a)

# Fractional exponents
def fractional(x, m, n):
    return x**(m/n)


if __name__ == "__main__":
    print(product(2, 2, 3))

    print(quotient(2, 3, 2))

    print(powerOfPower(2, 3, 2))

    print(powerOfProduct(2, 3, 2, 2))

    print(powerOfOne(2))
    
    print(powerOfZero(2))

    print(powerOfNegativeOne(2))

    print(changeSign(2, 3))

    print(fractional(4, 3, 2))
