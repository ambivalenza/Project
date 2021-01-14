import sqlite3
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QHeaderView

DB_FILE = 'leaderboard.sqlite'


class DB:
    def __init__(self):
        self.connection = sqlite3.connect(DB_FILE)

    def query(self, difficulty):
        query = f'''SELECT name, score FROM leaderboards WHERE difficulty = "{difficulty}" order by score desc'''
        return self.connection.cursor().execute(query).fetchall()

    def save(self, name, difficulty, score):
        res = self.connection.execute(
            f"SELECT * FROM leaderboards WHERE name = '{name}' AND difficulty = '{difficulty}'").fetchone()
        if res:
            self.connection.execute(f'''
        UPDATE leaderboards 
        SET score = {score}
        WHERE name = '{name}' AND difficulty = '{difficulty}'
        ''')
        else:
            self.connection.execute(f'''
            INSERT INTO leaderboards     (
                                  difficulty,
                                  name, 
                                  score
                              )
                              VALUES (
                                  "{difficulty}",
                                  "{name}",
                                  {score}
                              );''')
        self.connection.commit()

class Ui_Dialog(object):
    def __init__(self, difficulty, *args, **kwargs):
        self.db = DB()
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
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(['nickname', 'score'])

        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.db.query(self.difficulty)):
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
