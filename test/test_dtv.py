import sys, os
import pdb
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QObject, pyqtSignal


sys.path.append('..')
#load DTV from local classes because else test fails and package release not possible every time

from dicttotreeview.classes import DictToTreeView


class Sensor_standard(QObject):
    data_sig: pyqtSignal = pyqtSignal('PyQt_PyObject')
     
    def __init__(self):
        super().__init__()
        self.data_dict = {"Name": "Elena",
                            "Age": 21,
                            "height": 176.0,
                            "numbers": [1,2,3,4],
                            "book":{"title": "This",},
                            "boxes":[{"Name": "Elena", "Age": 21}, 2.5, 287],
                        }

class Sensor_parameter(QObject):
    data_sig: pyqtSignal = pyqtSignal('PyQt_PyObject')
     
    def __init__(self):
        super().__init__()
        self.data_dict = {"Name": "Elena",
                            "Age": 21,
                            "height": 176.0,
                            "numbers": [1,2,3,4],
                            "book":{"title": "This",},
                            "boxes":[{"Name": "Elena", "Age": 21}, 2.5, 287],
                        }

def test_dtv_init(qtbot):
    """
    Simply testing if DictToTreeView is callable without an error.
    Every test-sensor from above is used.
    """
    sensor1 = Sensor_standard()
    treeview = QtWidgets.QTreeView()
    dtv1 = DictToTreeView(sensor1.data_dict,treeview)
    sensor2 = Sensor_parameter()
    treeview = QtWidgets.QTreeView()
    dtv2 = DictToTreeView(sensor2.data_dict,treeview)
    assert dtv1.comp.data_dict == sensor1.data_dict 
    assert dtv2.comp.data_dict == sensor2.data_dict 


def test_dtv_signal_connection(qtbot):
    """
    Connect the data-signal to DictToTreeView.
    Every test-sensor from above is used.
    """
    #1
    sensor = Sensor_standard()
    treeview = QtWidgets.QTreeView()
    dtv1 = DictToTreeView(sensor.data_dict,treeview)
    sensor.data_sig.connect(dtv1.data_sig)
    #2
    sensor2 = Sensor_parameter()
    treeview = QtWidgets.QTreeView()
    dtv2 = DictToTreeView(sensor2.data_dict,treeview)
    sensor2.data_sig.connect(dtv2.data_sig)

def iteration(d,x=0):
    """
    Counts how much keys are in the dictionary.
    Additionally counts list-indices.
    """
    for key in d:
        x += 1
        if isinstance(d[key],dict):
            x = iteration(d[key],x)
        if isinstance(d[key],list):
            x += len(d[key])
    return x

def test_path_dict(qtbot):
    """
    Testing the length of path dict, ->everything was read
    Every test-sensor from above is used.
    """
    sensor1 = Sensor_standard()
    treeview = QtWidgets.QTreeView()
    dtv1 = DictToTreeView(sensor1.data_dict,treeview)
    sensor2 = Sensor_parameter()
    treeview = QtWidgets.QTreeView()
    dtv2 = DictToTreeView(sensor2.data_dict,treeview)
    assert len(dtv1.tree.path_dict) == iteration(sensor1.data_dict), "path-dict is len{} but data-dict has {} keys".format(len(dtv1.tree.path_dict),iteration(sensor1.data_dict))
    assert len(dtv2.tree.path_dict) == iteration(sensor2.data_dict), "path-dict is len{} but data-dict has {} keys".format(len(dtv2.tree.path_dict),iteration(sensor2.data_dict))
    
def test_dtv_compare(qtbot):
    """
    Tests the compare-class and get_new_data().
    """
    d = {'one':1,'two':2}
    treeview = QtWidgets.QTreeView()
    dtv = DictToTreeView(d,treeview)
    d['two'] = 3
    dtv.comp.get_new_data(d)
    assert dtv.comp.data_dict == d, "data-dict is {} but must be {}".format(dtv.comp.data_dict,d)

