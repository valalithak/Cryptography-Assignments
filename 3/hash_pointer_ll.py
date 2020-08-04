import os
import sys
import time
import sympy
import random as rnd

class Node: 
    def __init__(self, data, previous_hash, curr_hash):
        self.data = data
        self.previous_hash = previous_hash
        self.curr_hash = curr_hash
        self.next = None

class LinkedList: 
    def __init__(self): 
        self.head = None
    
    def printList(self): 
        temp = self.head 
        index = 0
        while (temp): 
            print("Node #" + str(index)+":")
            index+=1
            print("Data: "+str(temp.data))
            print("Previous Hash: "+str(temp.previous_hash))
            print("Current Hash: "+str(temp.curr_hash))
            print("\n")
            temp = temp.next

q = 99991
x = sympy.randprime(1000, 9999) 
g = 2 
y = pow(g, x, q) 
c = rnd.randint(1, q - 1)
r = pow(g, c, q)

def dlpHash(r, m):
    return ((pow(g, r)%q)*(pow(y, m%q)%q))%q

def createNode(data, prevHash, r):
    temp = Node(data, prevHash, r)
    temp.curr_hash = dlpHash(r, data)^prevHash
    return temp

ll = LinkedList()
random_hash = 10039 #random constant to store as the prev hash of the head, instead of null

ll.head = createNode(1, random_hash, r)
a = createNode(2, ll.head.curr_hash, r)
ll.head.next = a 

b = createNode(3, a.curr_hash,r)
a.next = b
ll.printList()