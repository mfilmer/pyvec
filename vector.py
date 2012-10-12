#from __future__ import division
from numbers import Number
import math

i = Vector([1,0,0])
j = Vector([0,1,0])
k = Vector([0,0,1])

class Vector(tuple):
    def __init__(self,inVec):
        length = len(inVec)
        tuple.__init__(inVec)

    ##### Public Methods #####
    def cross(self,other):
        if not len(self) <= 3 and len(other) <= 3:
            raise ValueError('Vectors must both be 3 dimensional')
        sx,sy,sz = self.extend(3)
        ox,oy,oz = other.extend(3)
        return Vector((sy*oz-sz*oy,sz*ox-sx*oz,sx*oy-sy*ox))

    #todo: make sure this is right (because it isn't)
    #magnitude of the cross product
    def area(self,other):
        if not len(self) <= 3 and len(other) <= 3:
            raise ValueError('Vectors must both be 3 dimensional')
        return abs(self) * abs(other) * math.sin(self.angle(other))

    #todo: if the vectors aren't the same length, add 0's to the end of
    #the shorter one to make them the same length
    def dot(self,other):
        ls = len(self)
        lo = len(other)
        if not ls == lo:
            #raise ValueError('Vectors must be the same length')
            self = Vector(self.extend(lo))
            other = Vector(other.extend(ls))
        return sum([s*o for s,o in zip(self,other)])

    def unit(self):
        return Vector(self / abs(self))

    def angle(self,other=None):
        if other is None:
            other = Vector([1])
        return math.acos(self.dot(other) / (abs(self)*abs(other)))

    #find the projection of this vector on another
    #a.projection(b) is the projection of a onto b
    def projection(self,other):
        # Version 1 (probably slow-ish)
        #return abs(self) * self.angle(other) * other.unit()
        # Version 2 (probably faster than version 1)
        #bHat = other.unit()
        #return self.dot(bHat) * bHat
        # Version 3 (hopefully the fastest)
        return self.dot(other) / other.dot(other) * other

    def extend(self,length):
        self = list(self)
        self.extend([0]*(length-len(self)))
        return Vector(self)

    ##### Convienence Properties #####
    # Component Vectors
    @property
    def x(self):
        return self[0]
    @property
    def y(self):
        return self[1]
    @property
    def z(self):
        return self[2]

    # Components of the unit vector
    @property
    def i(self):
        return self.unit()[0]
    @property
    def j(self):
        return self.unit()[1]
    @property
    def k(self):
        return self.unit()[2]

    ##### Utility Methods #####
    def _intMul(self,c):
        return Vector([s*c for s in self])

    @staticmethod
    def _verifySameLength(vec1,vec2):
        return len(vec1) == len(vec2)

    ##### Magic Methods #####
    def __add_(self,other):
        if not self._verifySameLength(self,other):
            raise ValueError('Vectors must be the same length')
        return Vector([s+o for s,o in zip(self,other)])
    def __radd__(self,other):
        if not self._verifySameLength(self,other):
            raise ValueError('Vectors must be the same length')
        return Vector([s+o for s,o in zip(self,other)])

    def __sub__(self,other):
        if not self._verifySameLength(self,other):
            raise ValueError('Vectors must be the same length')
        return Vector([s-o for s,o in zip(self,other)])
    def __rsub__(self,other):
        if not self._verifySameLength(self,other):
            raise ValueError('Vectors must be the same length')
        return Vector([o-s for s,o in zip(self,other)])

    def __mul__(self,other):
        if isinstance(other,Number):
            return self._intMul(other)
        return self.dot(other)
    def __rmul__(self,other):
        if isinstance(other,Number):
            return self._intMul(other)
        return self.dot(other)

    def __div__((x,y,z),c):
        return Vector((x/c,y/c,z/c))
    def __truediv__((x,y,z),c):
        return Vector((x/c,y/c,z/c))
    def __floordiv__((x,y,z),c):
        return Vector(map(int,(x//c,y//c,z//c)))

    def __pos__(self):
        return self

    def __neg__(self):
        return Vector([-1*s for s in self])

    def __abs__(self):
        return math.sqrt(sum([s**2 for s in self]))

    def __getitem__(self,key):
        if isinstance(key,int) or isinstance(key,slice):
            return Vector(super(Vector,self).__getitem__(key))
            #return Vector(self[key])
        elif key in ['i','j','k']:
            if key == 'i': return Vector(super(Vector,self).__getitem__(0))
            elif key == 'j': return Vector(super(Vector,self).__getitem__(1))
            else: return Vector(super(Vector,self).__getitem__(2))
        else:
            raise KeyError

    def __str__(self):
        return ('<{'+'},{'.join([str(i) for i in range(len(self))])+'}>')\
                .format(*self)

    def __repr__(self):
        return ('Vector([{'+'},{'.join([str(i) for i in \
                range(len(self))])+'}])').format(*self)

    def __nonzero__(self):
        return any(self)

    ##### Comparison Methods #####
    # For equality compare the actual vectors
    #def __eq__(self,other):
        #return self == other
    #def __ne__(self,other):
        #return self != other

    # Compare the magnitude
    def __lt__(self,other):
        return abs(self) < abs(other)
    def __le__(self,other):
        return abs(self) <= abs(other)

    def __gt__(self,other):
        return abs(self) > abs(other)
    def __ge__(self,other):
        return abs(self) >= abs(other)
