
import logging

# Reversing Linked List!
class Node:

    def __init__(self, value):
        self.value = value
        # ATTN:  to RESERVED syntax hilite!
        self.nextPtr = None

    def __repr__(self):
        if (self is not None):
            status = "Value and Next Ptr:  {0}, {1}".format(self.value, self.nextPtr)
        else:
            status = "None"
        return status

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
            if (scanPtr.value == value):
                foundPtr = scanPtr
                break
            scanPtr = scanPtr.nextPtr

        if (foundPtr is not None):
            return foundPtr.value
        else:
            return None


    # ATTN:  lookbak needs tracking!
    def remove(self, item):

        lookbak = None
        scanPtr = self.front
        foundPtr = None

        while (scanPtr is not None):
            if (scanPtr.value == item):
                foundPtr = scanPtr
                break
            #ATTN:  track lookbak ptr!
            lookbak = scanPtr
            scanPtr = scanPtr.nextPtr

        # print "FOUND and BAK:  {0}:{1}", foundPtr, lookbak

        # CASE 1:  NOT FOUND
        if (scanPtr is None) and (foundPtr is None):
            foundPtr = None

        # CASE 2:  FOUND, first item of list
        elif (lookbak is None) and (foundPtr == self.front):
            # ATTN:  unlink the FRONT
            self.front = foundPtr.nextPtr
            foundPtr.nextPtr = None

        # CASE 3, 4: FOUND, middle item of list; or last item of list
        elif (lookbak is not None):
            # ATTN:  UNLINK foundPtr via lookback to found.next connection!
            lookbak.nextPtr = foundPtr.nextPtr
            foundPtr.nextPtr = None
            # ATTN:  update END
            if (foundPtr == self.end):
                self.end = lookbak

        return foundPtr

    def display(self):

        print '\nLIST CONTENTS:  '

        curr = self.front
        # ATTN:  end at None!
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
list0 = List()
list0.display()      # ATTN: UPDATE LATEST STATE REF POINTERS!

print 'CASE1:  ONE-ITEM LIST'
list1 = List()
list1.append(1)
list1.display()

print 'CASE2:  THREE-ITEM LIST'
list1.append(2)
list1.append(3)
list1.display()

print 'CASE3:  REVERSE LIST'
list1.reverse()      # ATTN: UPDATE LATEST STATE REF POINTERS!
list1.display()

print 'CASE4:  REVERSE EMPTY LIST'
list0.reverse()
list0.display()

print 'CASE 5:  REVERSE one-element List!'
list3 = List()
list3.append(5)
list3.reverse()
list3.display()

print 'CASE6:  FIND in Empty, 1-element, 3-element List'

found51 = list0.find(5)
# None
print found51

found52 = list3.find(5)
# 5
print found52

found53 = list3.find(4)
# None
print found53

found54 = list1.find(2)
# 2
print found54

print '\nCASE7:  REMOVE from Empty, 1-element, 3-element list MID, 3-element List END'

try:

    print "\n7.1\n"
    # list0.display()
    del71 = list0.remove(5)
    # None
    print del71

    print "\n7.2\n"
    del72 = list3.remove(5)
    #5
    print del72

    print "\n7.3\n"
    del73 = list1.remove(2)
    # 2
    print del73

    print "\n7.4\n"
    del74 = list1.remove(3)
    # 3
    print del74

    print "\n7.5\n"
    del75 = list1.remove(1)
    # 1
    print del75

except Exception as ex:

    # logging.info('YIKES!', exc_info=True)
    logging.exception("YIKES!")

finally:

    'GRACEFUL EXIT?!'


