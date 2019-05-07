'''
Created on Feb 7, 2019

@author: ericpatel
'''
import sys

x1, y1 = map(int, sys.stdin.readline().split())
a = []
for i in range(x1):
    a.append(list(map(float, sys.stdin.readline().split())))
    
x2, y2 = map(int, input().split())

if y1 != x2:
    print("invalid input")
    sys.exit(0)
    a
b = []
for i in range(x2):
    b.append(list(map(float, sys.stdin.readline().split())))
    
for i in range(x1):
    result = []
    for j in range(y2):
        sum = 0
        for y in range(x2):
            sum += a[i][y] * b[y][j]
        result.append(sum)
    print(" ".join(map(str , result)))     