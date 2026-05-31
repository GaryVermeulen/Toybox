# probStats1.py

from gMatLib1 import factorial_iterative as factorial
from gMatLib1 import get_combinations as combos
from gMatLib1 import list_permutations as p

if __name__ == "__main__":

    print("Ex_9.i ")

    print(factorial(4) / (factorial(2) * factorial(2)))

    for combo in combos([1,2,3,4], 2):
        print(combo)


    print("Ex_9.ii ")

    print(factorial(4) / factorial(2))

    print(p([1,2,3,4]))


    print("Ex_9.iii ")

    print(factorial(10) / (factorial(3) * factorial(7)))

    for combo in combos([1,2,3,4,5,6,7,8,9,10], 3):
        print(combo)

    print("Ex_9.ii MAX")

    print(factorial(9) / factorial(2))

    maxP = p([1,2,3,4,5,6,7,8,9])

    print(maxP)
    print(len(maxP))
