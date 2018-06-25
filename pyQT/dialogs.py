# encoding: UTF-8

from qtpy.QtWidgets import (QWidget, QPushButton, QLineEdit,
                            QInputDialog, QApplication, QFrame, QColorDialog,
                            QLabel, QProgressBar, QCalendarWidget, QVBoxLayout,
                            QHBoxLayout)
from qtpy.QtGui import QColor, QPixmap
from qtpy.QtCore import QBasicTimer, QDate,Qt

import sys


class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()
        self.timer.start(10, self)

    def initUI(self):
        ml = QVBoxLayout(self)
        ul = QHBoxLayout(self)
        dl = QHBoxLayout(self)
        ml.addLayout(ul)
        ml.addLayout(dl)

        col = QColor(0, 0, 0)
        self.colorText = 'Color Nmae: {}'
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.btn2 = QPushButton('Color', self)
        self.btn2.move(20, 40)
        self.btn2.clicked.connect(self.showColorDialoge)

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())
        self.frm.setGeometry(130, 50, 100, 100)

        self.le = QLineEdit(self)
        self.le.move(130, 22)

        self.label = QLabel(self.colorText.format(None), self)
        self.label.setGeometry(20, 80, 100, 30)

        self.timer = QBasicTimer()
        self.pb = QProgressBar(self)
        self.step = 0
        self.pb.setGeometry(20, 170, 300, 20)

        # calendar
        self.timeLable = QLabel('time is: ', self)
        # self.timeLable.setGeometry(20, 120, 100, 30)
        cal = QCalendarWidget(self)
        cal.clicked[QDate].connect(self.showDate)

        ul.addWidget(self.timeLable)
        dl.addWidget(cal)

        self.setLayout(ml)
        self.setGeometry(300, 300, 550, 550)
        self.setWindowTitle('Dialog')
        self.show()

    def showDialog(self):
        # 通过下面的语句来实现QInputDialog的显示
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Input some thing')

        if ok:
            self.le.setText(text)

    def showColorDialoge(self):
        col = QColorDialog.getColor()   # 获取colorDialog的颜色

        if col.isValid():
            self.label.setText(self.colorText.format(col.name()))
            self.frm.setStyleSheet("QWidget { background-color: %s}" % col.name())

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
        else:
            self.step += 1
            self.pb.setValue(self.step)

    def showDate(self, date):
        d = date.toString(Qt.ISODate)
        self.timeLable.setText(d)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