def insertItem(item, text, path='root'):
        """
        Adds an item to the model. Equivalent to method in `MyTree`.
        4 Columns: name, type, value, path 
        """
        icon = QtGui.QIcon(":/images/return.png")
        
        if isinstance(item,int):
            #create name item
            standard_item = QtGui.QStandardItem()
            standard_item.setEditable(False)
            #set data for features
            standard_item.setData(item)
            #text() is visible on the treeview
            standard_item.setText(text)
            #create type item
            type_item = QtGui.QStandardItem()
            type_item.setEditable(False)
            type_item.setText('int')
            #create value item
            value_item = QtGui.QStandardItem()
            #cast the value, text is string
            value_item.setText(str(item))
            #create path item
            path_item = QtGui.QStandardItem()
            path_item.setEditable(False)
            #add yourself to hierarchy
            path = path + "['{}']".format(text)
            path_item.setText(path)
            #create item with default values (e.g. initial values)
            dflt_item = QtGui.QStandardItem()
            dflt_item.setData(item)
            dflt_item.setText(str(item))
            dflt_item.setTextAlignment(QtCore.Qt.AlignRight)
            dflt_item.setEditable(False)
            #create reset item with icon
            reset_item = QtGui.QStandardItem()
            reset_item.setText("reset")
            reset_item.setIcon(icon)
            reset_item.setEditable(False)
        
        elif isinstance(item,float):
            standard_item = QtGui.QStandardItem()
            standard_item.setEditable(False)
            standard_item.setData(item)
            standard_item.setText(text)
            type_item = QtGui.QStandardItem()
            type_item.setEditable(False)
            type_item.setText('float')
            value_item = QtGui.QStandardItem()
            value_item.setText(str(item))
            path_item = QtGui.QStandardItem()
            path_item.setEditable(False)
            path = path + "['{}']".format(text)
            path_item.setText(path)
            dflt_item = QtGui.QStandardItem()
            dflt_item.setData(item)
            dflt_item.setText(str(item))
            dflt_item.setTextAlignment(QtCore.Qt.AlignRight)
            dflt_item.setEditable(False)
            reset_item = QtGui.QStandardItem()
            reset_item.setText("reset")
            reset_item.setIcon(icon)
            reset_item.setEditable(False)
            
        elif isinstance(item,list):
            standard_item = QtGui.QStandardItem()
            standard_item.setEditable(False)
            standard_item.setData(item)
            standard_item.setText(text)
            type_item = QtGui.QStandardItem()
            type_item.setEditable(False)
            type_item.setText('list')
            path_item = QtGui.QStandardItem()
            path_item.setEditable(False)
            path = path + "['{}']".format(text)
            path_item.setText(path)
            dflt_item = QtGui.QStandardItem()
            dflt_item.setEditable(False)
            reset_item = QtGui.QStandardItem()
            reset_item.setEditable(False)
            value_item = QtGui.QStandardItem()
            text = 'length='+"{}".format(len(item))
            value_item.setText(text)
            value_item.setEditable(False)
            #add every position of list
            for i in range(0,len(item)):
                temp_standard_item = QtGui.QStandardItem()
                temp_standard_item.setEditable(False)
                temp_standard_item.setData(item[i])
                temp_standard_item.setText(str(i))
                temp_type_item = QtGui.QStandardItem()
                temp_type_item.setEditable(False)
                temp_dflt_item = QtGui.QStandardItem()
                temp_dflt_item.setTextAlignment(QtCore.Qt.AlignRight)
                temp_dflt_item.setEditable(False)
                temp_reset_item = QtGui.QStandardItem()
                temp_reset_item.setText("reset")
                temp_reset_item.setIcon(icon)
                temp_reset_item.setEditable(False)
                temp_value_item = QtGui.QStandardItem()
                temp_value_item.setText(str(item[i]))
                if isinstance(item[i],int):
                    temp_type_item.setText('int')
                    temp_dflt_item.setText(str(item[i]))
                    temp_dflt_item.setData(item[i])               
                if isinstance(item[i],float):
                    temp_type_item.setText('float') 
                    temp_dflt_item.setText(str(item[i]))
                    temp_dflt_item.setData(item[i])                
                if isinstance(item[i],str):
                    temp_type_item.setText('str')
                    temp_value_item.setText(item[i])
                    temp_dflt_item.setText(item[i])
                if isinstance(item[i],dict):
                    temp_type_item.setText('dict')
                    text = 'length='+"{}".format(len(item[i]))
                    temp_value_item.setText(text)
                    temp_value_item.setEditable(False) 
                temp_path_item = QtGui.QStandardItem()
                temp_path_item.setEditable(False)
                temp_path = path + "[{}]".format(i)
                temp_path_item.setText(temp_path)
                standard_item.setChild(i,0,temp_standard_item)
                standard_item.setChild(i,1,temp_type_item)
                standard_item.setChild(i,2,temp_value_item)
                standard_item.setChild(i,3,temp_path_item)
                standard_item.setChild(i,4,temp_dflt_item)
                standard_item.setChild(i,5,temp_reset_item)
                if isinstance(item[i],dict):
                    item_row = 0
                    for key in item[i]:
                        temp_item = insertItem(item[i][key],key,temp_path)
                        temp_standard_item.setChild(item_row,0,temp_item[0])
                        temp_standard_item.setChild(item_row,1,temp_item[1])
                        temp_standard_item.setChild(item_row,2,temp_item[2])
                        temp_standard_item.setChild(item_row,3,temp_item[3])
                        temp_standard_item.setChild(item_row,4,temp_item[4])
                        temp_standard_item.setChild(item_row,5,temp_item[5])
                        item_row += 1   
                
        elif isinstance(item,str):
            standard_item = QtGui.QStandardItem()
            standard_item.setEditable(False)
            standard_item.setData(item)
            standard_item.setText(text)
            type_item = QtGui.QStandardItem()
            type_item.setEditable(False)
            type_item.setText('str')
            value_item = QtGui.QStandardItem()
            value_item.setText(item)
            path_item = QtGui.QStandardItem()
            path_item.setEditable(False)
            path = path + "['{}']".format(text)
            path_item.setText(path)
            dflt_item = QtGui.QStandardItem()
            dflt_item.setData(item)
            dflt_item.setText(item)
            dflt_item.setTextAlignment(QtCore.Qt.AlignRight)
            dflt_item.setEditable(False)
            reset_item = QtGui.QStandardItem()
            reset_item.setText("reset")
            reset_item.setIcon(icon)
            reset_item.setEditable(False)

        elif isinstance(item,bytes):
            standard_item = QtGui.QStandardItem()
            standard_item.setEditable(False)
            standard_item.setData(item)
            standard_item.setText(text)
            type_item = QtGui.QStandardItem()
            type_item.setEditable(False)
            type_item.setText('bytes')
            value_item = QtGui.QStandardItem()
            value_item.setText(str(item))
            path_item = QtGui.QStandardItem()
            path_item.setEditable(False)
            path = path + "['{}']".format(text)
            path_item.setText(path)
            dflt_item = QtGui.QStandardItem()
            dflt_item.setData(item)
            dflt_item.setText(str(item))
            dflt_item.setTextAlignment(QtCore.Qt.AlignRight)
            dflt_item.setEditable(False)
            reset_item = QtGui.QStandardItem()
            reset_item.setText("reset")
            reset_item.setIcon(icon)
            reset_item.setEditable(False)
            
        elif isinstance(item,dict):
            standard_item = QtGui.QStandardItem()
            standard_item.setEditable(False)
            standard_item.setData(item)
            standard_item.setText(text)
            type_item = QtGui.QStandardItem()
            type_item.setEditable(False)
            type_item.setText('dict')
            path_item = QtGui.QStandardItem()
            path_item.setEditable(False)
            path = path + "['{}']".format(text)
            path_item.setText(path)
            dflt_item = QtGui.QStandardItem()
            dflt_item.setTextAlignment(QtCore.Qt.AlignRight)
            dflt_item.setEditable(False)
            reset_item = QtGui.QStandardItem()
            reset_item.setEditable(False)
            value_item = QtGui.QStandardItem()
            value_item.setEditable(False)
            #add length of dict
            text = 'length='+"{}".format(len(item))
            value_item.setText(text)
            #recursively adding the dict
            item_row = 0
            for key in item:
                temp_item = insertItem(item[key],key,path)
                standard_item.setChild(item_row,0,temp_item[0])
                standard_item.setChild(item_row,1,temp_item[1])
                standard_item.setChild(item_row,2,temp_item[2])
                standard_item.setChild(item_row,3,temp_item[3])
                standard_item.setChild(item_row,4,temp_item[4])
                standard_item.setChild(item_row,5,temp_item[5])
                item_row += 1   

        else:
            #not supported type:
            print('unsupported input value', item, 'from type', type(item))
            standard_item = QtGui.QStandardItem()
            standard_item.setEditable(False)
            standard_item.setData(item)
            standard_item.setText(text)
            type_item = QtGui.QStandardItem()
            type_item.setEditable(False)
            type_item.setText(str(type(item)))
            value_item = QtGui.QStandardItem()
            value_item.setEditable(False)
            value_item.setText(str(item))
            path_item = QtGui.QStandardItem()
            path_item.setEditable(False)
            path = path + "['{}']".format(text)
            path_item.setText(path)
            dflt_item = QtGui.QStandardItem()
            dflt_item.setData(item)
            dflt_item.setText(str(item))
            dflt_item.setTextAlignment(QtCore.Qt.AlignRight)
            dflt_item.setEditable(False)
            reset_item = QtGui.QStandardItem()
            reset_item.setText("reset")
            reset_item.setIcon(icon)
            reset_item.setEditable(False)
            
        return (standard_item, type_item, value_item, path_item, dflt_item, reset_item)

