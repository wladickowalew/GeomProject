from math import atan2


class Dot:
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __gt__(self, other):
        return atan2(-self.y, -self.x) > atan2(-other.y, -other.x)


class Line:
    def __init__(self, A, B):
        self.a = A.y - B.y
        self.b = B.x - A.x
        self.c = A.x * B.y - A.y * B.x

    def intersection(self, other):
        d = self.a * other.b - self.b * other.a
        x =   (self.b * other.c - self.c * other.b) / d
        y = - (self.a * other.c - self.c * other.a) / d
        return Dot((x, y))


class Section:
    def __init__(self, A, B):
        self.line = Line(A, B)
        self.A = A
        self.B = B

    def between(self, C):
        return self.A.x <= C.x <= self.B.x or self.B.x <= C.x <= self.A.x

    def intersection(self, angle):
        ans = []
        d = self.line.intersection(angle.BA.line)
        if self.between(d):
            vec = Vector(angle.B, d)
            if vec.kolleniar(angle.BA):
                ans.append(d)
        d = self.line.intersection(angle.BC.line)
        if self.between(d):
            vec = Vector(angle.B, d)
            if vec.kolleniar(angle.BC):
                ans.append(d)
        return ans





class Vector:
    def __init__(self, A, B):
        self.x = B.x - A.x
        self.y = B.y - A.y
        self.line = Line(A, B)

    def kolleniar(self, other):
        return (self.x / other.x - self.y / other.y) < 0.00000001 and self.x * other.x > 0

    def scalar_mult(self, other):
        return self.x * other.x + self.y * other.y

    def abs(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def cos(self, other):
        return self.scalar_mult(other) / (self.abs() * other.abs())


class Angle:
    def __init__(self, A, B, C):
        self.A = A
        self.C = C
        self.B = B
        self.BA = Vector(B, A)
        self.BC = Vector(B, C)
        self.cosABC = self.BA.cos(self.BC)

    def check_dot(self, D):
        BD = Vector(self.B, D)
        cosABD = self.BA.cos(BD)
        cosDBC = BD.cos(self.BC)
        return cosDBC >= self.cosABC and cosABD >= self.cosABC


class Triangle:
    def __init__(self, A, B, C):
        self.A = A
        self.C = C
        self.B = B
        self.ABC = Angle(A, B, C)
        self.BAC = Angle(B, A, C)
        self.BCA = Angle(B, C, A)
        self.sections = [Section(A, B), Section(C, B), Section(A, C)]

    def check_dot(self, D):
        return self.ABC.check_dot(D) and self.BCA.check_dot(D) and self.BAC.check_dot(D)


class Polygon:

    def __init__(self, dots=[]):
        self.dots = dots

    def findCenter(self):
        cx, cy = 0, 0
        for dot in self.dots:
            cx += dot.x
            cy += dot.y
        cx //= len(self.dots)
        cy //= len(self.dots)
        return Dot((cx, cy))

    def normalize(self):
        if not self.dots:
            return
        C = self.findCenter()
        dots1 = [Dot((dot.x - C.x, dot.y - C.y)) for dot in self.dots]
        dots1.sort()
        self.dots = [Dot((dot.x + C.x, dot.y + C.y)) for dot in dots1]

    def area(self):
        if not self.dots:
            return 0
        self.normalize()
        n = len(self.dots)
        s = (self.dots[n - 1].x + self.dots[0].x) * (self.dots[n - 1].y - self.dots[0].y)
        for i in range(n - 1):
            s += (self.dots[i].x + self.dots[i + 1].x) * (self.dots[i].y - self.dots[i + 1].y)
        return abs(s) / 2
