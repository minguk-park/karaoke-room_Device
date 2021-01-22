import sys
import os, glob
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(400, 200, 1000, 600)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(1000, 600)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.setTableWidgetData()

    def setTableWidgetData(self):
        column_headers = ['예약번호', '노래제목', '가수', '조회수']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        # 파일 가져와 저장
        targerdir = r"C:\Users\Mujac\Desktop\temp"
        files = os.listdir(targerdir)
        song_dict = []  # 노래저장

        for i in files:
            split_song = i[:-4].split(',')
            song_dict.append(split_song)

        for row, val in enumerate(song_dict):
            col=0
            for a in val:
                item = QTableWidgetItem(a)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                self.tableWidget.setItem(row, col, item)
                col=col+1
            row = row + 1

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()