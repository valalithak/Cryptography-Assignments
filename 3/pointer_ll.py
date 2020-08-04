import os
import sys
import time

class Node: 
    def __init__(self, data): 
        self.data = data 
        self.next = None 
   
class LinkedList: 
    def __init__(self): 
        self.head = None
    
    def printList(self): 
        temp = self.head 
        index = 0
        while (temp):
            print("Node #:"+str(index)) 
            print("Data: "+str(temp.data))
            temp = temp.next

ll = LinkedList() 
ll.head = Node(1) 
x = Node(2) 
y = Node(3) 
ll.head.next = x 
x.next = y
ll.printList()