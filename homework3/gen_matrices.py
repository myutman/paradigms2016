import random

n, m = map(int, input().split())

print(n)
for i in range(n):
    for j in range(n):
        print(random.randint(0, m), end = " ")
    print()
for i in range(n):
    for j in range(n):
        print(random.randint(0, m), end = " ")
    print()