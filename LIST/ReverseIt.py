
# Reversing Linked List!
class Node:

    def __init__(self, value):
        self.value = value
        # ATTN:  to RESERVED syntax hilite!
        self.nextPtr = None

class List:

    # ATTN:  RESERVED hiliting for DOUBLE __!
    # ATTN:  front and end point to FIRST node-value!
    # ATTN:  self reference in signature and member assignment!
    def __init__(self):
        self.front = None
        self.end = None


    # ATTN:  case of EMPTY list, then update BOTH state ptrs to be consistent!
    def append(self, value):

        if (self.front is None):
            self.front = Node(value)
            self.end = self.front

        else:
            newItem = Node(value)
            self.end.nextPtr = newItem
            self.end = newItem

    def find(self, value):

        foundPtr = None

        scanPtr = self.front
        while (scanPtr is not None):
            if (scanPtr == value):
                foundPtr = scanPtr

        return foundPtr


    def remove(self):
        pass

    def display(self):

        print '\nLIST CONTENTS:  '

        curr = self.front
        while (curr is not None):
            print curr.value
            # ATTN: iterate ptr or INFINITE LOOP -- DOH!
            curr = curr.nextPtr

        print '\n'


    def reverse(self):

        # ATTN:  3 ptrs,
        #        - PRE-INIT lookback, curr; OUTSIDE LOOP
        #        - DRIVE LOOP via CURRENT
        #        - @ BOTTOM LOOP: UPDATE lookbak, curr Ptrs!
        #        - @ TOP LOOP:  UPDATE lookfwd!
        lookbak = None
        curr = self.front

        # ATTN: UPDATE LATEST STATE REF POINTERS!
        self.front = self.end
        self.end = self.front

        # ATTN:  while
        while (curr is not None):

            lookfwd = curr.nextPtr

            # ATTN:  KEY operation here
            curr.nextPtr = lookbak

            # ATTN:  UPDATE ITERATOR SCAN PTRS!
            lookbak = curr
            curr = lookfwd





# DRIVER

print 'CASE0:  EMPTY LIST'
list1 = List()
list1.display()      # ATTN: UPDATE LATEST STATE REF POINTERS!

print 'CASE1:  ONE-ITEM LIST'
list1.append(1)
list1.display()

print 'CASE2:  THREE-ITEM LIST'
list1.append(2)
list1.append(3)
list1.display()

print 'CASE3:  REVERSE LIST'
list1.reverse()      # ATTN: UPDATE LATEST STATE REF POINTERS!
list1.display()

print 'CASE0:  REVERSE EMPTY LIST'
list2 = List()
list2.reverse()
list2.display()

print 'CASE 4:  REVERSE one-element List!'
list3 = List()
list3.append(5)
list3.reverse()
list3.display()

# TODO:  test REMOVE and FIND!
