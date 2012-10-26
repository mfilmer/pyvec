# vector\vector.py

#from __future__ import division
from itertools import izip_longest
from numbers import Number
import math

class Vector(tuple):
    def __new__(self,inVec,is3D=False):
        print 'making a new',
        if is3D:
            print '3D vector'
            return Vector3D(inVec)
        print 'boring vector'
        return tuple.__new__(self,inVec)
    #def __init__(self,inVec):
        #tuple.__init__(inVec)

    ##### Public Methods #####
    def cross(self,other):
        Vector._minDim(3,self,other)
        sx,sy,sz = self.extend(3)
        ox,oy,oz = other.extend(3)
        return Vector((sy*oz-sz*oy,sz*ox-sx*oz,sx*oy-sy*ox))

    #todo: make sure this is right (because it probably isn't)
    #magnitude of the cross product
    def area(self,other):
        """Calculate the magnitude of the cross product"""
        Vector._minDim(3,self,other)
        return abs(self) * abs(other) * abs(math.sin(self.angle(other)))

    def dot(self,other):
        #todo: consider:
        #sum(itertools.imap(operator.mul,self,other))
        ls = len(self)
        lo = len(other)
        return sum([s*o for s,o in izip_longest(self,other,0)])

    def unit(self):
        return Vector(self / abs(self))

    def angle(self,other=None):
        if other is None:
            other = Vector([1])
        return math.acos(self.dot(other) / (abs(self)*abs(other)))

    #find the projection of this vector on another
    #a.projection(b) is the projection of a onto b
    def projection(self,other):
        return self.dot(other) / other.dot(other) * other

    def dim(self):
        """Get the highest dimension of the vector"""
        return self[0:-1].dim() if self[-1] == 0 else len(self)

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

    def _minDim(dim,*vecs):
        for vec in vecs:
            if len(vec) > dim:
                raise ValueError('Vectors must both be {0} dimensional'.format(dim))

    ##### Magic Methods #####
    def __add_(self,other):
        return Vector([s+o for s,o in izip_longest(self,other,0)])
    def __radd__(self,other):
        return Vector([s+o for s,o in izip_longest(self,other,0)])

    def __sub__(self,other):
        return Vector([s-o for s,o in izip_longest(self,other,0)])
    def __rsub__(self,other):
        return Vector([o-s for s,o in izip_longest(self,other,0)])

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

    def __getslice__(self,i,j):
        return Vector(super(Vector, self).__getitem__(slice(i,j,1)))

    def __getitem__(self,key):
        if isinstance(key,int):
            try:
                return super(Vector, self).__getitem__(key)
            except IndexError:
                raise IndexError('index out of range')
        elif isinstance(key,slice):
            return Vector(super(Vector, self).__getitem__(key))
        elif key in ['i','j','k']:
            if key == 'i': return self.__getitem__(0)
            elif key == 'j': return self.__getitem__(1)
            else: return self.__getitem__(2)
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
    def isEqual(self,other):
        """Determine if two vectors are equal (magnitude and direction)"""
        return tuple(self) == tuple(other)

    # Compare the magnitude
    def __eq__(self,other):
        return abs(self) == abs(other)
    def __ne__(self,other):
        return abs(self) != abs(other)

    def __lt__(self,other):
        return abs(self) < abs(other)
    def __le__(self,other):
        return abs(self) <= abs(other)

    def __gt__(self,other):
        return abs(self) > abs(other)
    def __ge__(self,other):
        return abs(self) >= abs(other)

class Vector3D(Vector):
    """Vector class optimized for 3D vectors"""
    def __init__(self,inVec):
        self = self.extend(3)
    def __str__(self):
        return '5'

class _Const(object):
    def __init__(self):
        self.__i = Vector([1,0,0])
        self.__j = Vector([0,1,0])
        self.__k = Vector([0,0,1])
        self.__null = Vector([0])

    @property
    def i(self):
        return self.__i
    @property
    def j(self):
        return self.__j
    @property
    def k(self):
        return self.__k
    @property
    def null(self):
        return self.__null

const = _Const()
