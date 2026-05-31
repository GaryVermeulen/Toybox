# permutations1.py
# Permutations
#

def pure_permutations(iterable):
    # Low memory overhead and mimics itertools.permutations
    
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
    # Classic List-Based Backtracking Approach
    
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

if __name__ == "__main__":

    # Testing the Generator Approach
    string_input = "ABC"
    print(f"Permutations of {string_input}:")
    for p in pure_permutations(string_input):
        print("".join(p))

    # Testing the List-Based Approach
    #list_input = [1, 2, 3]
    list_input = ["a", "b", "c"]
    print(f"\nPermutations of {list_input}:")
    print(list_permutations(list_input))
