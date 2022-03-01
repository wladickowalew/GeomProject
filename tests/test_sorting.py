from math import atan2


class Dot:
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __gt__(self, other):
        return atan2(-self.y, -self.x) > atan2(-other.y, -other.x)


def normalize(dots):
    cx, cy = 0, 0
    for dot in dots:
        cx += dot.x
        cy += dot.y
    cx /= len(dots)
    cy /= len(dots)
    C = Dot((cx, cy))
    dots1 = [Dot((dot.x - C.x, dot.y - C.y)) for dot in dots]
    dots1.sort()
    return [Dot((dot.x + C.x, dot.y + C.y)) for dot in dots1]


input_dots = [Dot((6, 9)), Dot((8, 2)), Dot((2, 6)), Dot((10, 6)), Dot((4, 3))]
res = normalize(input_dots)
print(input_dots)
print(res)
