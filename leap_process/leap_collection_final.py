import sys

from PyQt5 import QtCore, QtWebSockets, QtNetwork, QtGui
from PyQt5.QtCore import QUrl, QCoreApplication, QTimer
from PyQt5.QtWidgets import QApplication
import pyqtgraph.opengl as gl
import json
import pyqtgraph as pg
import numpy as np
import time


class Client(QtCore.QObject):
    def __init__(self, parent):
        super().__init__(parent)

        self.client = QtWebSockets.QWebSocket("", QtWebSockets.QWebSocketProtocol.Version13, None)

        self.client.connected.connect(self.connected)
        self.client.error.connect(self.error)
        self.client.textMessageReceived.connect(self.on_message)
        self.stored_vectors = np.empty((21, 3))
        self.client.open(QUrl('ws://localhost:6437/v6.json'))

    def init_channel(self):
        print("init channel")
        self.client.sendTextMessage(json.dumps({'enableGestures': True}))
        self.client.sendTextMessage(json.dumps({'focused': True}))

    def connected(self):
        print("connected")
        self.init_channel()

    def on_message(self, message):
        data = json.loads(message)
        now = int(time.time() * 1000)
        with open("data/%d.dat" % now, 'w') as handle:
            handle.write(message)
        hands = data.get("hands", [])
        if len(hands) != 1:
            return
        hand = hands[0]
        wrist = np.array(hand.get('wrist', []))
        fingers = data.get("pointables", [])
        if len(fingers) != 5:
            return
        vectors = []
        for finger in fingers:
            vectors.append(np.array(finger["mcpPosition"]) - wrist)
            vectors.append(np.array(finger["pipPosition"]) - wrist)
            vectors.append(np.array(finger["dipPosition"]) - wrist)
            vectors.append(np.array(finger["tipPosition"]) - wrist)
        vectors.append(np.array(hand["palmPosition"]) - wrist)
        self.stored_vectors = vectors

    def error(self, error_code):
        print("error code: {}".format(error_code))
        print(self.client.errorString())

    def close(self):
        self.client.close()


class App(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        #### Create Gui Elements ###########
        self.mainbox = gl.GLViewWidget()
        self.setFixedSize(800, 800)
        self.setCentralWidget(self.mainbox)
        self.mainbox.setFixedSize(1600, 1200)
        self.mainbox.opts['viewport'] = (0, 0, 1600, 1200)
        self.mainbox.setWindowTitle('test')
        g = gl.GLGridItem()
        self.mainbox.addItem(g)
        pos = np.empty((21, 3))
        sizes = np.ones((21)) * 0.1
        colors = []
        colors_tpt = [[0, 1, 1, 1]]
        for i in range(5):
            colors.append(colors_tpt[0])
            colors.append(colors_tpt[0])
            colors.append(colors_tpt[0])
            colors.append(colors_tpt[0])
        colors.append([1, 0, 1, 1])

        self.sp = gl.GLScatterPlotItem(pos=pos, size=sizes, color=np.array(colors), pxMode=False)
        self.mainbox.addItem(self.sp)

        self.client = Client(app)
        # print(self.mainbox.getViewport())

        #### Start  #####################
        self._update()

    def _update(self):
        vector = np.array(self.client.stored_vectors)
        y, z, x = vector.T
        data = np.array([x, y, z])
        vector = data.transpose() / 50
        self.sp.setData(pos=vector)
        QtCore.QTimer.singleShot(50, self._update)


if __name__ == '__main__':
    global client
    app = QApplication(sys.argv)

    thisapp = App()
    thisapp.show()
    sys.exit(app.exec_())
