import numpy as np


def mult(a, b, k):
    if (k == 1):
        return a * b
    c = np.array([[0] * k for i in range(k)])
    k //= 2
    a11 = a[:k, :k]
    a12 = a[:k, k:]
    a21 = a[k:, :k]
    a22 = a[k:, k:]
    b11 = b[:k, :k]
    b12 = b[:k, k:]
    b21 = b[k:, :k]
    b22 = b[k:, k:]    
    p1 = mult(a11 + a22, b11 + b22, k)
    p2 = mult(a21 + a22, b11, k)
    p3 = mult(a11, b12 - b22, k)
    p4 = mult(a22, b21 - b11, k)
    p5 = mult(a11 + a12, b22, k)
    p6 = mult(a21 - a11, b11 + b12, k)
    p7 = mult(a12 - a22, b21 + b22, k)
    c[:k, :k] = p1 + p4 - p5 + p7
    c[:k, k:] = p3 + p5
    c[k:, :k] = p2 + p4
    c[k:, k:] = p1 - p2 + p3 + p6
    return c

n = int(input())
k = 1
while k < n:
    k += k

ls = []
for i in range(n):
    ls1 = list(map(int, input().split()))
    while (len(ls1) < k):
        ls1.append(0)
    ls += ls1
for i in range(n, k):
    for j in range(k):
        ls.append(0)
a = np.array(ls)  
a = a.reshape((k, k))

ls = []
for i in range(n):
    ls1 = list(map(int, input().split()))
    while (len(ls1) < k):
        ls1.append(0)
    ls += ls1
for i in range(n, k):
    for j in range(k):
        ls.append(0)
b = np.array(ls)
b = b.reshape(k, k)

c = mult(a, b, k)
print()
for i in range(n):
    for j in range(n):
        print(c[i][j], end=' ')
    print()

c1 = np.dot(a, b)
print()
"""for i in range(n):
    for j in range(n):
        print(c1[i][j], end=' ')
    print()"""
print()
if (c.all() == c1.all()):
    print("Correct")
    