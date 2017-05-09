
# ATTN:
# 1) SLICE [:] is a SHALLOW-COPY of List CONTAINER vs DEEP-COPY!
#    - see Stack Overflow:  Python how-to-clone-or-copy-a-list (including CONTENTs)
# 2) Python acts like:
#    - call by REFERENCE when MUTABLE argument passed in (CALLER var contents CHANGED on function return)
#    - call by VALUE when IMMUTABLE type passed in (CALLER var contents UNCHANGED on function return)
#    - see Jeff Knupp:  is-python-callbyvalue-or-callbyreference-neither
# 3) Python INHERITANCE
#    - learn python the hard way EX40:  Modules, Classes, Objects
#      (MODULE is just the xxx.py file, and can do import XXX)
#    - https://learnpythonthehardway.org/book/ex44.html on Inheritance vs Composition
#    - http://stackoverflow.com/questions/4015417/python-class-inherits-object#
#    - Python3_multiple_inheritance from Python-course.edu
#    - StackOverflow, Oop-chain-calling-parent ctor in Python
#    - StackOverflow, difference between abstract-class-and-interface in Python
#    - StackOverflow, inheritance vs composition
#      NOTE: duck-typing removes need for Interfaces
#    - getting the classname of an instance in Python
#    *** CAN CALL super(A,self).function to RESOLVE base class on DIAMOND-inheritance ambiguity problem!

"""
    ATTN:
    * Java supports SINGLE-interface model -- allows MULTIPLE interface inheritance for COMPOSITION IMPLEMENTATION; or members of class supporting interface
    * Python supports MULTIPLE-interface model -- allows only classes or abstract base classes; NOT interfaces
                                                  CAN have EITHER PURE abstract ABC meta classes simulating interfaces; OR partial-implementation abstract!

"""

from copy import deepcopy
from abc import ABCMeta, abstractmethod

# ATTN:  New-Style Python inputs OBJECT
class IStudent(object):

    # TODO:  verify if this is Pythonic for simulating Java Abstract Interface!
    __metaclass__ = ABCMeta

    @abstractmethod
    def calculateAverage(self):
        raise NotImplementedError('this is a PURE abstract base class; and Users must override calculate method with an implementation!')
        pass

# ATTN: this is a DISJOINT VERTICAL-SLICE implementation including interface VS ABOVE which has implementation only!
class PartierMixin(object):

    def __init__(self):

       print "ctor of PartierMixin called"
       print "IMPLEMENTATION separate from pure abstract interface."

    def traceInheritance(self):
       print "Got HERE to class:  " + type(self).__name__

    def chat(self):
       print "PARTYING!"

class StudierMixin(object):

    def __init__(self):

       print "ctor of StudierMixin called"
       print "IMPLEMENTATION separate from pure abstract interface."

    def traceInheritance(self):
       print "Got HERE to class:  " + type(self).__name__

    def chat(self):
       print "STUDYING!"


# NOTE:  this is just MAIN class
class Person(object):

    # ATTN:  DEEP COPY vs REFERENCE-to-SAME!  Need to EXPLICITLY Call ctor to construct!
    def __init__(self, id, first, last):

        print "ctor of Person called"
        self.id = int(id)
        self.firstName = str(first)
        self.lastName = str(last)


    def traceInheritance(self):
       print "Got HERE to class:  " + type(self).__name__


# ATTN:  MULTIPLE INTERFACE WITH IMPLEMENTATION MIXIN INHERITANCE!!!
# see Stack Overflow difference-between-abstract-class-and-interface-in-python
class Student(Person, IStudent, PartierMixin, StudierMixin):
# class Student(Person, IStudent, StudierMixin, PartierMixin):

    def __init__(self, id, first, last, scores):

        print "ctor of Student called"
        super(Student, self).__init__(id, first, last)
        # note:  following is needed to copy INTERNAL data in addition to above!
        self.scores = deepcopy(scores)

    def calculateAverage(self):

        total = sum(self.scores)
        count = len(scores)
        # ATTN: multiply by 1.0 to get DECIMAL!
        avg = 1.0 * total/count

        return avg

    def __repr__(self):

        return "STUDENT Info:\n{0}\n{1}\nAVG:  {2}".format(self.firstName, self.lastName, self.calculateAverage())

    def traceInheritance(self):

       print "Got HERE to class:  " + type(self).__name__
       # ATTN:  needs classname prior to refernece!
       # super(Student).traceInheritance(self)


# ********** TEST SCRIPT **********

scores = [90, 70]
me = Student(777, 'Dagny', 'Tag', scores)

# invokes SUB class calculation based on SUPER class data
avg = me.calculateAverage()

# invokes __repr__
print me

# tests return avg
print

# ctor hits from SUB to SUPER, supporting SUPER pure abstract class
me.traceInheritance()

# call to DISJOINT vertical-slice MIXIN
# ATTN:  ORDER overriding precedence from Class LEFT to RIGHT!
me.chat()
