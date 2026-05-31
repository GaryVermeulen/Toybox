# gMatLib1.py
# Collection of pure Python math functions
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

def pure_permutations(iterable):
    """
    Low memory overhead and mimics itertools.permutations
    
    Usage:
    
    string_input = "ABC"
    print(f"Permutations of {string_input}:")
    for p in pure_permutations(string_input):
        print("".join(p))
    """
    
    # Convert input to a list to support indexing and slicing
    items = list(iterable)
    length = len(items)
    
    # Base case: an empty list or single element has 1 permutation
    if length <= 1:
        yield tuple(items)
    else:
        # Loop through every element to set it as the first item
        for i in range(length):
            current_element = items[i]
            # Form a sub-list by excluding the current element
            remaining_elements = items[:i] + items[i+1:]
            
            # Recursively find permutations of the remaining sub-list
            for sub_permutation in pure_permutations(remaining_elements):
                yield (current_element,) + sub_permutation

def list_permutations(items):
    """
    Classic List-Based Backtracking Approach

    Usage:
    list_input = [1, 2, 3]
    list_input = ["a", "b", "c"]
    print(f"\nPermutations of {list_input}:")
    print(list_permutations(list_input))
    """
    # Base case
    if len(items) <= 1:
        return [items]
        
    result = []
    for i, current in enumerate(items):
        # Isolate the remaining elements
        remaining = items[:i] + items[i+1:]
        
        # Merge the current element with all sub-permutations
        for p in list_permutations(remaining):
            result.append([current] + p)
            
    return result

def get_combinations(iterable, r):
    """
    This algorithm selects groups of size r from an iterable
    where order does not matter and repetition is not allowed.

    Usage:
    items = ["a", "b", "c"]
    for combo in get_combinations(items, 2):
        print(combo)
    
    """
    
    pool = tuple(iterable)
    n = len(pool)
    
    if r > n or r < 0:
        return

    indices = list(range(r))
    yield tuple(pool[i] for i in indices)

    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
            
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        
        yield tuple(pool[i] for i in indices)

def get_all_combinations(arr):
    """
    Usage:
    items = ['A', 'B', 'C']
    for combo in get_all_combinations(items):
        print(combo)
    """
    if not arr:
        yield []
    else:
        for rest in get_all_combinations(arr[1:]):
            yield rest            # Exclude the first element
            yield [arr[0]] + rest # Include the first element
        

