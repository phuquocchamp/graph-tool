from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog
import matplotlib.pyplot as plt
import networkx as nx
import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import settings
from parser import parse, write_to_test, parse_generations
from executing import runcmd


class Ui_MainWindow(object):
    gstyle = 0
    rdata = ""
    G = nx.Graph()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1265, 777)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.inputData = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.inputData.setGeometry(QtCore.QRect(20, 80, 211, 521))
        self.inputData.setPlainText("")
        self.inputData.setObjectName("inputData")
        self.graphDataLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.graphDataLabel.setGeometry(QtCore.QRect(20, 60, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.graphDataLabel.setFont(font)
        self.graphDataLabel.setObjectName("graphDataLabel")
        self.undirectedButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.undirectedButton.setGeometry(QtCore.QRect(20, 10, 94, 34))
        self.undirectedButton.setObjectName("undirectedButton")
        self.directedButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.directedButton.setGeometry(QtCore.QRect(140, 10, 94, 34))
        self.directedButton.setObjectName("directedButton")
        self.exportButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.exportButton.setGeometry(QtCore.QRect(1150, 690, 91, 34))
        self.exportButton.setObjectName("exportButton")
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(250, 10, 881, 721))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.graphArea = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.graphArea.setContentsMargins(0, 0, 0, 0)
        self.graphArea.setObjectName("graphArea")
        self.terminalLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.terminalLabel.setGeometry(QtCore.QRect(20, 620, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.terminalLabel.setFont(font)
        self.terminalLabel.setObjectName("terminalLabel")
        self.terminalData = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.terminalData.setGeometry(QtCore.QRect(20, 640, 211, 87))
        self.terminalData.setObjectName("terminalData")
        self.generationSpinBox = QtWidgets.QSpinBox(parent=self.centralwidget)
        self.generationSpinBox.setGeometry(QtCore.QRect(1150, 560, 91, 21))
        self.generationSpinBox.setObjectName("generationSpinBox")
        self.generationLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.generationLabel.setGeometry(QtCore.QRect(1150, 540, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.generationLabel.setFont(font)
        self.generationLabel.setObjectName("generationLabel")
        self.autoGenBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.autoGenBtn.setGeometry(QtCore.QRect(1150, 600, 93, 28))
        self.autoGenBtn.setObjectName("autoGenBtn")
        self.drawButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.drawButton.setGeometry(QtCore.QRect(1150, 650, 93, 28))
        self.drawButton.setObjectName("drawButton")
        self.styleGraph = QtWidgets.QComboBox(parent=self.centralwidget)
        self.styleGraph.setGeometry(QtCore.QRect(1150, 500, 91, 22))
        self.styleGraph.setObjectName("styleGraph")
        self.styleGraph.addItem("")
        self.styleGraph.addItem("")
        self.styleGraph.addItem("")
        self.styleGraph.addItem("")
        self.styleGraph.addItem("")
        self.styleGraph.addItem("")
        self.styleGraph.addItem("")
        self.styleGraph.addItem("")
        self.styleGraphLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.styleGraphLabel.setGeometry(QtCore.QRect(1150, 470, 91, 20))
        self.styleGraphLabel.setObjectName("styleGraphLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1265, 21))
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

        # -------------------- Logic Function ------------------- #

        # add canvas
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.graphArea.addWidget(self.canvas)

        # directed Graph
        self.directedButton.clicked.connect(self.setDirectedGraph)

        # undirected Graph
        self.undirectedButton.clicked.connect(self.setUnDirectedGraph)

        # draw clicked.
        self.drawButton.clicked.connect(self.submitDraw)

        # draw graph follow gen
        self.autoGenBtn.clicked.connect(self.autoDrawGraphByGen)

        # generation spinbox
        self.generationSpinBox.valueChanged.connect(self.drawGraphByGen)

        # style Graph
        self.styleGraph.activated.connect(self.setGraphStyle)

        # export Graph
        self.exportButton.clicked.connect(self.exportGraphFile)

    def setDirectedGraph(self):
        self.directedButton.setStyleSheet("background-color: #576ee7")
        self.undirectedButton.setStyleSheet("background-color: white")
        self.G = nx.DiGraph()

    def setUnDirectedGraph(self):
        self.undirectedButton.setStyleSheet("background-color: #576ee7")
        self.directedButton.setStyleSheet("background-color: white")
        self.G = nx.Graph()

    def setGraphStyle(self, index):
        self.gstyle = index + 1
        print("Selected Graph Style: => ", self.gstyle)
        self.drawGraph(self.rdata)

    def submitDraw(self):
        self.rdata = self.inputData.toPlainText()
        self.drawGraph(self.rdata)

    def autoDrawGraphByGen(self):
        for count in range(1, 16):
            self.generationSpinBox.setValue(count)
            self.generationSpinBox.valueChanged.emit(count)

    def drawGraphByGen(self, count):

        count = int(self.generationSpinBox.value())

        # rdata = self.inputData.toPlainText()
        grapharray = self.rdata.split("\n")
        edges = []
        terminal = []
        for i in range(len(grapharray)):
            edges.append(grapharray[i].split(" "))
        terminalData = self.terminalData.toPlainText()
        terminal = terminalData.split(" ")
        write_to_test(parse(edges, terminal))
        # print(runcmd(settings.GA_command))
        # print(runcmd("ls"))

        generations = parse_generations(edges)
        generations.pop(0)
        self.highline_road(str(generations[count]), self.rdata)

    # Highline road
    def highline_road(self, gen, rdata):
        print("Highlining graph with style: => ", self.gstyle)
        print("Called highline_road")
        self.figure.clf()
        # # Create a new graph
        # G = nx.Graph()
        ecount = 0  # Check selected gen
        for line in self.rdata.split("\n"):
            if line.strip():
                data = line.strip().split()
                if gen[ecount] == "1":
                    self.G.add_edge(data[0], data[1], color="red", weight=int(data[2]))
                else:
                    self.G.add_edge(
                        data[0], data[1], color="black", weight=int(data[2])
                    )

                # print(f"{gen[ecount]} => {line}")

                ecount += 1

        colors = nx.get_edge_attributes(self.G, "color").values()
        weights = nx.get_edge_attributes(self.G, "weight").values()

        # Draw the graph
        pos = nx.spring_layout(self.G)  # Compute positions for drawing

        options = {
            "with_labels": True,
            "font_size": 15,
            "node_size": 500,
            "node_color": "gray",
            "edge_color": colors,
            "linewidths": list(weights),
            "width": 3,
        }
        pos = nx.spring_layout(self.G, seed=self.gstyle)
        nx.draw(self.G, pos, **options)
        edge_labels = nx.get_edge_attributes(self.G, "weight")
        nx.draw_networkx_edge_labels(
            self.G, pos, edge_labels=edge_labels, font_color="blue"
        )

        self.canvas.draw()

    def drawGraph(self, rdata):
        print("Drawing graph with style: => ", self.gstyle)

        self.figure.clf()
        # # Create a new graph

        for line in self.rdata.split("\n"):
            if line.strip():
                data = line.strip().split()
                self.G.add_edge(data[0], data[1], color="red", weight=int(data[2]))

        # Draw the graph
        pos = nx.spring_layout(self.G)  # Compute positions for drawing

        options = {
            "with_labels": True,
            "font_size": 15,
            "node_size": 500,
            "node_color": "gray",
            # "edgecolors": "black",
            "linewidths": 3,
            "width": 3,
        }
        pos = nx.spring_layout(self.G, seed=self.gstyle)
        nx.draw(self.G, pos, edge_color="black", **options)
        edge_labels = nx.get_edge_attributes(self.G, "weight")
        nx.draw_networkx_edge_labels(
            self.G, pos, edge_labels=edge_labels, font_color="blue"
        )

        self.canvas.draw()

    def exportGraphFile(self):
        fileName, _ = QFileDialog.getSaveFileName(
            None,
            "Save Graph as Image",
            "",
            "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)",
        )
        if fileName:
            self.canvas.print_figure(fileName, bbox_inches="tight", dpi=300)
            print("Graph saved as:", fileName)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Visualize Graph Data"))
        self.graphDataLabel.setText(_translate("MainWindow", "Graph Data:"))
        self.undirectedButton.setText(_translate("MainWindow", "Undirected"))
        self.directedButton.setText(_translate("MainWindow", "Directed"))
        self.exportButton.setText(_translate("MainWindow", "Export"))
        self.terminalLabel.setText(_translate("MainWindow", "Terminal set"))
        self.generationLabel.setText(_translate("MainWindow", "Generation"))
        self.autoGenBtn.setText(_translate("MainWindow", "Auto"))
        self.drawButton.setText(_translate("MainWindow", "Draw"))
        self.styleGraph.setItemText(0, _translate("MainWindow", "Style 1"))
        self.styleGraph.setItemText(1, _translate("MainWindow", "Style 2"))
        self.styleGraph.setItemText(2, _translate("MainWindow", "Style 3"))
        self.styleGraph.setItemText(3, _translate("MainWindow", "Style 4"))
        self.styleGraph.setItemText(4, _translate("MainWindow", "Style 5"))
        self.styleGraph.setItemText(5, _translate("MainWindow", "Style 6"))
        self.styleGraph.setItemText(6, _translate("MainWindow", "Style 7"))
        self.styleGraph.setItemText(7, _translate("MainWindow", "Style 8"))
        self.styleGraphLabel.setText(_translate("MainWindow", "Style Graph"))
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
