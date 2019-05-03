'''
Created on Feb 7, 2019

@author: ericpatel
'''
import sys

stack = []
x = ''
while(1):
    x = sys.stdin.readline().strip()
    if(x.isdigit() == True):
        print(int(x))
        stack.append(int(x))
    elif(x == '~'):
        if(len(stack) >= 1):
            x = stack.pop()
            print(x * -1)
            stack.append(x)
    elif(len(x) == 1):
        if(len(stack) >= 2):
            b = stack.pop()
            a = stack.pop()
            if(x == '+'):
                print(a + b)
                stack.append(a+b)
            elif(x == '-'):
                print(a - b)
                stack.append(a-b)
            elif(x == '*'):
                print(a * b)
                stack.append(a*b)
            elif(x == "/"):
                if(b == 0):
                    stack.append(a)
                    stack.append(b)
                    print("error: division by zero")
                else:
                    print(float(a)/b)
                    stack.append(float(a)/b)
        else:
            print("invalid operation")
    else:
        exit()