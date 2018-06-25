import sys
from qtpy.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLCDNumber, QSlider, QMainWindow, QTextEdit, QLineEdit, QMessageBox, QCalendarWidget
from qtpy.QtCore import Qt, QObject, QDate
from qtpy.QtCore import Signal
# from PyQt5.QtCore import pyqtSignal
from mymodule.completedata import completestockdata, dailyUpdate

class Communicate(QObject):
    closeApp = Signal()


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        lbl1 = QLabel('Zetcode', self)
        lbl1.move(15, 10)

        lbl2 = QLabel('tutorials', self)
        lbl2.move(35, 40)

        lbl3 = QLabel('for programmers', self)
        lbl3.move(55, 70)

        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')

        hbox = QHBoxLayout()
        hbox.addStretch(1)  # 会随着窗口伸缩而变动位置
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        #vbox.addStretch(1)
        vbox.addLayout(hbox)
        # vbox.setGeometry()

        self.setLayout(vbox)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Absolute')
        self.show()


class gridBox(QWidget):

    def __init__(self):
        super(gridBox, self).__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        names = ['1', '2', '3', '4', '5', '6']
        positions = [(i, j) for i in range(2) for j in range(3)]

        for position, name in zip(positions, names):
            button = QPushButton(name)
            grid.addWidget(button, *position)

        self.move(300, 300)
        self.show()


class signalExample(QWidget):
    def __init__(self):
        super(signalExample, self).__init__()
        self.text = 'x @ {x}, y @ {y}'.format(x=0, y=0)
        self.pushRecord = 'this is a test'
        self.initUI()

    def initUI(self):
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)
        self.lable = QLabel(self.text, self)
        btn = QPushButton('bt1', self)
        btn2 = QPushButton('bt2', self)
        self.lable2 = QLabel(self.pushRecord, self)

        hbox = QHBoxLayout()
        hbox.addWidget(btn)
        hbox.addWidget(btn2)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)
        vbox.addWidget(self.lable)
        vbox.addLayout(hbox)
        vbox.addWidget(self.lable2)

        self.setLayout(vbox)
        sld.valueChanged.connect(lcd.display)   # sld的value会传入display
        self.setMouseTracking(True)
        btn.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Event handler')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def mouseMoveEvent(self, e):
        self.text = 'x @ {x}, y @ {y}'.format(x=e.x(), y=e.y())
        self.lable.setText(self.text)

    def buttonClicked(self):
        sender = self.sender()
        self.pushRecord += sender.text() + '\n'
        self.lable2.setText(self.pushRecord)
        # self.statusBar().showMessage()


class dataComplete(QWidget):
    """数据补充的界面"""

    def __init__(self):
        super(dataComplete, self).__init__()
        self.n = 1
        self.start = None
        self.end = None
        self.text = ''
        self.initUI()

    def initUI(self):
        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)

        vl1 = QVBoxLayout()
        vl2 = QVBoxLayout()

        # 按钮
        lastData = QPushButton('Last n days Data')
        todayButton = QPushButton('Today Data')
        periodData = QPushButton('Period Data')

        # N lable 提示 以及读取
        daysChoose = QLineEdit(self)
        daysChoose.textChanged[str].connect(self.onChanged)
        daysChooseHint = QLabel('PLZ Enter n:')
        daysChooseHint.setMaximumHeight(10)

        todayButton.clicked.connect(dailyUpdate)
        lastData.clicked.connect(self.showMessage)

        vl1.addWidget(todayButton)
        vl1.addWidget(daysChooseHint)
        vl1.addWidget(daysChoose)
        vl1.addWidget(lastData)
        vl1.addWidget(periodData)

        # 右侧消息框
        # messageBox = QLabel('Here are some code things')
        self.logMoniter = QTextEdit(self)
        self.logMoniter.setMinimumSize(25, 300)
        # logMoniter.setBaseSize(10, 300)
        vl2.addWidget(self.logMoniter)

        mainLayout.addLayout(vl1)
        mainLayout.addLayout(vl2)

        self.move(300, 300)
        self.setWindowTitle("Data Complete")
        # self.show()

    def onChanged(self, s):
        """改变n的值"""
        i = int(s)
        self.n = i

    def showMessage(self):
        """弹框确认是否补充n天前的数据"""
        reply = QMessageBox.question(self, 'Message', 'your n is {}, sure to complete?'.format(self.n),
                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            dailyUpdate(self.n)

    def updateLeft(self, date):
        self.text += date.toString(Qt.ISODate) + '\n'
        self.logMoniter.setText(self.text)

    def updateRight(self, date):
        pass


class calendar(QWidget):
    def __init__(self, mainWindow):
        super(calendar, self).__init__()
        self.mainWindow = mainWindow
        self.initUI()

    def initUI(self):
        cal = QCalendarWidget(self)
        cal.clicked[QDate].connect(self.mainWindow.updateLeft)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = dataComplete()
    sys.exit(app.exec_())
