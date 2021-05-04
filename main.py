import sys, os
import random
from pathlib import Path
import r6statsapi
import asyncio
loop = asyncio.get_event_loop()
client = r6statsapi.Client("TOKEN")
import globalfile
# TODO: move to pyside6 when 6.1 is released for graphs
# PySide is a huge library, so we import what we want explixitly
from PySide2.QtCore import (Qt, QRectF, QSize, QRect, QDateTime, QDir, Signal, QMetaObject)
from PySide2.QtGui import (QPalette, QColor, QRadialGradient, QLinearGradient, QConicalGradient,
                           QBrush, QGradient, QFont, QPixmap, QIcon)
from PySide2.QtWidgets import (QVBoxLayout, QHBoxLayout, QStyleFactory, QWidget, QLineEdit, QPushButton, QApplication,
                               QDialog, QMainWindow, QLabel, QGroupBox, QDoubleSpinBox, QSpinBox, QDateTimeEdit, QComboBox,
                               QStatusBar, QMenuBar,
                               QDateEdit,
                               QCheckBox, QTextEdit, QTabWidget, QFileSystemModel, QTreeView)
# from PySide2.QtCharts import (QLineSeries)
from PySide2.QtCharts import QtCharts

from PIL import Image, ImageOps, ImageDraw, ImageFont

import ctypes
try:  # This code is windows specific, so requires protection
    newappid = u'Zestyy.SnackR6.GUI.V1' # these lines are used to seperate the app from the python 'umbrella'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(newappid)
except:
    pass

# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.setWindowTitle("MainWindow")
#         MainWindow.resize(750, 500)# 58, 58
#         self.centralwidget = QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         MainWindow.setCentralWidget(self.centralwidget)
#         QMetaObject.connectSlotsByName(MainWindow)


