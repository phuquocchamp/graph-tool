from PyQt6 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1271, 845)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.inputData = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.inputData.setGeometry(QtCore.QRect(30, 130, 221, 611))
        self.inputData.setPlainText("")
        self.inputData.setObjectName("inputData")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 90, 91, 16))
        self.label.setObjectName("label")
        self.undirectedButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.undirectedButton.setGeometry(QtCore.QRect(30, 30, 94, 34))
        self.undirectedButton.setObjectName("undirectedButton")
        self.directedButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.directedButton.setGeometry(QtCore.QRect(160, 30, 94, 34))
        self.directedButton.setObjectName("directedButton")
        self.exportButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.exportButton.setGeometry(QtCore.QRect(1170, 770, 91, 34))
        self.exportButton.setObjectName("exportButton")
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(290, 30, 861, 771))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.graphArea = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.graphArea.setContentsMargins(0, 0, 0, 0)
        self.graphArea.setObjectName("graphArea")
        self.drawButttn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.drawButttn.setGeometry(QtCore.QRect(170, 760, 75, 23))
        self.drawButttn.setObjectName("drawButttn")

        # add canvas
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.graphArea.addWidget(self.canvas)

        # draw clicked.
        self.drawButttn.clicked.connect(self.submitDraw)

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

    def submitDraw(self):
        rdata = self.inputData.toPlainText()
        self.draw_weighted_graph_text(rdata)

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
            "edgecolors": "black",
            "linewidths": 3,
            "width": 3,
        }

        nx.draw(G, pos, **options)
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
