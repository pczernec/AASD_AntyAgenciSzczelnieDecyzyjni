# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QMainWindow, QApplication, QGridLayout, QPushButton, QWidget, QSlider
from PySide2.QtWebSockets import QWebSocket
from PySide2.QtCore import QUrl, Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import colors, cm
import json

import numpy as np

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.socket = QWebSocket()
        grid = QGridLayout()

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        grid.addWidget(self.sc, 0, 0)

        self.sf = MplCanvas(self, width=5, height=4, dpi=100)
        grid.addWidget(self.sf, 0, 1)

        self.agents_slider = QSlider(Qt.Orientation.Horizontal)
        self.agents_slider.setMinimum(0)
        self.agents_slider.setMaximum(10)
        self.agents_slider.setSingleStep(1)
        self.agents_slider.valueChanged.connect(self.on_agent_change)
        grid.addWidget(self.agents_slider, 1, 0)

        button = QPushButton("Reconnect")
        grid.addWidget(button, 2, 0)
        button.clicked.connect(self._reconnect)

        exitbtn = QPushButton("Exit")
        grid.addWidget(exitbtn, 2, 1)
        exitbtn.clicked.connect(self._exit)

        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)

        self.connect_to_agent(0)

    def _reconnect(self):
        self.connect_to_agent(self.current_id)

    def _exit(self):
       QApplication.quit()

    def connect_to_agent(self, idx):
        self.current_id = idx
        self.HP = []
        self.DG = []
        self.socket.close()
        self.socket.error.connect(self._socket_error)
        self.socket.textMessageReceived.connect(self.on_agent_data_received)
        self.socket.open(QUrl(f'ws://localhost:{5000+idx}'))

    def _socket_error(self):
        print(self.socket.errorString())

    def on_agent_data_received(self, msg):
        msg = json.loads(msg)
        print(msg)
        scores = msg['scores']
        myscore = msg['myscore']

        X = []
        Y = []
        Z = []

        for score in scores:
            X.append(score['x'])
            Y.append(score['y'])
            Z.append(score['hp'])

        X = np.array(X) - (myscore['x'])
        Y = np.array(Y) - (myscore['y'])

        self.plot_scores(X, Y, Z)
        self.plot_myscore(myscore)

    def plot_scores(self, X, Y, Z):
        print(X, Y, Z)

        self.sc.axes.cla()
        self.sc.axes.set_xlim(-1, 1)
        self.sc.axes.set_ylim(-1, 1)
        self.sc.axes.set_title(f"Pozycje i stan agnetów, widok agenta {self.current_id}")
        self.sc.axes.set_ylabel("Y")
        self.sc.axes.set_xlabel("X")
        self.sc.axes.scatter(X, Y, c=cm.hot(Z), norm=colors.Normalize(vmin=0.0, vmax=1.0))
        self.sc.draw()

    def plot_myscore(self, score):
        hp = score['hp']
        dg = hp - 0.1 # TODO:

        self.HP = self.HP[:50] + [ hp ]
        self.DG = self.DG[:50] + [ dg ]

        self.sf.axes.cla()
        self.sf.axes.scatter(range(0, len(self.HP)), self.HP, c=cm.hot(self.HP), norm=colors.Normalize(vmin=0, vmax=1.0), label='Stan agenta')
        self.sf.axes.scatter(range(0, len(self.DG)), self.DG, c=cm.hot(self.DG), norm=colors.Normalize(vmin=0, vmax=1.0), label='Poziom zagrożenia')
        self.sf.axes.set_title(f'Stan agenta {self.current_id}')
        self.sf.axes.set_ylim(0, 1)
        self.sf.axes.legend()
        self.sf.draw()


    def on_agent_change(self):
        idx = self.agents_slider.value()
        self.connect_to_agent(idx)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