class un_input(QDialog):
    def __init__(self, parent=None):
        super(un_input, self).__init__(parent)
        self.setWindowIcon(QIcon("src/logo/Snack-R6-icon.png"))
        QApplication.setStyle(QStyleFactory.create("fusion"))
        QApplication.setFont(QFont("Helvetica", 11, 60))  # Montserrat Medium
        self.setWindowTitle("View statistics")
        self.resize(750, 500)
        dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
        path = dir_path / "src" / "ranks"
        oppath = dir_path / "src" / "ranks" / "250"
        # for imgpath in os.listdir(path):  # NOTE: folder image resize script
        #     if len(imgpath.split(".")) > 1:
        #         # print(imgpath)
        #         img = Image.open(path / imgpath)
        #         img = img.resize([int(img.size[0]*0.5), int(img.size[1]*0.5)], 3)
        #         img.save(oppath / imgpath)
        logo = Image.open("src/logo/Snack-R6-logo.png")
        logo = logo.resize([int(logo.size[0]*0.0625), int(logo.size[1]*0.0625)], 3) # 3 for bicubic filtering
        logo.save("SL.png")
        print(logo.size)
        # logosize = logo.
        Qtlogo = QPixmap("src/logo/SL.png")
        self.LogoLabel = QLabel()
        self.LogoLabel.setPixmap(Qtlogo)
        self.LogoLabel.setAlignment(Qt.AlignHCenter)
        # logo.

        self.PanelPalette = QPalette()
        self.bggradient = QConicalGradient().AmyCrisp

        self.UNlabel = QLabel("Username: ")
        self.UNinput = QLineEdit()
        self.UNinput.setWhatsThis("Input the account name here!")
        self.UNlayout = QHBoxLayout()
        self.UNlayout.addWidget(self.UNlabel)
        self.UNlayout.addWidget(self.UNinput)
        # self.UNlayout.addWidget(self.UNconf)

        self.PlatformLabel = QLabel("Platform: ")
        self.PlatformInput = QComboBox()
        self.PlatformInput.setWhatsThis("Choose the platform of the stats you want to see!")
        self.PlatformInput.addItems(["PC", "XBOX", "PlayStation"])
        self.PlatformLayout = QHBoxLayout()
        self.PlatformLayout.addWidget(self.PlatformLabel)
        self.PlatformLayout.addWidget(self.PlatformInput)

        self.UNconf = QPushButton("Get stats!")

        self.PanelPalette.setBrush(QPalette.Window, QBrush(self.bggradient))

        self.error_text = QLabel()
        self.error_text.setAlignment(Qt.AlignBottom)
        self.error_text.setWhatsThis("Shows the status of the window, or the most recent error.")
        self.createStatusBar()

        self.PanelLayout = QVBoxLayout()
        self.PanelLayout.setAlignment(Qt.AlignCenter)
        self.PanelLayout.addWidget(self.LogoLabel)
        self.PanelLayout.addSpacing(50)
        self.PanelLayout.addLayout(self.UNlayout)
        self.PanelLayout.addLayout(self.PlatformLayout)
        self.PanelLayout.addWidget(self.UNconf)
        self.PanelLayout.addSpacing(20)
        self.PanelLayout.addWidget(self.error_text)


        self.SpacedLayout = QHBoxLayout()
        self.SpacedLayout.addSpacing(20)
        self.SpacedLayout.addLayout(self.PanelLayout)
        self.SpacedLayout.addSpacing(20)
        # self.SpacedLayout.addWidget(self.error_text)

        # self.FinalLayout = QVBoxLayout()
        # self.FinalLayout.addLayout(self.SpacedLayout)
        # self.FinalLayout.addWidget(self.error_text)

        self.setPalette(self.PanelPalette)
        self.setLayout(self.SpacedLayout)

        self.UNconf.clicked.connect(lambda: Manager.ShowMain(self, username=self.UNinput.text(), platform=self.PlatformInput.currentText()))


    def changeStatusBar(self, text, *, isError=False, isWarn=False, isSuccess=False):  # * means you have to call isError, isWarn, or isSuccess by name.
        newPalette = QPalette()
        if isError:
            newPalette.setColor(QPalette.WindowText, Qt.red)
        elif isWarn:
            newPalette.setColor(QPalette.WindowText, Qt.yellow)
        elif isSuccess:
            newPalette.setColor(QPalette.WindowText, Qt.green)
        else:
            newPalette.setColor(QPalette.WindowText, Qt.white)
        self.error_text.setPalette(newPalette)
        self.error_text.setText(text)

    def createStatusBar(self):
        self.error_text.setText("Ready!")

    def OpenMain(self):
        main_win = main_panel(self.UNinput.text())
        main_win.show()
        self.close()


