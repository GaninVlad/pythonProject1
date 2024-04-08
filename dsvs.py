import csv
import io
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMainWindow
a = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
<class>MainWindow</class>
<widget class="QMainWindow" name="MainWindow">
<property name="geometry">
<rect>
<x>0</x>
<y>0</y>
<width>1077</width>
<height>817</height>
</rect>
</property>
<property name="windowTitle">
<string>MainWindow</string>
</property>
<widget class="QWidget" name="centralwidget">
<widget class="QTableWidget" name="tableWidget">
<property name="geometry">
<rect>
<x>20</x>
<y>40</y>
<width>1021</width>
<height>711</height>
</rect>
</property>
<property name="minimumSize">
<size>
<width>1021</width>
<height>711</height>
</size>
</property>
<property name="maximumSize">
<size>
<width>1021</width>
<height>711</height>
</size>
</property>
<row>
<property name="text">
<string>Математика и механика</string>
</property>
</row>
<row>
<property name="text">
<string>Компьютерные и информационные науки</string>
</property>
</row>
<row>
<property name="text">
<string>Физика и астрономия</string>
</property>
</row>
<column>
<property name="text">
<string>Специальность</string>
</property>
</column>
<column>
<property name="text">
<string>численность выпускников в тыс</string>
</property>
</column>
<column>
<property name="text">
<string>соответствует в тыс</string>
</property>
</column>
<column>
<property name="text">
<string>соответствует в %</string>
</property>
</column>
<column>
<property name="text">
<string>не соответствует в %</string>
</property>
</column>
<item row="0" column="0">
<property name="text">
<string>29.3</string>
</property>
</item>
<item row="0" column="1">
<property name="text">
<string>20.6</string>
</property>
</item>
<item row="0" column="2">
<property name="text">
<string>8.7</string>
</property>
</item>
<item row="0" column="3">
<property name="text">
<string>70</string>
</property>
</item>
<item row="0" column="4">
<property name="text">
<string>30</string>
</property>
</item>
<item row="1" column="0">
<property name="text">
<string>8.3</string>
</property>
</item>
<item row="1" column="1">
<property name="text">
<string>6.1</string>
</property>
</item>
<item row="1" column="2">
<property name="text">
<string>2.2</string>
</property>
</item>
<item row="1" column="3">
<property name="text">
<string>74</string>
</property>
</item>
<item row="1" column="4">
<property name="text">
<string>27</string>
</property>
</item>
<item row="2" column="0">
<property name="text">
<string>8.4</string>
</property>
</item>
<item row="2" column="1">
<property name="text">
<string>5.8</string>
</property>
</item>
<item row="2" column="2">
<property name="text">
<string>2.6</string>
</property>
</item>
<item row="2" column="3">
<property name="text">
<string>69</string>
</property>
</item>
<item row="2" column="4">
<property name="text">
<string>31</string>
</property>
</item>
</widget>
</widget>
<widget class="QMenuBar" name="menubar">
<property name="geometry">
<rect>
<x>0</x>
<y>0</y>
<width>1077</width>
<height>26</height>
</rect>
</property>
</widget>
<widget class="QStatusBar" name="statusbar"/>
</widget>
<resources/>
<connections/>
</ui>
'''
class InteractiveReceipt(QMainWindow):
    def __init__(self):
        super().__init__()
        design = io.StringIO(a)
        uic.loadUi(design, self)
        self.load_table("vps.csv")

    def load_table(self, table_name):
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for i, row in enumerate(reader):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(elem))
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem('0'))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.itemChanged.connect(self.result)

    def result(self):
        print(self.tableWidget.rowCount(4))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InteractiveReceipt()
    ex.show()
    sys.exit(app.exec())