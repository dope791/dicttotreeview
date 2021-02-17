import sys
import copy 
import numpy as np
import time
from deepdiff import DeepDiff, Delta
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from MainWindow import Ui_MainWindow  
sys.path.append('.')
from lib.dicts import s_Param_ProductionBlock_t
from pprintpp import pprint as pp



class DummySensor(QObject):
    sensor_data_sig: pyqtSignal = pyqtSignal('PyQt_PyObject')
     
    def __init__(self):
        super().__init__()
        self.data_dict = s_Param_ProductionBlock_t

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.gen_new_data)
        self.timer.start(3000)

    def gen_new_data(self):
        #changing ['s_AlgoMode']['e_HystMode']
        self.data_dict['ALINE']['e_SensorType'] += 1
        self.sensor_data_sig.emit(self.data_dict)

    @pyqtSlot(dict)
    def update_dc(self, dc):
        change = DeepDiff(self.data_dict,dc)
        #print('Change: ',change)
        self.data_dict = copy.deepcopy(dc)
        #print("user dict",self.data_dict)

        
           
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.TreeView = self.ui.treeView
        
         

