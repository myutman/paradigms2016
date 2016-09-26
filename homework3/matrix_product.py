import numpy as np
import math
import sys


def mult(a, b, k):
    if (k == 1):
        return a * b
    c = np.zeros((k, k), dtype=np.int)
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

def read_matrix(n, k, f=sys.stdin):
    a = np.loadtxt(f, dtype=np.int, ndmin=2)
    b = list(map(list, a[n:]))
    a = list(map(list, a[:n]))
    for i in range(n):
        a[i] += [0] * (k - n)
    for i in range(n, k):
        a.append([0] * k)
    a = np.array(a)
    for i in range(n):
        b[i] += [0] * (k - n)
    for i in range(n, k):
        b.append([0] * k)
    b = np.array(b)
    return a, b

def output(c, n):
    print()
    for i in range(n):
        for j in range(n):
            print(c[i][j], end=' ')
        print()

def test(filename):
    f = open(filename)
    n = int(f.readline())
    k = 2 ** math.ceil(math.log2(n))
    a, b = read_matrix(n, k, f)
    c = mult(a, b, k)
    c1 = np.dot(a, b)
    if c.all() == c1.all():
        print("correct")    

if __name__ == "__main__":
    n = int(input())
    k = 2 ** math.ceil(math.log2(n))
    a, b = read_matrix(n, k)
    c = mult(a, b, k)
    output(c, n)

    