import sys
sys.path.append('.')
import copy 
import time
from deepdiff import DeepDiff
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from MainWindow import Ui_MainWindow 
from pprintpp import pprint as pp
 
class DummySensor(QObject):
    sensor_data_sig: pyqtSignal = pyqtSignal('PyQt_PyObject')
     
    def __init__(self):
        super().__init__()
        self.data_dict = {"Name": "Elena",
                            "Age": 21,
                            "height": 176.0,
                            "numbers": [1,2,3,4],
                            "book":{"title": "This",},
                            "boxes":[{"Name": "Elena", "Age": 21}, 2.5, 287],
                            }

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.gen_new_data)
        self.timer.start(3000)

    def gen_new_data(self):
        self.data_dict["Age"] += 1
        self.sensor_data_sig.emit(self.data_dict)

    @pyqtSlot(dict)
    def update_dc(self, dc):
        change = DeepDiff(self.data_dict,dc) 
        self.data_dict = copy.deepcopy(dc)
       

        
           
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.TreeView = self.ui.treeView
        
         
