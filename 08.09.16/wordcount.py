"""Wordcount exercise
Google's Python class
 
The main() below is already defined and complete. It calls print_words()
and print_top() functions which you write.
 
1. For the --count flag, implement a print_words(filename) function that counts
how often each word appears in the text and prints:
word1 count1
word2 count2
...
 
Print the above list in order sorted by word (python will sort punctuation to
come before letters -- that's fine). Store all the words as lowercase,
so 'The' and 'the' count as the same word.
 
2. For the --topcount flag, implement a print_top(filename) which is similar
to print_words() but which prints just the top 20 most common words sorted
so the most common word is first, then the next most common, and so on.
 
Use str.split() (no arguments) to split on all whitespace.
 
Workflow: don't build the whole program at once. Get it to an intermediate
milestone and print your data structure and sys.exit(0).
When that's working, try for the next milestone.
 
Optional: define a helper function to avoid code duplication inside
print_words() and print_top().
 
"""
 
import sys
 
# Define print_words(filename) and print_top(filename) functions.
# You could write a helper utility function that reads a file
# and builds and returns a word/count dict for it.
# Then print_words() and print_top() can just call the utility function.

def get(filename):
    inf = open(filename, "r")
    s = []
    s1 = inf.readline()
    while (s1 != ''):
        s.append(s1)
        s1 = inf.readline()
    snew = []
    for s1 in s:
        lst = s1.split()
        for s2 in lst:
            snew.append(s2)
    s = snew
    for c in '.,!?-:;"\'':
        snew = []
        for s1 in s:
            lst = s1.split(c)
            for s2 in lst:
                snew.append(s2)
        s = snew
    d = dict()
    for s1 in s:
        s1 = s1.lower()
        if s1 in d:
            d[s1] += 1
        else:
            d[s1] = 1;
    s = []
    d.pop('')
    for s1 in d:
        s.append((s1,d[s1]))
    return s

def print_words(filename):
    lst = get(filename)
    lst = sorted(lst)
    for s in lst:
        print(s[0], s[1]) 

def print_top(filename):
    lst = get(filename)
    lst = sorted(lst, key = lambda x: (-x[1], x[0]))
    for i in range(min(len(lst), 20)):
        s = lst[i]
        print(s[0], s[1])

###
 
# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
    if len(sys.argv) != 3:
        print('usage: ./wordcount.py {--count | --topcount} file')
        sys.exit(1)
 
    option = sys.argv[1]
    filename = sys.argv[2]
    if option == '--count':
        print_words(filename)
    elif option == '--topcount':
        print_top(filename)
    else:
        print('unknown option: ' + option)
        sys.exit(1)
 
if __name__ == '__main__':
    main()