# This Python file uses the following encoding: utf-8
import json
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide2.QtCore import Qt, QUrl
from PySide2.QtWebSockets import QWebSocket
from PySide2.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QPushButton,
    QSlider,
    QWidget,
)


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):
    # Those constants are shared with the DangerNotifier class.
    SMALL_DANGER = 0.2
    MEDIUM_DANGER = 0.5
    RUN_TYPE_OF_DANGER = 0.8

    ZONE_AREA_RADIUS = 0.3

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
        self.socket.open(QUrl(f"ws://localhost:{5000+idx}"))

    def _socket_error(self):
        print(self.socket.errorString())

    def on_agent_data_received(self, msg):
        msg = json.loads(msg)

        states = msg["states"]
        scores = [s["hp"] for s in states]
        my_state = states[0]
        my_score = msg["my_score"]
        my_area_danger_level = msg["area_danger"]

        X = []
        Y = []
        Z = []

        for state, score in zip(states, scores):
            X.append(state["x"])
            Y.append(state["y"])
            Z.append(score)

        X = np.array(X) - (my_state["x"])
        Y = np.array(Y) - (my_state["y"])

        self.plot_scores(X, Y, Z, my_area_danger_level)
        self.plot_myscore(my_score, my_area_danger_level)

    def plot_scores(self, X, Y, Z, my_area_danger_level):
        self.sc.axes.cla()

        circle_col = "g"
        if my_area_danger_level == self.MEDIUM_DANGER:
            circle_col = "b"
        elif my_area_danger_level == self.RUN_TYPE_OF_DANGER:
            circle_col = "r"
            self.sc.axes.set_facecolor('xkcd:salmon')

        self.sc.axes.set_xlim(-1, 1)
        self.sc.axes.set_ylim(-1, 1)
        self.sc.axes.set_title(
            f"Pozycje i stan agentów, widok agenta {self.current_id}"
        )
        self.sc.axes.set_ylabel("Y")
        self.sc.axes.set_xlabel("X")
        cmap = cm.get_cmap("winter")
        self.sc.axes.scatter(X, Y, c=cmap(Z), norm=colors.Normalize(vmin=0.0, vmax=1.0))


        zone_area = plt.Circle(
            (0, 0),
            self.ZONE_AREA_RADIUS,
            color=circle_col,
            clip_on=True,
            fill=False,
        )
        self.sc.axes.add_patch(zone_area)
        self.sc.draw()

    def plot_myscore(self, my_score, my_area_danger_level):
        self.HP = self.HP[:50] + [my_score]
        self.DG = self.DG[:50] + [my_area_danger_level]

        self.sf.axes.cla()
        self.sf.axes.scatter(
            range(0, len(self.HP)),
            self.HP,
            c=cm.hot(self.HP),
            norm=colors.Normalize(vmin=0, vmax=1.0),
            label="Stan agenta",
        )
        self.sf.axes.scatter(
            range(0, len(self.DG)),
            self.DG,
            c=cm.hot(self.DG),
            norm=colors.Normalize(vmin=0, vmax=1.0),
            label="Poziom zagrożenia",
        )
        self.sf.axes.set_title(f"Stan agenta {self.current_id}")
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
