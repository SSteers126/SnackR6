# from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
#                              QHBoxLayout, QVBoxLayout, QMainWindow)
# from PyQt5.QtCore import Qt, QSize
# from PyQt5 import QtWidgets, uic
# import sys
#
#
# class MainWindow(QMainWindow):
#
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
#         self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
#         self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
#
#         for i in range(1,50):
#             object = QLabel("TextLabel")
#             self.vbox.addWidget(object)
#
#         self.widget.setLayout(self.vbox)
#
#         #Scroll Area Properties
#         self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
#         self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.scroll.setWidgetResizable(True)
#         self.scroll.setWidget(self.widget)
#
#         self.setCentralWidget(self.scroll)
#
#         self.setGeometry(600, 100, 1000, 900)
#         self.setWindowTitle('Scroll Area Demonstration')
#         self.show()
#
#         return
#
# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     main = MainWindow()
#     sys.exit(app.exec_())
#
# if __name__ == '__main__':
#     main()


import sys
from PyQt5 import QtWidgets


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        scroll_area = QtWidgets.QScrollArea(central_widget)
        scroll_area.setGeometry(360, 10, 420, 180)
        scroll_area.setWidgetResizable(True)

        container = QtWidgets.QWidget()
        scroll_area.setWidget(container)

        # Set widgets via layout
        lay = QtWidgets.QVBoxLayout(container)
        lay.setContentsMargins(10, 10, 0, 0)
        for letter in "ABCDE":
            text = letter * 100
            label = QtWidgets.QLabel(text)
            lay.addWidget(label)
        lay.addStretch()

        self.setGeometry(300, 300, 803, 520)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())