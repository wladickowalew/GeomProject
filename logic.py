from geom_objects import *

angles = []
triangles = []
dots = []
mode = {
    "angle": False,
    "triangle": False
}
current_dots = []
polygons = []


def load_from_file(file_name):
    file = open(file_name)
    count_t, count_a = map(int, file.readline().split())
    for _ in range(count_t):
        x1, y1, x2, y2, x3, y3 = map(float, file.readline().split())
        triangles.append(Triangle(Dot((x1, y1)), Dot((x2, y2)), Dot((x3, y3))))
    for _ in range(count_a):
        x1, y1, x2, y2, x3, y3 = map(float, file.readline().split())
        angles.append(Angle(Dot((x1, y1)), Dot((x2, y2)), Dot((x3, y3))))
    file.close()


def edit_mode_off():
    mode["angle"] = False
    mode["triangle"] = False
    current_dots.clear()


def add_dot(dot):
    dots.append(dot)
    current_dots.append(dot)
    if len(current_dots) == 3:
        if mode["angle"]:
            angles.append(Angle(*current_dots))
            mode["angle"] = False
        elif mode["triangle"]:
            triangles.append(Triangle(*current_dots))
            mode["triangle"] = False
        current_dots.clear()


def clear_data():
    polygons.clear()
    angles.clear()
    triangles.clear()
    current_dots.clear()
    mode["angle"] = False
    mode["triangle"] = False


def solve():
    print(angles)
    print(triangles)
    ansP, maxS = None, 0
    for triangle in triangles:
        for angle in angles:
            p = findPolygon(triangle, angle)
            S = p.area()
            if S > maxS:
                ansP, maxS = p, S
    return ansP


def findPolygon(triange, angle):
    # ans = Polygon([Dot((0, 0)), Dot((50, 0)),
    #                Dot((0, 30)), Dot((50, 30)),
    #                Dot((25, 50))])
    ans = Polygon([])
    # add simple dots
    if angle.check_dot(triange.A):
        ans.dots.append(triange.A)
    if angle.check_dot(triange.B):
        ans.dots.append(triange.B)
    if angle.check_dot(triange.C):
        ans.dots.append(triange.C)
    if triange.check_dot(angle.B):
        ans.dots.append(angle.B)
    # add intersections
    for section in triange.sections:
        ans.dots.extend(section.intersection(angle))
    return ans
