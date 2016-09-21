# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    lst1 = []
    for i in range(len(lst)):
        if i == len(lst) - 1 or lst[i] != lst[i + 1]:
            lst1.append(lst[i])
    return lst1
        
 
# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    lst3, i, j = [], 0, 0
    while i < len(lst1) or j < len(lst2):
        if i == len(lst1) or j != len(lst2) and lst1[i] > lst2[j]:
            lst3.append(lst2[j])
            j += 1
        else:
            lst3.append(lst1[i])
            i += 1
    return lst3