class main_panel(QMainWindow):
    resized = Signal()
    def __init__(self, username="", userplatform="PC", parent=None):
        super(main_panel, self).__init__(parent)
        self.setWindowIcon(QIcon("src/logo/Snack-R6-icon.png"))
        QApplication.setStyle(QStyleFactory.create("fusion"))
        QApplication.setFont(QFont("Helvetica", 11, 60))  # Montserrat Medium
        self.setWindowTitle("View statistics")
        self.resize(1000, 750)
        # ui = Ui_MainWindow()
        # ui.setupUi(self)

        self.PanelPalette = QPalette()#styling
        self.bggradient = QConicalGradient(800.0, 694.0, 167.0).AquaSplash
        # self.bggradient.setColorAt(0.0, QColor(0, 0, 0))
        # self.bggradient.setColorAt(0.95, QColor(30, 10, 80))
        # self.bggradient.setColorAt(0.975, QColor(40, 15, 110))
        # self.bggradient.setColorAt(0.985, QColor(25, 11, 60))
        # self.bggradient.setColorAt(0.988, QColor(10, 10, 10))
        # self.bggradient.setColorAt(1.0, QColor(0, 0, 0))

        # Change palette to suit background of window

        self.PanelPalette.setColor(QPalette.Window, QColor(56, 76, 76))
        self.PanelPalette.setColor(QPalette.WindowText, Qt.white)

        self.PanelPalette.setColor(QPalette.Button, QColor(20, 50, 60))
        self.PanelPalette.setColor(QPalette.ButtonText, QColor(200, 200, 200))
        self.PanelPalette.setColor(QPalette.Highlight, QColor(110, 110, 110))

        self.PanelPalette.setColor(QPalette.Base, QColor(50, 60, 70))
        self.PanelPalette.setColor(QPalette.Text, Qt.white)
        self.PanelPalette.setBrush(QPalette.Window, QBrush(self.bggradient))

        self.checkPalette = QPalette()
        self.checkPalette.setColor(QPalette.Text, QColor(0, 0, 200))
        self.checkPalette.setColor(QPalette.Base, QColor(40, 40, 40))
        self.setPalette(self.PanelPalette)

        self.Tabs = QTabWidget()
        # self.Tabs.resizeEvent = self.moveBG
        self.HSpaceLayout = QHBoxLayout()
        self.HSpaceLayout.addSpacing(20)
        self.HSpaceLayout.addWidget(self.Tabs)
        self.HSpaceLayout.addSpacing(20)
        self.WindowLayout = QVBoxLayout()
        self.title = QLabel("Stats for " + username)
        self.WindowLayout.addWidget(self.title)
        self.WindowLayout.addSpacing(20)
        self.WindowLayout.addLayout(self.HSpaceLayout)
        self.WindowLayout.addSpacing(20)
        self.WindowWidget = QWidget()
        self.WindowWidget.setLayout(self.WindowLayout)

        self.setCentralWidget(self.WindowWidget)

        self.KDLayout = QVBoxLayout()
        self.KDWidget = QWidget()
        self.KDWidget.setLayout(self.KDLayout)
        self.Tabs.addTab(self.KDWidget, "Ranked &K/D per season")

        self.ELOLayout = QVBoxLayout()
        self.ELOWidget = QWidget()
        self.ELOWidget.setLayout(self.ELOLayout)
        self.Tabs.addTab(self.ELOWidget, "&MMR stats")

        self.OperatorTabs = QTabWidget()
        self.Tabs.addTab(self.OperatorTabs, "&Operator data")

        self.GenOpsWidget = QWidget()
        self.GenOpsLayout = QVBoxLayout()
        self.GenOpsWidget.setLayout(self.GenOpsLayout)
        self.OperatorTabs.addTab(self.GenOpsWidget, "General")


        platform = r6statsapi.Platform.uplay
        if userplatform == "XBOX":
            platform = r6statsapi.Platform.xbl
        elif userplatform == "PS4":
            platform = r6statsapi.Platform.psn

        self.SeasonalData = loop.run_until_complete(client.get_seasonal_stats(username, platform))
        self.OperatorData = loop.run_until_complete(client.get_operators_stats(username, platform))
        # print(self.SeasonalData.seasons)
        print(self.SeasonalData.seasons["crimson_heist"]["regions"]["emea"][0])
        # print(self.SeasonalData.seasons["crimson_heist"]["regions"]["emea"][0]["max_mmr"])
        # print(self.OperatorData.operators)
        self.genAllGraphs()
        self.genRankIcons()

        # self.resized.connect(lambda: self.moveBG())

    def genAllGraphs(self):
        self.genKDGraph()
        self.genELOGraph()

    def genKDGraph(self):
        self.KDGraph = QtCharts.QChartView()

        self.KDSeries = QtCharts.QLineSeries()
        KDList = []
        l = []
        seasons = len(self.SeasonalData.seasons)
        for i in range(seasons):
            l.append(None)
        for count, season in enumerate(self.SeasonalData.seasons):
            l[self.SeasonalData.seasons[season]["regions"]["emea"][0]["season_id"] - 6] = (self.SeasonalData.seasons[season]["name"])
            kills = self.SeasonalData.seasons[season]["regions"]["emea"][0]["kills"]
            if kills is None or kills <= 0:
                kills = 0
            deaths = self.SeasonalData.seasons[season]["regions"]["emea"][0]["deaths"]
            if deaths is None or deaths <= 0:
                deaths = 1
            self.KDSeries.append(float(seasons - count), (KD := kills/deaths))
            KDList.append(KD)

        KDList.sort(reverse=True)
        self.KDChart = QtCharts.QChart()
        self.KDChart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        self.KDChart.setTitle("Seasonal Ranked K/D")
        self.KDChart.addSeries(self.KDSeries)
        self.KDChart.legend().setVisible(False)

        X_axis = QtCharts.QBarCategoryAxis()
        X_axis.append(l)
        Y_axis = QtCharts.QValueAxis()
        Y_axis.setRange(0.0, float(KDList[0]))

        self.KDChart.addAxis(X_axis, Qt.AlignBottom)
        self.KDChart.addAxis(Y_axis, Qt.AlignLeft)
        self.KDGraph.setChart(self.KDChart)
        self.KDLayout.addWidget(self.KDGraph)

    def genELOGraph(self):
        self.ELOGraph = QtCharts.QChartView()

        self.ELOSet = QtCharts.QBarSet("Latest MMR")
        self.MaxELOSet = QtCharts.QBarSet("Max MMR")
        ELOList = []
        LifetimeMax = 0
        l = []

        seasons = len(self.SeasonalData.seasons)
        for i in range(seasons):
            l.append(None)
            ELOList.append([None, None])
        for count, season in enumerate(self.SeasonalData.seasons):
            l[self.SeasonalData.seasons[season]["regions"]["emea"][0]["season_id"] - 6] = (self.SeasonalData.seasons[season]["name"])
            ELO = self.SeasonalData.seasons[season]["regions"]["emea"][0]["mmr"]
            if ELO is None or ELO <= 0:
                ELO = 0
            maxELO = self.SeasonalData.seasons[season]["regions"]["emea"][0]["max_mmr"]
            if maxELO is None or maxELO <= 0:
                maxELO = 0
            if maxELO > LifetimeMax:
                LifetimeMax = maxELO
            ELOList[self.SeasonalData.seasons[season]["regions"]["emea"][0]["season_id"] - 6] = [ELO, maxELO]
        for i in ELOList:
            self.ELOSet.append(i[0])
            self.MaxELOSet.append(i[1])

        ELOList.sort(reverse=True)
        self.ELOChart = QtCharts.QChart()
        self.ELOChart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        self.ELOChart.setTitle("Seasonal Ranked MMR")

        self.ELOSeries = QtCharts.QBarSeries()
        self.ELOSeries.append(self.ELOSet)
        self.ELOSeries.append(self.MaxELOSet)
        self.ELOChart.addSeries(self.ELOSeries)

        X_axis = QtCharts.QBarCategoryAxis()
        X_axis.append(l)
        Y_axis = QtCharts.QValueAxis()
        Y_axis.setRange(0.0, float(LifetimeMax))

        self.ELOChart.addAxis(X_axis, Qt.AlignBottom)
        self.ELOChart.addAxis(Y_axis, Qt.AlignLeft)
        self.ELOGraph.setChart(self.ELOChart)
        self.ELOLayout.addWidget(self.ELOGraph)

    def genRankIcons(self):
        self.ELOGraph1 = QtCharts.QChartView()

        self.ELOSet1 = QtCharts.QBarSet("Latest MMR")
        self.MaxELOSet1 = QtCharts.QBarSet("Max MMR")
        ELOList = []
        LifetimeMax = 0
        l = []

        seasons = len(self.SeasonalData.seasons)

    def moveBG(self, event):
        # print("move grad")
        WidgetSize = event.size()
        WindowWidth = WidgetSize.width() + 58
        WindowHeight = WidgetSize.height() + 58
        self.bggradient.setCenter(WindowWidth + 50, WindowHeight + 194)  # keeps gradient in the same position relative to the window
        # self.bggradient.setColorAt(0.975, QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))


    # def resizeEvent(self, event=None):
    #     self.resized.emit()
    #     print(event)
    #     return super(main_panel, self).resizeEvent(event)

class Manager:
    def __init__(self):
        self.inputwin = un_input()
        self.inputwin.show()
    def ShowMain(self, username, platform):
        try:
            self.MainWin = main_panel(username, platform)
            self.MainWin.show()
            self.close()  # Since the function is being 'extracted' from the class, the context of 'self' is the login window
        except Exception as e:
            self.changeStatusBar(str(e), isError=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Passing the script to the Application
    # win = main_panel(globalfile.username)
    # win.show()
    windmanager = Manager()
    sys.exit(app.exec_())
