'''
Created on Feb 7, 2019

@author: ericpatel
'''
import sys

class node:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right
        
root = node(None, None, None)
temp = root
while(True):
    try:
        x, y = (input().split())
        if(x == 'i'):
            if(root.val == None or root.val == int(y)):
                root.val = int(y)
            else:
                while(True):
                    if(int(y) > temp.val):
                        if(temp.right == None):
                            temp.right = node(int(y), None, None)
                            break
                        else:
                            temp = temp.right
                    else:
                        if(temp.left == None):
                            temp.left = node(int(y), None, None)
                            break
                        else:
                            temp = temp.left
        elif(x == 'q'):
            steps = []
            if(root.val == int(y)):
                print("found: root")
                continue
            while(True):
                if(temp == None):
                    print("not found")
                    break 
                elif(int(y) > temp.val):
                    steps.append("r")
                    temp = temp.right
                elif(int(y) < temp.val):
                    steps.append("l")
                    temp = temp.left
                elif(temp.val == int(y)):
                    print("found: " + " ".join(steps))
                    break
        temp = root
    except:
        exit()