def test_insertItem(qtbot):
    """
    Builds a model and inserts the dictionary, d.
    Tests whether DictToTreeView works like function `MyTree.insertItem()`.
    Testing rowcount, columncout, haschildren.
    """
    d = {
        'dict':{
            'dict':{
                'dict':{
                    'dict':0,
                },
            },
        },
        'int':32,
        'float':3.221,
        'list':[1,2,3],
        'str': 'string',
        'byte': b'',
    }
    treeview = QtWidgets.QTreeView()
    dtv = DictToTreeView(d,treeview)

    #create model
    model_rows = len(d)
    standard_model = QtGui.QStandardItemModel(model_rows,6)
    #define columns like pyqtgraph.widgets.DataTreeWidget
    name_column = QtGui.QStandardItem('name')
    standard_model.setHorizontalHeaderItem(0,name_column)
    type_column = QtGui.QStandardItem('type')
    standard_model.setHorizontalHeaderItem(1,type_column)
    value_column = QtGui.QStandardItem('value')
    standard_model.setHorizontalHeaderItem(2,value_column)
    path_column = QtGui.QStandardItem('path')
    standard_model.setHorizontalHeaderItem(3,path_column)
    default_column = QtGui.QStandardItem('default')
    default_column.setTextAlignment(QtCore.Qt.AlignRight)
    standard_model.setHorizontalHeaderItem(4,default_column)
    reset_column = QtGui.QStandardItem()
    standard_model.setHorizontalHeaderItem(5,reset_column)
    #append items to model
    model_row = 0
    for key in d:
        item = insertItem(d[key],key)
        #setItem(start=0,start=0,item)
        standard_model.setItem(model_row,0,item[0])
        standard_model.setItem(model_row,1,item[1])
        standard_model.setItem(model_row,2,item[2])
        standard_model.setItem(model_row,3,item[3])
        standard_model.setItem(model_row,4,item[4])
        standard_model.setItem(model_row,5,item[5])
        model_row += 1
        
    #test row, column, hasChildren
    x1 = standard_model.rowCount() - dtv.tree.standard_model.rowCount()
    x2 = standard_model.columnCount() - dtv.tree.standard_model.columnCount()
    x3 = standard_model.hasChildren() - dtv.tree.standard_model.hasChildren()
    #to continue

    assert x1 == 0, "test was {} rows, package gives {} rows back".format(standard_model.rowCount(),dtv.tree.standard_model.rowCount())
    assert x2 == 0, "test was {} columns, package gives {} columns back".format(standard_model.columnCount(),dtv.tree.standard_model.columnCount())
    assert x3 == 0, "children in test: {}, children in package: {}".format(standard_model.hasChildren(),dtv.tree.standard_model.hasChildren())

