class Dot:
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]


class Line:
    def __init__(self, A, B):
        self.a = A.y - B.y
        self.b = B.x - A.x
        self.b = A.x * B.y - A.y * B.x


class Vector:
    def __init__(self, A, B):
        self.x = B.x - A.x
        self.y = B.y - A.y

    def scalar_mult(self, other):
        return self.x * other.x + self.y * other.y

    def abs(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def cos(self, other):
        return self.scalar_mult(other) / (self.abs() * other.abs())


class Angle:
    def __init__(self, A, B, C):
        self.top = B
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
        self.ABC = Angle(A, B, C)
        self.BAC = Angle(B, A, C)
        self.BCA = Angle(B, C, A)

    def check_dot(self, D):
        return self.ABC.check_dot(D) and self.BCA.check_dot(D) and self.BAC.check_dot(D)


class Polygon:
    def __init__(self):
        self.dots = set()

    def normalize(self):  #преобразование множества точек в список (упорядочивание точек)
        return []

    def area(self):
        dots = self.normalize()
        n = len(dots)
        s = (dots[n - 1].x + dots[0].x) * (dots[n - 1].y - dots[0].y)
        for i in range(n - 1):
            s += (dots[i].x + dots[i + 1].x) * (dots[i].y - dots[i + 1].y)
        return abs(s) / 2


