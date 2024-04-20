from PyQt6 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
import networkx as nx
import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import settings
from parser import parse, write_to_test, parse_generations
from executing import runcmd


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1265, 780)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.inputData = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.inputData.setGeometry(QtCore.QRect(30, 100, 221, 511))
        self.inputData.setPlainText("")
        self.inputData.setObjectName("inputData")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 80, 91, 16))
        self.label.setObjectName("label")
        self.undirectedButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.undirectedButton.setGeometry(QtCore.QRect(30, 30, 94, 34))
        self.undirectedButton.setObjectName("undirectedButton")
        self.directedButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.directedButton.setGeometry(QtCore.QRect(160, 30, 94, 34))
        self.directedButton.setObjectName("directedButton")
        self.exportButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.exportButton.setGeometry(QtCore.QRect(1160, 690, 91, 34))
        self.exportButton.setObjectName("exportButton")
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(290, 30, 851, 691))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.graphArea = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.graphArea.setContentsMargins(0, 0, 0, 0)
        self.graphArea.setObjectName("graphArea")
        self.TerminalLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.TerminalLabel.setGeometry(QtCore.QRect(40, 610, 91, 16))
        self.TerminalLabel.setObjectName("TerminalLabel")
        self.TerminalTextEdit = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.TerminalTextEdit.setGeometry(QtCore.QRect(30, 630, 221, 87))
        self.TerminalTextEdit.setObjectName("TerminalTextEdit")
        self.Generation = QtWidgets.QSpinBox(parent=self.centralwidget)
        self.Generation.setGeometry(QtCore.QRect(1160, 350, 91, 21))
        self.Generation.setObjectName("Generation")
        self.GenerationLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.GenerationLabel.setGeometry(QtCore.QRect(1170, 330, 55, 16))
        self.GenerationLabel.setObjectName("GenerationLabel")
        self.AutoIncreaseButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.AutoIncreaseButton.setGeometry(QtCore.QRect(1160, 400, 93, 28))
        self.AutoIncreaseButton.setObjectName("AutoIncreaseButton")
        self.drawButttn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.drawButttn.setGeometry(QtCore.QRect(1160, 640, 93, 28))
        self.drawButttn.setObjectName("drawButttn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1265, 26))
        self.menubar.setObjectName("menubar")
        self.menuVisual_Graph_Tool = QtWidgets.QMenu(parent=self.menubar)
        self.menuVisual_Graph_Tool.setObjectName("menuVisual_Graph_Tool")
        self.fileMenu = QtWidgets.QMenu(parent=self.menubar)
        self.fileMenu.setObjectName("fileMenu")
        self.editMenu = QtWidgets.QMenu(parent=self.menubar)
        self.editMenu.setObjectName("editMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuVisual_Graph_Tool.menuAction())
        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.editMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1271, 21))
        self.menubar.setObjectName("menubar")
        self.menuVisual_Graph_Tool = QtWidgets.QMenu(parent=self.menubar)
        self.menuVisual_Graph_Tool.setObjectName("menuVisual_Graph_Tool")
        self.fileMenu = QtWidgets.QMenu(parent=self.menubar)
        self.fileMenu.setObjectName("fileMenu")
        self.editMenu = QtWidgets.QMenu(parent=self.menubar)
        self.editMenu.setObjectName("editMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuVisual_Graph_Tool.menuAction())
        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.editMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # add canvas
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.graphArea.addWidget(self.canvas)

        # draw clicked.
        self.drawButttn.clicked.connect(self.submitDraw)

        # draw graph follow gen
        self.AutoIncreaseButton.clicked.connect(self.autoDrawGraphByGen)

        # generation spinbox
        self.Generation.valueChanged.connect(self.drawGraphByGen)

    def submitDraw(self):
        rdata = self.inputData.toPlainText()
        self.draw_weighted_graph_text(rdata)

    def autoDrawGraphByGen(self):
        for count in range(1, 16):
            self.Generation.setValue(count)
            self.Generation.valueChanged.emit(count)
            time.sleep(5)

    def drawGraphByGen(self, count):

        count = int(self.Generation.value())

        rdata = self.inputData.toPlainText()
        grapharray = rdata.split("\n")
        edges = []
        terminal = []
        for i in range(len(grapharray)):
            edges.append(grapharray[i].split(" "))
        terminalData = self.TerminalTextEdit.toPlainText()
        terminal = terminalData.split(" ")
        write_to_test(parse(edges, terminal))
        # print(runcmd(settings.GA_command))
        # print(runcmd("ls"))

        generations = parse_generations(edges)
        generations.pop(0)
        self.highline_road(str(generations[count]), rdata)

    # Highline road
    def highline_road(self, gen, rdata):
        print("Called highline_road")
        self.figure.clf()
        # Create a new graph
        G = nx.Graph()
        ecount = 0  # Check selected gen
        for line in rdata.split("\n"):
            if line.strip():
                data = line.strip().split()
                if gen[ecount] == "1":
                    G.add_edge(data[0], data[1], color="red", weight=int(data[2]))
                else:
                    G.add_edge(data[0], data[1], color="black", weight=int(data[2]))

                print(f"{gen[ecount]} => {line}")

                ecount += 1

        colors = nx.get_edge_attributes(G, "color").values()
        weights = nx.get_edge_attributes(G, "weight").values()

        # Draw the graph
        pos = nx.spring_layout(G)  # Compute positions for drawing

        options = {
            "with_labels": True,
            "font_size": 15,
            "node_size": 500,
            "node_color": "white",
            "edge_color": colors,
            "linewidths": list(weights),
            "width": 3,
        }
        pos = nx.spring_layout(G, seed=1)
        nx.draw(G, pos, **options)
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="blue")

        self.canvas.draw()

    def draw_weighted_graph_text(self, rdata):

        self.figure.clf()
        # Create a new graph
        G = nx.Graph()

        for line in rdata.split("\n"):
            if line.strip():
                data = line.strip().split()
                source = int(data[0])
                target = int(data[1])
                weight = int(data[2])
                G.add_edge(source, target, weight=weight)

        # Draw the graph
        pos = nx.spring_layout(G)  # Compute positions for drawing

        options = {
            "with_labels": True,
            "font_size": 15,
            "node_size": 500,
            "node_color": "white",
            # "edgecolors": "black",
            "linewidths": 3,
            "width": 3,
        }
        pos = nx.spring_layout(G, seed=1)
        nx.draw(G, pos, edge_color="black", **options)
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="blue")

        self.canvas.draw()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Graph Data:"))
        self.undirectedButton.setText(_translate("MainWindow", "Undirected"))
        self.directedButton.setText(_translate("MainWindow", "Directed"))
        self.exportButton.setText(_translate("MainWindow", "Export"))
        self.TerminalLabel.setText(_translate("MainWindow", "Terminal set"))
        self.GenerationLabel.setText(_translate("MainWindow", "Generation"))
        self.AutoIncreaseButton.setText(_translate("MainWindow", "Auto"))
        self.drawButttn.setText(_translate("MainWindow", "Draw"))
        self.menuVisual_Graph_Tool.setTitle(
            _translate("MainWindow", "Visual Graph Tool")
        )
        self.fileMenu.setTitle(_translate("MainWindow", "File"))
        self.editMenu.setTitle(_translate("MainWindow", "Edit"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
