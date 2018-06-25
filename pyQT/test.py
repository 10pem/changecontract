from qtpy.QtCore import QDate, QDateTime, QTime, Qt
from qtpy.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget, QMainWindow, QAction, qApp, QMenu
from qtpy.QtGui import QIcon
from qtpy import QtGui
import sys

now = QDate.currentDate()

print(now.toString(Qt.ISODate))
print(now.toString(Qt.DefaultLocaleLongDate))

datetime = QDateTime.currentDateTime()
print(datetime.toString())

time = QTime.currentTime()
print(time.toString(Qt.DefaultLocaleLongDate))

# localdatetime
print(datetime.toString(Qt.ISODate))
# Universal datetime
print(datetime.toUTC().toString(Qt.ISODate))


class Example(QMainWindow):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):

        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')   # 设置快捷键
        exitAct.setStatusTip('Exit app')    # 设置状态栏提醒
        exitAct.triggered.connect(qApp.quit)

        # 子目录
        impMenu = QMenu('import', self)
        subAct = QAction('test', self)
        impMenu.addAction(subAct)

        # check菜单
        viewStatAct = QAction('View Statusbar', self)
        viewStatAct.setStatusTip('View statusbar')
        viewStatAct.setCheckable(True)  # 开启打钩模式
        viewStatAct.triggered.connect(self.toggleMenu)  # toggleMenu会传入参数

        # 状态栏
        self.statusBar().showMessage('Ready')

        # 菜单栏
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(exitAct)
        fileMenu.addMenu(impMenu)
        fileMenu.addAction(viewStatAct)

        self.resize(250, 150)
        self.center()
        self.setWindowTitle('Message box')
        self.show()

        # 工具栏(菜单栏某几个工具的快速使用)
        self.toolbar = self.addToolBar('Exti')
        self.toolbar.addAction(exitAct)

    def toggleMenu(self, state):
        if state:
            self.statusBar().show()
        else:
            self.statusBar().hide() # 关闭状态栏

    def center(self):
        """居中显示"""
        qr = self.frameGeometry()   # 获得frame
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    ## EVENT

    def closeEvent(self, event):
        """"""
        reply = QMessageBox.question(self, 'Message', 'sure?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def contextMenuEvent(self, event):
        """也叫弹出式菜单, 就是右键单击弹出"""
        cmenu = QMenu(self)

        newAct = cmenu.addAction('New')
        openAct = cmenu.addAction('Open')
        quitAct = cmenu.addAction('Quit')

        # 从event获取位置信息, 通过mapToGlobal
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            qApp.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
