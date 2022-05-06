from PyQt5 import uic
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon
from logic import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui/MainWindow.ui', self)
        self.addTriangleBtn.clicked.connect(self.add_triangle_click)
        self.addAngleBtn.clicked.connect(self.add_angle_click)
        self.loadBtn.clicked.connect(self.load_from_file_click)
        self.solveBtn.clicked.connect(self.solve_click)
        self.cancelBtn.clicked.connect(self.cancel_click)
        self.addTriangleByCoordBtn.clicked.connect(self.add_triangle_by_coord_click)
        self.addAngleByCoordBtn.clicked.connect(self.add_angle_by_coord_click)
        self.clearBtn.clicked.connect(self.clear_all_click)
        self.cancelBtn.hide()

    def add_triangle_by_coord_click(self):
        dots = self.read_data_from_TE()
        if dots:
            triangles.append(Triangle(*dots))
            self.update()
        print("add triangle by coord")

    def add_angle_by_coord_click(self):
        dots = self.read_data_from_TE()
        if dots:
            angles.append(Angle(*dots))
            self.update()
        print("add angle by coord")

    def clear_all_click(self):
        clear_data()
        self.coordALE.setText("")
        self.coordBLE.setText("")
        self.coordCLE.setText("")
        self.ansLBL.setText("Искомая площадь равна: не вычислено")
        self.update_buttons()
        self.update()

    def add_triangle_click(self):
        print("add triangle")
        mode["triangle"] = True
        self.update_buttons()

    def add_angle_click(self):
        mode["angle"] = True
        self.update_buttons()

    def load_from_file_click(self):
        file_name = QFileDialog.getOpenFileName(self, 'Выберите файл', '/home')[0]
        load_from_file(file_name)
        self.update()

    def solve_click(self):
        p = solve()
        if p is None:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Отсутствуют пересечения углов и треугольников")
            msgBox.exec()
            return
        if not polygons:
            polygons.append(0)
        polygons[0] = p
        self.ansLBL.setText(f"Искомая площадь равна: {polygons[0].area()}")
        self.update()

    def cancel_click(self):
        edit_mode_off()
        self.update()
        self.update_buttons()

    def read_data_from_TE(self):
        try:
            A = Dot([float(i) for i in self.coordALE.text().split()])
            B = Dot([float(i) for i in self.coordBLE.text().split()])
            C = Dot([float(i) for i in self.coordCLE.text().split()])
            if not self.dot_in_field(A.x, A.y):
                raise Exception
            if not self.dot_in_field(B.x, B.y):
                raise Exception
            if not self.dot_in_field(C.x, C.y):
                raise Exception
            self.coordALE.setText("")
            self.coordBLE.setText("")
            self.coordCLE.setText("")
            return A, B, C
        except Exception:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                "Неверный формат ввода. Проверьте корректность заполнения полей. Так же ваши координаты не должны быть слишком большими!")
            msgBox.setWindowTitle("Что-то не так с вашими данными((")
            msgBox.exec()

    def update_buttons(self):
        vidgets = [self.addAngleBtn, self.addTriangleBtn, self.loadBtn, self.solveBtn,
                   self.addTriangleByCoordBtn, self.addAngleByCoordBtn, self.clearBtn,
                   self.coordALE, self.coordBLE, self.coordCLE]
        if mode["triangle"] or mode["angle"]:
            self.cancelBtn.show()
            for vidget in vidgets:
                vidget.setEnabled(False)
        else:
            self.cancelBtn.hide()
            for vidget in vidgets:
                vidget.setEnabled(True)

    def dot_in_field(self, x, y):
        return 250 <= x <= 1050 and 20 <= y <= 640

    def mousePressEvent(self, event):
        if not (mode["triangle"] or mode["angle"]):
            return
        x, y = event.x(), event.y()
        if event.button() == Qt.LeftButton and self.dot_in_field(x, y):
            add_dot(Dot((x - 650, 330 - y)))
            self.update()
            self.update_buttons()

    #################   Painting   #################

    def paintEvent(self, ev):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.paintDecartSystem(qp)
        self.paintAngles(qp)
        self.paintTriangles(qp)
        self.paintDots(qp)
        self.paintPolygon(qp)

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
        # self.paintLine(qp, TOP_LEFT, TOP_RIGHT)
        # self.paintLine(qp, BOTTOM_LEFT, BOTTOM_RIGHT)
        # self.paintLine(qp, TOP_LEFT, BOTTOM_LEFT)
        # self.paintLine(qp, TOP_RIGHT, BOTTOM_RIGHT)

    def paintDot(self, qp, dot):
        qp.drawEllipse(int(650 + dot.x - 2), int(330 - dot.y - 2), 4, 4)

    def paintLine(self, qp, A, B):
        qp.drawLine(int(A.x + 650), int(330 - A.y), int(B.x + 650), int(330 - B.y))

    def paintAngles(self, qp):
        pen = QPen(Qt.green, 2)
        brush = QBrush(Qt.green)
        qp.setPen(pen)
        qp.setBrush(brush)
        for tr in angles:
            self.paintDot(qp, tr.A)
            self.paintDot(qp, tr.B)
            self.paintDot(qp, tr.C)
            self.paintLine(qp, tr.B, intersection_with_border(tr, tr.A, tr.BA))
            self.paintLine(qp, tr.B, intersection_with_border(tr, tr.C, tr.BC))

    def paintTriangles(self, qp):
        pen = QPen(Qt.red, 2)
        brush = QBrush(Qt.red)
        qp.setPen(pen)
        qp.setBrush(brush)
        for tr in triangles:
            self.paintDot(qp, tr.A)
            self.paintDot(qp, tr.B)
            self.paintDot(qp, tr.C)
            self.paintLine(qp, tr.A, tr.B)
            self.paintLine(qp, tr.B, tr.C)
            self.paintLine(qp, tr.A, tr.C)

    def paintDots(self, qp):
        pen = QPen(Qt.blue, 2)
        brush = QBrush(Qt.blue)
        qp.setPen(pen)
        qp.setBrush(brush)
        for dot in current_dots:
            self.paintDot(qp, dot)

    def convertP2P(self, polygon):
        ans = QPolygon()
        for dot in polygon.dots:
            p = QPoint(650 + int(dot.x), 330 - int(dot.y))
            ans.append(p)
        return ans

    def paintPolygon(self, qp):
        if not polygons:
            return
        pen = QPen(Qt.black, 2)
        brush = QBrush(Qt.magenta)
        qp.setPen(pen)
        qp.setBrush(brush)
        points = self.convertP2P(polygons[0])
        qp.drawPolygon(points)
