import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem


class Ui_Dialog(object):
    def __init__(self, difficulty, connection, *args, **kwargs):
        self.connection = connection
        self.difficulty = difficulty
        super().__init__(*args, **kwargs)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(321, 402)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(30, 40, 261, 331))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['nickname', 'score'])
        query = f'''SELECT name, score FROM leaderboards WHERE difficulty = "{self.difficulty}" order by score desc'''
        try:
            res = self.connection.cursor().execute(query).fetchall()
        except:
            import traceback
            print(traceback.format_exc())
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.label_leaderboard = QtWidgets.QLabel(Dialog)
        self.label_leaderboard.setGeometry(QtCore.QRect(30, 10, 271, 16))
        font = QtGui.QFont()
        font.setFamily("monaco")
        font.setPointSize(12)
        self.label_leaderboard.setFont(font)
        self.label_leaderboard.setObjectName("label_leaderboard")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_leaderboard.setText(_translate("Dialog", f"таблица лидеров уровня {self.difficulty}"))

    def start_window(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_Dialog()
        ui.setupUi(MainWindow)
        MainWindow.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