def path_column(item, liste):
    """
    Create a list of the entries in the 4. column of a QStandardItemModel.
    """
    #pdb.set_trace()
    for i in range(item.rowCount()):
        if isinstance(item, QtGui.QStandardItemModel): 
            path_item = item.item(i,3)
            liste.append(path_item.text())
            if (item.item(i,1).text() == 'dict'):
                path_column(item.item(i,0),liste)
            elif (item.item(i,1).text() == 'list'):
                for c in range(item.item(i,0).rowCount()):
                    liste.append(path_item.text()+"[{}]".format(c))
        elif isinstance(item, QtGui.QStandardItem): 
            path_item = item.child(i,3)
            liste.append(path_item.text())
            if (item.child(i,1).text() == 'dict'): 
                path_column(item.child(i,0),liste)
            elif (item.child(i,1).text() == 'list'):
                for c in range(item.child(i,0).rowCount()):
                    liste.append(path_item.text()+"[{}]".format(c))
    return liste    
        
def test_path_column(qtbot):
    """
    Compares if the hidden column 4 is the same as the keys of the generated path dict.
    """
    sensor1 = Sensor_standard()
    treeview = QtWidgets.QTreeView()
    dtv = DictToTreeView(sensor1.data_dict,treeview)

    forthC = []
    forthC = path_column(dtv.tree.standard_model, forthC)
    #assertion error raised automatically
    assert list(dtv.tree.path_dict) == forthC




        



