import sys, os
import random
from pathlib import Path
import r6statsapi
import asyncio
loop = asyncio.get_event_loop()
client = r6statsapi.Client("Token")
import globalfile
# TODO: move to pyside6 when 6.1 is released for graphs
# PySide is a huge library, so we import what we want explixitly
from PySide2.QtCore import (Qt, QRectF, QSize, QRect, QDateTime, QDir, Signal, QMetaObject)
from PySide2.QtGui import (QPalette, QColor, QRadialGradient, QLinearGradient, QConicalGradient,
                           QBrush, QGradient, QFont, QPixmap, QIcon)
from PySide2.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QStyleFactory, QWidget, QLineEdit, QPushButton, QApplication,
                               QDialog, QMainWindow, QLabel, QGroupBox, QDoubleSpinBox, QSpinBox, QDateTimeEdit, QComboBox,
                               QStatusBar, QMenuBar, QSizePolicy,
                               QDateEdit,
                               QCheckBox, QTextEdit, QTabWidget, QFileSystemModel, QTreeView, QScrollArea)
# from PySide2.QtCharts import (QLineSeries)
from PySide2.QtCharts import QtCharts

from PIL import Image, ImageOps, ImageDraw, ImageFont
import conversions

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

        # dir_path = Path(os.path.dirname(os.path.realpath(__file__)))  # NOTE: folder image resize script
        # path = dir_path / "src" / "operator icons"
        # oppath = dir_path / "src" / "operator icons" / "250"
        # for imgpath in os.listdir(path):
        #     if len(imgpath.split(".")) > 1:
        #         # print(imgpath)
        #         img = Image.open(path / imgpath)
        #         img = img.resize([250, 250], 3)  # 0.01 = 5x5
        #         img.save(oppath / imgpath)

        # logo = Image.open("src/logo/Snack-R6-logo.png")
        # logo = logo.resize([int(logo.size[0]*0.0625), int(logo.size[1]*0.0625)], 3) # 3 for bicubic filtering
        # logo.save("SL.png")
        # print(logo.size)

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
        self.BoldFont = QFont("Helvetica", 15, 70)
        self.SubSectionFont = QFont("Helvetica", 12, 70)
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

        # Creating a menu for a new user, then a button to bring us back to user input
        self.ToolBar = QMenuBar()
        self.setMenuBar(self.ToolBar)
        self.UserTools = self.ToolBar.addMenu("New user")
        self.ReGenAction = self.UserTools.addAction("Enter a new username...")
        # Connecting the menu button to return to the menu
        self.ReGenAction.triggered.connect(lambda: Manager.ShowNewInput(self))

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
        # Adding main tabs, and the TabWidgets to place inside the main tabs
        self.ELOTabs = QTabWidget()

        self.GenScroll = QScrollArea()
        self.GenScroll.setWidgetResizable(True)
        self.GenScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.GenScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.GenOpsScrollContainer = QWidget()
        self.GenScroll.setWidget(self.GenOpsScrollContainer)
        self.GenOpsLayout = QVBoxLayout(self.GenOpsScrollContainer)
        self.Tabs.addTab(self.GenScroll, "General")

        self.Tabs.addTab(self.ELOTabs, "&MMR stats")

        self.Tabs.addTab(self.KDWidget, "Ranked &K/D per season")
        self.OperatorTabs = QTabWidget()
        self.Tabs.addTab(self.OperatorTabs, "&Operator data")

        self.ELOLayout = QVBoxLayout()
        self.ELOWidget = QWidget()
        self.ELOWidget.setLayout(self.ELOLayout)
        self.BasicELOLayout = QVBoxLayout()

        self.BasicELOScroll = QScrollArea()

        self.BasicELOScroll.setWidgetResizable(True)
        self.BasicELOScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.BasicELOScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.BasicELOScrollContainer = QWidget()
        self.BasicELOScroll.setWidget(self.BasicELOScrollContainer)

        self.ELOTabs.addTab(self.BasicELOScroll, "basic MMR stats")
        self.ELOTabs.addTab(self.ELOWidget, "MMR chart")


        platform = r6statsapi.Platform.uplay
        if userplatform == "XBOX":
            platform = r6statsapi.Platform.xbl
        elif userplatform == "PS4":
            platform = r6statsapi.Platform.psn

        self.GeneralData = loop.run_until_complete(client.get_generic_stats(username, platform))
        self.SeasonalData = loop.run_until_complete(client.get_seasonal_stats(username, platform))
        self.OperatorData = loop.run_until_complete(client.get_operators_stats(username, platform))
        self.WeaponData = loop.run_until_complete(client.get_weapon_stats(username, platform))
        # print(self.WeaponData.weapons)
        for i in self.WeaponData.weapons:
            print(i)
        # print(self.SeasonalData.seasons)
        # print(self.SeasonalData.seasons["crimson_heist"]["regions"]["emea"][0])
        # print(self.SeasonalData.seasons["crimson_heist"]["regions"]["emea"][0]["max_mmr"])
        # print(self.OperatorData.operators)
        self.genAllGraphs()
        self.genRankIcons()
        self.genGeneralData()

    def genAllGraphs(self):
        self.genKDGraph()
        self.genELOGraph()

    def genKDGraph(self):
        self.KDGraph = QtCharts.QChartView()

        self.KDSeries = QtCharts.QLineSeries()
        KDList = []
        SeasonNames = []
        seasons = len(self.SeasonalData.seasons)
        for i in range(seasons):
            SeasonNames.append(None)
        for count, season in enumerate(self.SeasonalData.seasons):
            SeasonNames[self.SeasonalData.seasons[season]["regions"]["emea"][0]["season_id"] - 6] = (self.SeasonalData.seasons[season]["name"])
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
        X_axis.append(SeasonNames)
        Y_axis = QtCharts.QValueAxis()
        Y_axis.setRange(0.0, float(KDList[0]))

        self.KDChart.addAxis(X_axis, Qt.AlignBottom)
        self.KDChart.addAxis(Y_axis, Qt.AlignLeft)
        self.KDGraph.setChart(self.KDChart)
        self.KDLayout.addWidget(self.KDGraph)

    def genELOGraph(self):
        self.ELOGraph = QtCharts.QChartView()
        self.ELOSet = QtCharts.QBarSet("Latest MMR")
        self.ELOSet.setBrush(QBrush(QLinearGradient().MagicRay))
        self.MaxELOSet = QtCharts.QBarSet("Max MMR")
        self.MaxELOSet.setBrush(QBrush(QLinearGradient().GrownEarly))
        ELOList = []
        LifetimeMax = 0
        SeasonNames = []

        seasons = len(self.SeasonalData.seasons)
        for i in range(seasons):
            SeasonNames.append(None)
            ELOList.append([None, None])
        for count, season in enumerate(self.SeasonalData.seasons):
            SeasonNames[self.SeasonalData.seasons[season]["regions"]["emea"][0]["season_id"] - 6] = (self.SeasonalData.seasons[season]["name"])
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
        self.ELOChart.setTitle("Seasonal Ranked MMR (No max MMR means season ended as unranked)")

        self.ELOSeries = QtCharts.QBarSeries()
        self.ELOSeries.append(self.ELOSet)
        self.ELOSeries.append(self.MaxELOSet)
        self.ELOChart.addSeries(self.ELOSeries)

        X_axis = QtCharts.QBarCategoryAxis()
        X_axis.append(SeasonNames)
        Y_axis = QtCharts.QValueAxis()
        Y_axis.setRange(0.0, float(LifetimeMax))

        self.ELOChart.addAxis(X_axis, Qt.AlignBottom)
        self.ELOChart.addAxis(Y_axis, Qt.AlignLeft)
        self.ELOGraph.setChart(self.ELOChart)
        self.ELOLayout.addWidget(self.ELOGraph)

    def genRankIcons(self):
        ELOList = []
        LifetimeMax = 0
        LifetimeMaxRank = ""
        SeasonNames = []

        seasons = len(self.SeasonalData.seasons)
        for i in range(seasons):
            SeasonNames.append(None)
            ELOList.append([None, None])
        for count, season in enumerate(self.SeasonalData.seasons):
            SeasonNames[self.SeasonalData.seasons[season]["regions"]["emea"][0]["season_id"] - 6] = (self.SeasonalData.seasons[season]["name"])
            ELORank = self.SeasonalData.seasons[season]["regions"]["emea"][0]["rank_text"]

            maxELORank = self.SeasonalData.seasons[season]["regions"]["emea"][0]["max_rank_text"]

            maxELO = self.SeasonalData.seasons[season]["regions"]["emea"][0]["max_mmr"]
            ChampRank = self.SeasonalData.seasons[season]["regions"]["emea"][0]["champions_rank_position"]
            if maxELO > LifetimeMax:
                LifetimeMax = maxELO
                LifetimeMaxRank = maxELORank
            ELOList[self.SeasonalData.seasons[season]["regions"]["emea"][0]["season_id"] - 6] = [ELORank, maxELORank, ChampRank]

        rank_path = Path(os.path.dirname(os.path.realpath(__file__)))
        rank_path = rank_path / "src" / "ranks" / "100"

        RankList = conversions.rank_roman_to_int(LifetimeMaxRank)
        RankName = RankList[0]
        if len(RankList) > 1:
            RankName += "-" + str(RankList[1])
        RankName += ".png"
        self.MaxRankImage = QLabel()
        self.MaxRankImage.setAlignment(Qt.AlignCenter)
        # self.MaxRankImage.setMinimumHeight(70)
        self.MaxRankImage.setPixmap(QPixmap(str(rank_path / RankName)))

        # Setting up the highest rank GroupBox
        self.GeneralBasicELO = QGroupBox("General")
        self.MaxRankText = QLabel("Highest rank: ")
        self.MaxRankText.setFont(self.BoldFont)
        self.MaxRankText.setAlignment(Qt.AlignCenter)
        self.MaxRankLayout = QHBoxLayout()
        self.MaxRankLayout.addWidget(self.MaxRankText)
        self.MaxRankLayout.addWidget(self.MaxRankImage)
        self.GeneralBasicELO.setLayout(self.MaxRankLayout)
        # adding GroupBoxes and Layout
        self.BasicELOSeasons = QGroupBox("Season")
        self.BasicELORanks = QGroupBox("Rank")
        self.BasicELOMaxRanks = QGroupBox("Max Rank")
        self.SeasonLabels = QVBoxLayout()
        self.RankLabels = QVBoxLayout()
        self.MaxRankLabels = QVBoxLayout()
        # Adding the season names for the left GroupBox
        # (Minimum height to ensure the labels are correctly aligned and spaced
        for season in SeasonNames:
            SeasonLabel = QLabel(season)
            SeasonLabel.setMinimumHeight(70)
            SeasonLabel.setAlignment(Qt.AlignVCenter)
            # Inserting at 0 to add the newest season at the top
            self.SeasonLabels.insertWidget(0, SeasonLabel)
        # Setting the season names to the GroupBox
        self.BasicELOSeasons.setLayout(self.SeasonLabels)
        # Making a layout to add all widgets that is *parented* to the ScrollArea
        self.BasicELOLabels = QVBoxLayout(self.BasicELOScrollContainer)
        self.BasicELOLabels.addWidget(self.GeneralBasicELO)
        self.BasicSeasonalELOLabels = QHBoxLayout()
        self.BasicELOLabels.addLayout(self.BasicSeasonalELOLabels)
        self.BasicSeasonalELOLabels.addWidget(self.BasicELOSeasons)
        # Changing the path to use smaller rank icons
        rank_path = Path(os.path.dirname(os.path.realpath(__file__)))
        rank_path = rank_path / "src" / "ranks" / "55"
        # TODO: Convert logos etc into qrc for ease of distribution
        # Using the rank from the API to select the correct icon,
        # And use it.
        for count, ELOSet in enumerate(ELOList):
            # print(count)
            # print(len(ELOList))
            RankList = conversions.rank_roman_to_int(ELOSet[0])
            RankName = RankList[0]
            RankLabel = QLabel()
            RankLabel.setAlignment(Qt.AlignCenter)
            RankLabel.setMinimumHeight(70)

            if len(RankList) > 1:
                RankName += "-" + str(RankList[1])
            RankName += ".png"
            RankLabel.setPixmap(QPixmap(str(rank_path / RankName)))

            # TODO: logic seems incorrect but works, if the last season does *not* show number for champions OR better logic is found, edit it here.
            if RankList[0] == "champions" and count + 1 == len(ELOList):
                RankLabelLayout = QHBoxLayout()
                RankLabelLayout.addWidget(RankLabel)
                ChampRankLabel = QLabel("#{}".format(str(ChampRank)))
                # ChampRankLabel.setAlignment(Qt.AlignCenter)
                RankLabelLayout.addWidget(ChampRankLabel)
                RankLabelLayout.setAlignment(Qt.AlignCenter)
                self.RankLabels.insertLayout(0, RankLabelLayout)
            else:
                self.RankLabels.insertWidget(0, RankLabel)
            # else:
            #     RankLabel.setText("Champion")
            #     RankLabel.setAlignment(Qt.AlignCenter)

            MaxRankList = conversions.rank_roman_to_int(ELOSet[1])
            MaxRankName = MaxRankList[0]
            MaxRankLabel = QLabel()
            MaxRankLabel.setAlignment(Qt.AlignCenter)
            MaxRankLabel.setMinimumHeight(70)
            if len(MaxRankList) > 1:
                MaxRankName += "-" + str(MaxRankList[1])
            MaxRankName += ".png"
            MaxRankLabel.setPixmap(QPixmap(str(rank_path / MaxRankName)))
            # else:
            #     MaxRankLabel.setText("Champion")
            #     MaxRankLabel.setAlignment(Qt.AlignCenter)
            self.MaxRankLabels.insertWidget(0, MaxRankLabel)

        self.BasicELORanks.setLayout(self.RankLabels)
        self.BasicELOMaxRanks.setLayout(self.MaxRankLabels)
        self.BasicSeasonalELOLabels.addWidget(self.BasicELORanks)
        self.BasicSeasonalELOLabels.addWidget(self.BasicELOMaxRanks)
        self.BasicELOLayout.addLayout(self.BasicELOLabels)

    def genGeneralData(self):
        # Build a dictionary that is assigned the indexes of all entries, and their corresponding operator names for easy searching
        OperatorIndexDict = {}
        for count, i in enumerate(self.OperatorData.operators):
            OperatorIndexDict[i["name"]] = count
        # print(OperatorIndexDict)
        # print(self.OperatorData.operators[OperatorIndexDict["Aruni"]])
        # print(self.OperatorData.operators[OperatorIndexDict["Mute"]])
        mostUsedDefender = ["", 0]
        mostUsedAttacker = ["", 0]
        mostUsedAttackers = []
        mostUsedDefenders = []


        # Bar Chart variables
        self.TopOpsChartView = QtCharts.QChartView()
        self.TopOpsChart = QtCharts.QChart()
        self.TopOpsChart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        self.TopOpsKDSet = QtCharts.QBarSet("K/D")
        self.TopOpsKDSet.setBrush(QBrush(QLinearGradient().MagicRay))
        self.TopOpsWLSet = QtCharts.QBarSet("W/L")
        self.TopOpsWLSet.setBrush(QBrush(QLinearGradient().GrownEarly))  # TODO: QLinearGradient().BlackSea, QLinearGradient().MagicRay

        self.TopFragOpsChartView = QtCharts.QChartView()
        self.TopFragOpsChart = QtCharts.QChart()
        self.TopFragOpsChart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        self.TopFragOpsKDSet = QtCharts.QBarSet("K/D")
        self.TopFragOpsKDSet.setBrush(QBrush(QLinearGradient().MagicRay))
        self.TopFragOpsWLSet = QtCharts.QBarSet("W/L")
        self.TopFragOpsWLSet.setBrush(QBrush(QLinearGradient().GrownEarly))

        OperatorList = []
        TopOps = {}
        TopFrags = {}
        MaxWLChartVal = 0.0

        for i in(self.OperatorData.operators):
            # Iterating to find the most used operators
            uses = i["wins"] + i["losses"]
            if i["role"] == "Attacker":
                if uses > mostUsedAttacker[1]:
                    mostUsedAttacker = [i["name"], uses]
                    mostUsedAttackers.insert(0, [i["name"], uses])
            else:
                if uses > mostUsedAttacker[1]:
                    mostUsedDefender = [i["name"], uses]
                    mostUsedDefenders.insert(0, [i["name"], uses])

            # Adding Chart Data
            # self.TopOpsKDSet.append(i["kd"])
            # self.TopOpsWLSet.append(i["wl"])
            if i["kd"] > MaxWLChartVal:
                MaxWLChartVal = i["kd"]
            if i["wl"] > MaxWLChartVal:
                MaxWLChartVal = i["wl"]
            TopOps[(i["name"], i["kd"])] = [i["wl"]]
            TopFrags[(i["name"], i["wl"])] = [i["kd"]]
            OperatorList.append(i["name"])

        # This reorders the dictionary to be ordered from highest WL to lowest, with keys of the operator name and KD
        TopOps = {key: value for key, value in sorted(TopOps.items(), key=lambda item: item[1], reverse=True)}
        TopFrags = {key: value for key, value in sorted(TopFrags.items(), key=lambda item: item[1], reverse=True)}
        TopOpNames = []
        TopFragOpNames = []
        # print(TopOps)
        for i in list(TopOps)[0:15]:  # Get first 5 items: 5 highest win/losses
            TopOpNames.append(i[0])
            self.TopOpsKDSet.append(i[1])
            self.TopOpsWLSet.append(TopOps[i])

        MaxKDChartVal = 0.0
        for i in list(TopFrags)[0:15]:  # Get first 5 items: 5 highest win/losses
            TopFragOpNames.append(i[0])
            self.TopFragOpsKDSet.append(TopFrags[i])
            self.TopFragOpsWLSet.append(i[1])
            if TopFrags[i][0] > MaxKDChartVal:
                MaxKDChartVal = TopFrags[i][0]
            if i[1] > MaxKDChartVal:
                MaxKDChartVal = i[1]

        # Generating the GroupBox for most used operators
        self.GeneralDataGroup = QGroupBox("General")
        self.GenGroupOpsLabel = QLabel("Top operators: ")
        self.GenGroupOpsLabel.setFont(self.SubSectionFont)
        self.MostUsedOpsLayout = QHBoxLayout()
        self.MostUsedAttackerLabel = QLabel("Attackers: ")
        self.MostUsedAttackerLabel.setAlignment(Qt.AlignCenter)
        self.MostUsedAttackerLabel.setFont(self.BoldFont)
        self.MostUsedDefenderLabel = QLabel("Defenders: ")
        self.MostUsedDefenderLabel.setAlignment(Qt.AlignCenter)
        self.MostUsedDefenderLabel.setFont(self.BoldFont)
        self.MostUsedOpsLayout.addWidget(self.MostUsedAttackerLabel)
        self.MostUsedOpsLayout.addWidget(self.MostUsedDefenderLabel)

        large_operator_icon_path = Path(os.path.dirname(os.path.realpath(__file__))) / "src" / "operator icons" / "100"
        # Adding the top 3 attacker and defender icons to the GroupBox
        for i in range(3):
            AttackerIcon = QLabel()
            DefenderIcon = QLabel()
            AttackerIcon.setAlignment(Qt.AlignCenter)
            DefenderIcon.setAlignment(Qt.AlignCenter)
            AttackerIcon.setPixmap(str(large_operator_icon_path / mostUsedAttackers[i][0].lower()))
            DefenderIcon.setPixmap(str(large_operator_icon_path / mostUsedDefenders[i][0].lower()))
            self.MostUsedOpsLayout.insertWidget(i+1, AttackerIcon)
            self.MostUsedOpsLayout.addWidget(DefenderIcon)

        self.GeneralGroupLayout = QVBoxLayout()
        self.GeneralGroupLayout.addWidget(self.GenGroupOpsLabel)
        self.GeneralGroupLayout.addLayout(self.MostUsedOpsLayout)

        WeaponCount = 0
        AvgHeadshotPercentage = 0.0
        TopWeapon = ["", 0.0, 0]  # Gun name, K/D (will require 100 or more kills to count)
        for i in self.WeaponData.weapons:
            # Adding data for headshot % average
            if i["headshot_percentage"] != 0:
                WeaponCount += 1  # Total is needed, so enumerate would not help much here
                AvgHeadshotPercentage += i["headshot_percentage"]
            # Adding data for top weapon
            if i["kills"] >= 100:
                if i["kd"] > TopWeapon[1]:
                    TopWeapon = [i["weapon"], round(i["kd"], 5), i["kills"]]
        if WeaponCount != 0:
            AvgHeadshotPercentage /= WeaponCount
            AvgHeadshotPercentage = str(round(AvgHeadshotPercentage, 5))
            AvgHeadshotPercentage += "%"
        else:
            AvgHeadshotPercentage = "N/A"

        self.HeadshotPercentageLayout = QHBoxLayout()
        self.HeadshotCategoryLabel = QLabel("Headshot percentage: ")
        self.HeadshotValueLabel = QLabel(str(AvgHeadshotPercentage))
        self.HeadshotCategoryLabel.setFont(self.SubSectionFont)
        # self.HeadshotValueLabel.setFont(self.BoldFont)
        self.HeadshotPercentageLayout.addWidget(self.HeadshotCategoryLabel)
        self.HeadshotPercentageLayout.addWidget(self.HeadshotValueLabel)
        self.GeneralGroupLayout.addLayout(self.HeadshotPercentageLayout)

        self.TopWeaponLayout = QHBoxLayout()
        self.TopWeaponCategoryLabel = QLabel("Top Weapon: ")
        self.TopWeaponCategoryLabel.setFont(self.SubSectionFont)
        if TopWeapon[0] != "":
            self.TopWeaponValueLabel = QLabel("{0}, {1}K/D ({2} kills)".format(TopWeapon[0], TopWeapon[1], TopWeapon[2]))
        else:
            self.TopWeaponValueLabel = QLabel("Not enough data.")
        self.TopWeaponLayout.addWidget(self.TopWeaponCategoryLabel)
        self.TopWeaponLayout.addWidget(self.TopWeaponValueLabel)
        self.GeneralGroupLayout.addLayout(self.TopWeaponLayout)

        self.GeneralDataGroup.setLayout(self.GeneralGroupLayout)

        self.GenOpsLayout.addWidget(self.GeneralDataGroup)

        # Generating a KD and Win/Loss bar chart for top winning ops

        X_axis = QtCharts.QBarCategoryAxis()
        X_axis.append(TopOpNames)
        Y_axis = QtCharts.QValueAxis()
        Y_axis.setRange(0.0, float(MaxWLChartVal))

        self.TopOpsChart.addAxis(X_axis, Qt.AlignBottom)
        self.TopOpsChart.addAxis(Y_axis, Qt.AlignLeft)

        self.TopOpsBarSeries = QtCharts.QBarSeries()
        self.TopOpsBarSeries.append(self.TopOpsWLSet)
        self.TopOpsBarSeries.append(self.TopOpsKDSet)
        self.TopOpsChart.addSeries(self.TopOpsBarSeries)
        self.TopOpsChartView.setChart(self.TopOpsChart)
        self.TopOpsChartView.setMinimumHeight(400)  # Stopping the graph from being resized to be unreadable
        # self.TopOpsChartView.setMaximumHeight(400)  # Use if the graph reacts badly to maximising after another graph has been added
        self.TopOpsGroup = QGroupBox("Top 15 operators by Win/Loss")
        self.TopOpsChartLayout = QVBoxLayout()
        self.TopOpsChartLayout.addWidget(self.TopOpsChartView)
        self.TopOpsGroup.setLayout(self.TopOpsChartLayout)
        self.GenOpsLayout.addWidget(self.TopOpsGroup)

        # Generating a KD and Win/Loss bar chart for top fragging ops

        Frag_X_axis = QtCharts.QBarCategoryAxis()
        Frag_X_axis.append(TopFragOpNames)
        Frag_Y_axis = QtCharts.QValueAxis()
        Frag_Y_axis.setRange(0.0, float(MaxKDChartVal))

        self.TopFragOpsChart.addAxis(Frag_X_axis, Qt.AlignBottom)
        self.TopFragOpsChart.addAxis(Frag_Y_axis, Qt.AlignLeft)

        self.TopFragOpsBarSeries = QtCharts.QBarSeries()
        self.TopFragOpsBarSeries.append(self.TopFragOpsKDSet)
        self.TopFragOpsBarSeries.append(self.TopFragOpsWLSet)
        self.TopFragOpsChart.addSeries(self.TopFragOpsBarSeries)
        self.TopFragOpsChartView.setChart(self.TopFragOpsChart)
        self.TopFragOpsChartView.setMinimumHeight(400)  # Stopping the graph from being resized to be unreadable
        # self.TopOpsChartView.setMaximumHeight(400)  # Use if the graph reacts badly to maximising after another graph has been added
        self.TopFragOpsGroup = QGroupBox("Top 15 operators by K/D")
        self.TopFragOpsChartLayout = QVBoxLayout()
        self.TopFragOpsChartLayout.addWidget(self.TopFragOpsChartView)
        self.TopFragOpsGroup.setLayout(self.TopFragOpsChartLayout)
        self.GenOpsLayout.addWidget(self.TopFragOpsGroup)


    # def moveBG(self, event):
    #     # print("move grad")
    #     WidgetSize = event.size()
    #     WindowWidth = WidgetSize.width() + 58
    #     WindowHeight = WidgetSize.height() + 58
    #     self.bggradient.setCenter(WindowWidth + 50, WindowHeight + 194)  # keeps gradient in the same position relative to the window
    #     # self.bggradient.setColorAt(0.975, QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))


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

    def ShowNewInput(self):
        self.inputwin = un_input()
        self.inputwin.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Passing the script to the Application
    # win = main_panel(globalfile.username)
    # win.show()
    windmanager = Manager()
    sys.exit(app.exec_())
