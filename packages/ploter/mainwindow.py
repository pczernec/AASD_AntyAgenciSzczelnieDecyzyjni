import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
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
from matplotlib import cm, colors
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.colors import ListedColormap

# Add `packages` dir to path to allow import of `constants`
sys.path.insert(1, str(Path(__file__).parent.parent.absolute()))
from constants.constants import Constants as C


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.socket = QWebSocket()
        self.socket.error.connect(self._socket_error)
        self.socket.textMessageReceived.connect(self.on_agent_data_received)

        grid = QGridLayout()
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        self.sc = MplCanvas(width=5, height=4, dpi=100)
        grid.addWidget(self.sc, 0, 0)

        self.sf = MplCanvas(width=5, height=4, dpi=100)
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

        self.current_id = 0
        self.HP = []
        self.DG = []

        self.connect_to_agent(0)

    def _reconnect(self):
        self.connect_to_agent(self.current_id)

    def _exit(self):
        QApplication.quit()

    def on_agent_change(self):
        idx = self.agents_slider.value()
        self.connect_to_agent(idx)

    def connect_to_agent(self, idx):
        self.current_id = idx
        self.HP = []
        self.DG = []
        self.socket.close()
        self.socket.open(QUrl(f"ws://localhost:{5000 + idx}"))

    def _socket_error(self):
        err = self.socket.errorString()
        print(err)

        self.clear_plots()
        self.sc.axes.set_title(f"Agent {self.current_id}: {err}")
        self.draw_plots()

    def on_agent_data_received(self, msg):
        msg = json.loads(msg)

        states = msg["states"]
        scores = [s["hp"] for s in states]
        my_state = states[0]
        my_score = msg["my_score"]
        my_area_danger_level = msg["area_danger"]

        x = []
        y = []
        z = []

        for state, score in zip(states, scores):
            x.append(state["x"])
            y.append(state["y"])
            z.append(score)

        x = np.array(x) - (my_state["x"])
        y = np.array(y) - (my_state["y"])

        self.HP = self.HP[-C.HISTORY_LEN :] + [my_score]
        self.DG = self.DG[-C.HISTORY_LEN :] + [my_area_danger_level]

        self.clear_plots()
        self.plot_scores(x, y, z)
        self.plot_myscore()
        self.draw_plots()

    def clear_plots(self):
        locator = plticker.MultipleLocator(base=1)
        hist_pad = C.HISTORY_LEN * 0.05

        self.sc.axes.cla()
        self.sc.axes.set_xlim(-1, 1)
        self.sc.axes.set_ylim(-1, 1)
        self.sc.axes.xaxis.set_major_locator(locator)
        self.sc.axes.yaxis.set_major_locator(locator)
        self.sc.axes.set_xlabel("X")
        self.sc.axes.set_ylabel("Y")
        self.sc.axes.set_facecolor("xkcd:white")
        self.sc.axes.set_aspect("equal", adjustable="box")

        self.sf.axes.cla()
        self.sf.axes.set_xlim(-(C.HISTORY_LEN + hist_pad), hist_pad)
        self.sf.axes.set_ylim(0, 1)
        self.sf.axes.set_xlabel("Czas")

    def draw_plots(self):
        self.sc.draw()
        self.sf.draw()

    def plot_scores(self, x, y, z):
        circle_col = "g"
        if self.DG[-1] == C.MEDIUM_DANGER:
            circle_col = "b"
        if self.DG[-1] == C.SERIOUS_DANGER:
            circle_col = "r"
            self.sc.axes.set_facecolor("xkcd:salmon")

        self.sc.axes.set_title(
            f"Pozycje i stan agentów, widok agenta {self.current_id}"
        )

        cmap = cm.get_cmap("winter")
        norm = plt.Normalize(vmin=0.0, vmax=1.0)
        self.sc.axes.scatter(x, y, c=cmap(norm(z)))

        zone_area = plt.Circle(
            (0, 0),
            C.ZONE_AREA_RADIUS,
            color=circle_col,
            clip_on=True,
            fill=False,
        )
        self.sc.axes.add_patch(zone_area)

    def plot_myscore(self):
        norm = plt.Normalize(vmin=0.0, vmax=1.0)
        cmapGreens = cm.get_cmap("Greens")
        cmap = ListedColormap(cmapGreens(np.linspace(0.4, 1.0, 256)))
        self.sf.axes.scatter(
            range(1 - len(self.HP), 1),
            self.HP,
            c=cmap(norm(self.HP)),
            label="Stan agenta",
            marker="+",
        )

        norm = colors.Normalize(vmin=0, vmax=1.0)
        cmapHot = cm.get_cmap("hot")
        cmap = ListedColormap(cmapHot(np.linspace(0.1, 0.5, 256)))
        self.sf.axes.scatter(
            range(1 - len(self.DG), 1),
            self.DG,
            c=cmap(norm(self.DG)),
            label="Poziom zagrożenia",
        )

        self.sf.axes.set_title(f"Stan agenta {self.current_id}")
        self.sf.axes.legend(loc=2)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
