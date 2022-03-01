from geom_objects import *
import logic
import sys
import traceback
from PyQt5 import uic
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui/MainWindow.ui', self)
        self.addTriangleBtn.clicked.connect(self.add_triangle)
        self.addAngleBtn.clicked.connect(self.add_angle)
        self.loadBtn.clicked.connect(self.load_from_file)
        self.solveBtn.clicked.connect(self.solve)
        self.cancelBtn.clicked.connect(self.cancel)
        self.cancelBtn.hide()
        self.angles = []
        self.triangles = []
        self.dots = []
        self.angle_edit = False
        self.triangle_edit = False
        self.current_dots = []
        self.polygon = None

    def add_triangle(self):
        self.triangle_edit = True
        self.update_buttons()
        print("add Triangle")

    def add_angle(self):
        self.angle_edit = True
        self.update_buttons()
        print("add angle")

    def load_from_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Выберите файл', '/home')[0]
        file = open(fname)
        count_t, count_a = map(int, file.readline().split())
        for _ in range(count_t):
            x1, y1, x2, y2, x3, y3 = map(float, file.readline().split())
            self.triangles.append(Triangle(self.convert_coord(x1, y1),
                                           self.convert_coord(x2, y2),
                                           self.convert_coord(x3, y3)))
        for _ in range(count_a):
            x1, y1, x2, y2, x3, y3 = map(float, file.readline().split())
            self.angles.append(Angle(self.convert_coord(x1, y1),
                                     self.convert_coord(x2, y2),
                                     self.convert_coord(x3, y3)))
        file.close()
        self.update()

    def solve(self):
        self.polygon = logic.solve(self.angles, self.triangles)
        print(self.polygon.area())
        self.update()

    def convertP2P(self, polygon):
        ans = QPolygon()
        for dot in polygon.dots:
            p = QPoint(dot.x, dot.y)
            ans.append(p)
        return ans

    def paintPolygon(self, qp):
        if self.polygon is None:
            return
        pen = QPen(Qt.green, 3)
        brush = QBrush(Qt.green)
        qp.setPen(pen)
        qp.setBrush(brush)
        points = self.convertP2P(self.polygon)
        qp.drawPolygon(points)

    def cancel(self):
        self.angle_edit = False
        self.triangle_edit = False
        self.current_dots = []
        self.update()
        self.update_buttons()
        print("cancel")

    def paintEvent(self, ev):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.paintDecartSystem(qp)
        self.paintAngles(qp)
        self.paintTriangles(qp)
        self.paintDots(qp)
        self.paintPolygon(qp)


    def paintAngles(self, qp):
        pen = QPen(Qt.green, 3)
        brush = QBrush(Qt.green)
        qp.setPen(pen)
        qp.setBrush(brush)
        for tr in self.angles:
            self.paintDot(qp, tr.A)
            self.paintDot(qp, tr.top)
            self.paintDot(qp, tr.C)
            self.paintLine(qp, tr.top, tr.A)
            self.paintLine(qp, tr.top, tr.C)

    def paintTriangles(self, qp):
        pen = QPen(Qt.red, 3)
        brush = QBrush(Qt.red)
        qp.setPen(pen)
        qp.setBrush(brush)
        for tr in self.triangles:
            self.paintDot(qp, tr.A)
            self.paintDot(qp, tr.B)
            self.paintDot(qp, tr.C)
            self.paintLine(qp, tr.A, tr.B)
            self.paintLine(qp, tr.B, tr.C)
            self.paintLine(qp, tr.A, tr.C)

    def paintDots(self, qp):
        pen = QPen(Qt.blue, 3)
        brush = QBrush(Qt.blue)
        qp.setPen(pen)
        qp.setBrush(brush)
        for dot in self.current_dots:
            self.paintDot(qp, dot)


    def paintDot(self, qp, dot):
        qp.drawEllipse(dot.x - 2, dot.y - 2, 4, 4)


    def paintLine(self, qp, A, B):
        qp.drawLine(A.x, A.y, B.x, B.y)


    def paintDecartSystem(self, qp):
        pen = QPen(Qt.black, 1)
        brush = QBrush(Qt.black)
        qp.setPen(pen)
        qp.setBrush(brush)
        qp.drawLine(650, 30, 650, 639)
        qp.drawLine(650, 30, 655, 35)
        qp.drawLine(650, 30, 645, 35)
        qp.drawLine(250, 330, 1050, 330)
        qp.drawLine(1050, 330, 1045, 335)
        qp.drawLine(1050, 330, 1045, 325)


    def update_buttons(self):
        if self.angle_edit or self.triangle_edit:
            self.cancelBtn.show()
            self.addAngleBtn.setEnabled(False)
            self.addTriangleBtn.setEnabled(False)
            self.loadBtn.setEnabled(False)
            self.solveBtn.setEnabled(False)
        else:
            self.cancelBtn.hide()
            self.addAngleBtn.setEnabled(True)
            self.addTriangleBtn.setEnabled(True)
            self.loadBtn.setEnabled(True)
            self.solveBtn.setEnabled(True)


    def dot_in_field(self, x, y):
        return 250 <= x <= 1050 and 20 <= y <= 640


    def mousePressEvent(self, event):
        if not (self.angle_edit or self.triangle_edit):
            return
        x, y = event.x(), event.y()
        if event.button() == Qt.LeftButton and self.dot_in_field(x, y):
            self.add_dot(Dot((x, y)))


    def add_dot(self, dot):
        self.dots.append(dot)
        self.current_dots.append(dot)
        if len(self.current_dots) == 3:
            if self.angle_edit:
                self.angles.append(Angle(*self.current_dots))
                self.angle_edit = False
            elif self.triangle_edit:
                self.triangles.append(Triangle(*self.current_dots))
                self.triangle_edit = False
            self.current_dots = []
        self.update()
        self.update_buttons()

    def convert_coord(self, x, y):
        return Dot((x + 650, 330 - y))


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


if __name__ == '__main__':
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
