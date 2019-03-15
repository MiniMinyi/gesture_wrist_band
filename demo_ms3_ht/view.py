import sys

from PyQt5 import QtCore, QtWebSockets, QtNetwork, QtGui
from PyQt5.QtCore import QUrl, QCoreApplication, QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
import pyqtgraph.opengl as gl
import json
import pyqtgraph as pg
import numpy as np
import time
import requests
from data_container import Data_container
import os
import  tensorflow as tf


class Client(QThread):

    def __init__(self, data_container, url, url_type):
        QThread.__init__(self)
        self._data_container = data_container
        self._get_url = url
        self._type = url_type

    # run method gets called when we start the thread
    def run(self):
        now = int(time.time() * 1000)
        res = requests.get(self._get_url, params={'time': now, 'pDelay': 40000})
        ret = res.content
        self._data_container.insert_image(ret, self._type)


class Predict(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, data_container):
        QThread.__init__(self)
        self._data_container = data_container

    # run method gets called when we start the thread
    def run(self):
        res_flag, ret = self._data_container.predict()
        # print("get prediction ret", res_flag, ret)
        self.signal.emit(ret)


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
        self._data_container = Data_container()
        # print(self.mainbox.getViewport())
        self._gege_client = None
        self._didi_client = None
        self._prediction_thread = None

        # Start
        self._update()

    def _update(self):
        # if self._gege_client:
        #     print(self._gege_client.isFinished())
        if not self._gege_client or self._gege_client.isFinished():
            self._gege_client = Client(self._data_container, "http://192.168.5.178/html/cam_pic.php", 0)
            self._gege_client.start()

        if not self._didi_client or self._didi_client.isFinished():
            self._didi_client = Client(self._data_container, "http://192.168.5.73/html/cam_pic.php", 1)
            self._didi_client.start()

        # if not self._prediction_thread or self._prediction_thread.isFinished():
        #     self._prediction_thread = Predict(self._data_container)
        #     self._prediction_thread.signal.connect(self._finished_prediction)
        #     self._prediction_thread.start()
        res_flag, ret = self._data_container.predict()
        if res_flag == 0:
            ret_points = np.reshape(ret, [21, 3])
            # print(ret_points)
            y, z, x = ret_points.T
            data = np.array([x, y, z])
            vector = data.transpose() / 50
            self.sp.setData(pos=vector)
        # print("update")

        QtCore.QTimer.singleShot(10, self._update)

    def _finished_prediction(self, result):
        pass
        # print(result)


if __name__ == '__main__':
    os.environ["KMP_BLOCKTIME"] = '0'
    os.environ["KMP_SETTINGS"] = '1'
    os.environ["KMP_AFFINITY"] = 'granularity=fine,verbose,compact,1,0'
    os.environ["OMP_NUM_THREADS"] = '4'

    app = QApplication(sys.argv)

    thisapp = App()
    thisapp.show()
    sys.exit(app.exec_())
