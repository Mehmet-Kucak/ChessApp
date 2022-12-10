import math
import MathX

def min(a:float, b:float):
    if a < b:
        return a
    else:
        return b
def max(a:float, b:float):
    if a > b:
        return a
    else:
        return b
def clamp(value:float, min:float, max:float):
    if value < min:
        return min
    if value > max:
        return max
    return value
def isEven(number):
    a = float(number) / 2

    if a == math.ceil(a):
        return True
    else:
        return False
def isOdd(number):
    a = float(number) / 2

    if a == math.ceil(a):
        return False
    else:
        return True

class Vector2(object):
    #Static Properties
    @staticmethod
    def up():
        return Vector2(0.0, 1.0)
    @staticmethod
    def down():
        return Vector2(0.0, -1.0)
    @staticmethod
    def left():
        return Vector2(0.0, 0.0)
    @staticmethod
    def right():
        return Vector2(0.0, 0.0)

    @staticmethod
    def one():
        return Vector2(1.0, 1.0)
    @staticmethod
    def zero():
        return Vector2(0.0, 0.0)
    @staticmethod
    def negativeOne():
        return Vector2(-1.0, -1.0)

    @staticmethod
    def positiveInfinity():
        return Vector2(math.inf,math.inf)
    @staticmethod
    def negativeInfinity():
        return Vector2(-math.inf,-math.inf)
    ##################


    #Properties
    x = 0.0
    y = 0.0
    def normalized(self):
        normalized=Vector2(0,0)
        length=(math.sqrt((self.x*self.x)+(self.y*self.y)))
        normalized.x=self.x/length
        normalized.y=self.y/length

        return normalized
    def magnitude(self):
        return Vector2(self.x*self.x,self.y*self.y)
    def sqrtmagnitude(self):
        return Vector2(math.sqrt(self.x * self.x), math.sqrt(self.y * self.y))
    def length(self):
        length=0.0

        length=math.sqrt(self.x**2+self.y**2)

        return length
    ###########


    #Constructors
    def __init__(self, x:float, y:float):
        self.x=x
        self.y=y
    #############


    #Methodts
    def Equals(self, _value):
        if self.x == Vector2.x and self.y == Vector2.y:
            return True
        return False
    def Normalize(self):
        normalized = Vector2(0, 0)
        length = (math.sqrt((self.x * self.x) + (self.y * self.y)))
        normalized.x = self.x / length
        normalized.y = self.y / length

        return normalized
    def ToString(self,Separator=","):
        return str(self.x)+Separator+str(self.y)
    #########


    #Static Methods
    @staticmethod
    def Angle(_from, _to):
        angle=0.0

        angle=(((_from.x*_from.y)+(_to.x*_to.y))/(math.sqrt(_from.x*_from.x,_from.y*_from.y)*math.sqrt(_to.x*_to.x,_to.y*_to.y)))

        return angle
    @staticmethod
    def ClampMagnitude(_vector2, _maxLength):
        magnitude=0.0

        length=math.sqrt(_vector2.x**2,_vector2.y**2)
        f=MathX.min(length,_maxLength)
        magnitude=MathX.Vector2(f*_vector2.x,f*_vector2.y)

        return magnitude
    @staticmethod
    def Distance(a, b):
        distance=0.0

        distance=math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)

        return distance
    @staticmethod
    def Dot(a, b):
        dot=0.0

        dot= a.x * b.x + a.y * b.y

        return dot
    @staticmethod
    def Lerp(a, b, t:float):
        lerp=Vector2.zero()

        lerp=Vector2((a.x+(abs(a.x-b.x)*clamp(t))),(a.y+(abs(a.y-b.y)*clamp(t))))

        return lerp
    @staticmethod
    def LerpUnclamped(a, b, t:float):
        lerp=Vector2.zero()

        lerp=Vector2((a.x+(abs(a.x-b.x)*t)),(a.y+(abs(a.y-b.y)*t)))

        return lerp
    @staticmethod
    def Max(a, b):
        return Vector2(max(a.x,b.x),max(a.y,b.y))
    @staticmethod
    def Min(a, b):
        return Vector2(min(a.x,b.x),min(a.y,b.y))
    @staticmethod
    def MoveTowards(current, target, maxDistanceDelta:float):
        a = target - current
        magnitude = a.magnitude()

        if magnitude <= maxDistanceDelta or magnitude == 0:
            return target

        return current + a / magnitude * maxDistanceDelta
    ###############


    #Operators
    def __repr__(self):
        return "MathX.Vector2({},{})".format(self.x, self.y)
    def __str__(self, separator=","):
        return "({}{}{})".format(self.x, separator, self.y)

    def __add__(self, other):
        if isinstance(other, Vector2):
            return MathX.Vector2(self.x+other.x, self.y+other.y)
        return NotImplemented
    def __iadd__(self, other):
        if isinstance(other, Vector2):
            return MathX.Vector2(self.x+other.x, self.y+other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return MathX.Vector2(self.x-other.x, self.y-other.y)
        return NotImplemented
    def __isub__(self, other):
        if isinstance(other, Vector2):
            return MathX.Vector2(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return MathX.Vector2(self.x*other.x, self.y*other.y)
        return NotImplemented
    def __imul__(self, other):
        if isinstance(other, Vector2):
            return MathX.Vector2(self.x*other.x, self.y*other.y)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            return MathX.Vector2(self.x/other.x, self.y/other.y)
        return NotImplemented
    def __idiv__(self, other):
        if isinstance(other, Vector2):
            return MathX.Vector2(self.x/other.x, self.y/other.y)
        return NotImplemented
    def __floordiv__(self, other):
        if isinstance(other, Vector2):
            return MathX.Vector2(self.x//other.x, self.y//other.y)
        return NotImplemented

    def __len__(self):
        return MathX.Vector2.length(self)
    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        else:
            print("Index({}) is outside of bounds!".format(item))
    def __setitem__(self, key, value):
        if key == 0:
            return MathX.Vector2(value,self.y)
        elif key == 1:
            return MathX.Vector2(self.x, value)
        else:
            print("Index({}) is outside of bounds!".format(key))

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False
    def __ne__(self, other):
        if self.x != other.x or self.y != other.y:
            return True
        else:
            return False
    def __lt__(self, other):
        if self.length() < other.length:
            return True
        else:
            return False
    def __le__(self, other):
        if self.length() <= other.length:
            return True
        else:
            return False
    def __gt__(self, other):
        if self.length() > other.length:
            return True
        else:
            return False
    def __ge__(self, other):
        if self.length() >= other.length:
            return True
        else:
            return False

    def __pow__(self, power, modulo=None):
        return MathX.Vector2(self.x**power, self.y**power)
    ##########