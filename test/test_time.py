import sys, os
sys.path.append('..')
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from dicttotreeview.classes import DictToTreeView
import time

class Sensor_standard(QObject):
    data_sig: pyqtSignal = pyqtSignal('PyQt_PyObject')
     
    def __init__(self):
        super().__init__()
        self.data_dict = {'values':list(range(0,5000))}

def test_time_of_signals(qtbot):

    #sensor
    sensor = Sensor_standard()

    #dicttotreeview
    treeview = QtWidgets.QTreeView()

    test_dict2  = {'values': [v + 1 for v in sensor.data_dict['values']] }

    dtv = DictToTreeView(sensor.data_dict, treeview, reset_column=True, highlight_changes=True)
    dtv.tree.ShowPathColumn(True)

    #signals
    sensor.data_sig.connect(dtv.data_sig)#connect input data
    #dtv.output_sig.connect(sensor.update_dc)#connect output data



    with qtbot.waitSignal(dtv.output_sig, timeout=0) as blocker:
        #change dictionary
        start = time.time()
        sensor.data_dict = test_dict2
        sensor.data_sig.emit(sensor.data_dict)
        end = time.time()

    # -s
    #print(end-start)
    duration = end-start
    assert blocker.signal_triggered, 'output signal has not been called'
    assert duration < 1.0, 'time({}) was GREATER than 1s'.format(duration)
    assert duration < 0.7, 'time({}) was greater than 0.700s'.format(duration)
    