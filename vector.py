from numbers import Number
import math

class Vector(tuple):
    def __init__(self,inVec):
        length = len(inVec)
        tuple.__init__(inVec)

    ##### Public Methods #####
    def cross((sx,sy,sz),(ox,oy,oz)):
        if not len(self) == len(other) == 3:
            raise ValueError('Vectors must both be 3 dimensional')
        return Vector((sy*oz-sz*oy,sz*ox-sx*oz,sx*oy-sy*ox))

    def dot(self,other):
        if not self._verifySameLength(self,other):
            raise ValueError('Vectors must be the same length')
        return sum([s*o for s,o in zip(self,other)])

    def unit(self):
        return Vector(self / abs(self))

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
        c = float(c)
        return Vector((x/c,y/c,z/c))
    def __floordiv__((x,y,z),c):
        return Vector(map(int,map(math.floor,(x/c,y/c,z/c))))

    def __pos__(self):
        return self

    def __neg__(self):
        return Vector([-1*s for s in self])

    def __abs__(self):
        return math.sqrt(sum([s**2 for s in self]))

    def __str__(self):
        return ('({'+'},{'.join([str(i) for i in range(len(self))])+'})')\
                .format(*self)

    def __repr__(self):
        return ('Vector([{'+'},{'.join([str(i) for i in \
                range(len(self))])+'}])').format(*self)
