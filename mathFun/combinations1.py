# combinations1.py
# Combinations in pure python
#

def get_combinations(iterable, r):
    # This algorithm selects groups of size \(r\) from an iterable
    # where order does not matter and repetition is not allowed.
    
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
    if not arr:
        yield []
    else:
        for rest in get_all_combinations(arr[1:]):
            yield rest            # Exclude the first element
            yield [arr[0]] + rest # Include the first element
        



if __name__ == "__main__":

    items = ["a", "b", "c"]
    #items = ['A', 'B', 'C']

    print("get_combinations for items: ", items)
    for combo in get_combinations(items, 2):
        print(combo)

    
    
    print("get_all_combinations for items: ", items)
    for combo in get_all_combinations(items):
        print(combo)
