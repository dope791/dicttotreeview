import sys
import copy 
import re
from deepdiff import DeepDiff, Delta
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QSortFilterProxyModel
from PyQt5.QtWidgets import QAbstractItemView
                                                                


class Compare(QObject):
    """
    This class is holding the current dictionary data.
    Through its method it actualizes the dicitonary with new data input.
    Signal of changed dictionary will be emitted.
    """    
    change_sig: pyqtSignal = pyqtSignal(dict)
    org_dc: pyqtSignal = pyqtSignal(dict)
    item_edit: pyqtSignal = pyqtSignal(QtCore.QModelIndex,str,object)

    def __init__(self, original_dict):
        """
        Initialize with Your dictionary.

        =============== =================== ========================================
        **Arguments:**   **type:**
        *original_dict*   *dict*            original dictionary 
        =============== =================== ========================================
        """
        super().__init__()
        self.data_dict = copy.deepcopy(original_dict)
        self.colored = False
    

    def Colored_Change(self ,colored: bool):
        """
        Set True if you want to see changed values magenta. 
        Default is False.
        """
        self.colored = colored  


    @pyqtSlot('QStandardItem*')
    def edit_item(self, item):
        """
        Called when QStandardItem(item) in QTreeView has been edited.
        Working on the self data dictionary and 
        adjusting the original dictionary of DTV. 

        =============== ======================= ========================================
        **Arguments:**   **type:**
        *item*          *QtGui.QStandarditem*   item that has changed
        =============== ======================= ========================================
        """
        #calling the function again:
        if self.colored == True:
            item.setForeground(QtGui.QBrush(QtGui.QColor("magenta")))
        index = item.index()
        path_index = index.siblingAtColumn(3)
        root_path = path_index.data()
        path_list = re.split(r'\W+',root_path[4:])
        dc_target = self.get_value(self.data_dict,path_list)
        #type support,compare old type
        if isinstance(dc_target,int):
            #item.text() is a string
            try:
                value = int(item.text())
            except ValueError:
                try:
                    value = float(item.text())
                    value = int(value)
                except ValueError:
                    print("wrong datatype input")
                    value = dc_target
            finally:
                self.set_value(self.data_dict,path_list,value)
        elif isinstance(dc_target,float):
            try:
                value = float(item.text())
            except ValueError:
                print("wrong datatype input")
                value = item.text()
                value = dc_target 
            finally:
                self.set_value(self.data_dict,path_list,value)
        elif isinstance(dc_target,str):
            try:
                print('wrong datatype input')
                #float can cast int too
                value = float(item.text())
                value = dc_target
            except ValueError:
                value = item.text() 
            finally:
                self.set_value(self.data_dict,path_list,value)
        elif isinstance(dc_target,bytes):
            try:
                value = bytes(item.text())
            except (ValueError, TypeError):
                print("wrong datatype input")
                value = dc_target
            finally:    
                self.set_value(self.data_dict,path_list,value)
        self.org_dc.emit(self.data_dict)
        self.item_edit.emit(index,root_path,value)

    @pyqtSlot(dict)
    def get_new_data(self, new_data):
        """
        Actualizing the data dictionary that holds the current data.  
        The signal of changed dictionary will be emitted every time of new data dict received. 

        =============== =================== ========================================
        **Arguments:**   **type:**
        *new_data*       *dict*              dictionary with new arguments
        =============== =================== ========================================

        =============== =================== =========================================
        **Return:**      **type:**
        *changes*       *DeepDiff*            dictionary of changes
        =============== =================== =========================================
        """
        change = DeepDiff(self.data_dict,new_data)
        delta = Delta(change)
        self.data_dict = self.data_dict + delta 
        self.change_sig.emit(change)
        self.org_dc.emit(self.data_dict)
        return change    
       

    def get_value(self,dc,path_list,ref_list=[],value=0):
        """
        Returns the current value hold by the dictionary in the place of 'path'.

        =============== ========================= ===========================================
        **Arguments:**   **type:**
        *dc*             *dict*                   target dictionary to be searched
        *path_list*      *list*                   sequence of keys for the several value
        *ref_list*       *list*                   dummy list to copy to (>no reference work)
        *value*          *int,str,bytes,float*    value in the place
        =============== ========================= ===========================================
        
        ================= ======================= =========================================== 
        **Returns:**      **type:**
        *value*            *int,str,byte,float*   value in the place  
        ================= ======================= =========================================== 
        """
        ref_list = path_list.copy()
        if ref_list != []:
            that = ref_list[0]
            ref_list.pop(0)
            if that != '' and not isinstance(dc,(int,float)):
                if isinstance(dc,list):
                    that = int(that)
                value = self.get_value(dc[that],ref_list,value)
            else:
                value = self.get_value(dc,ref_list,value)
            return value
        #if ref_list is empty
        else:
            value = dc
            return value 


    def set_value(self,dc,path_list,value):
        """
        Set a value to a dictionary with description of path.

        =============== ========================= ===========================================
        **Arguments:**   **type:**
        *dc*             *dict*                   target dictionary to be written into
        *path_list*      *list*                   sequence of keys for the value to be placed
        *value*          *int,str,bytes,float*    new value 
        =============== ========================= ===========================================
        """
        if path_list != []:
            that = path_list[0]
            path_list.pop(0)
            if that != '':
                if not isinstance(dc[that],dict):
                    if isinstance(dc[that],list):
                        index = int(path_list[0])
                        dc[that][index] = value
                        return
                    dc[that] = value
                self.set_value(dc[that],path_list,value)
            else:
                self.set_value(dc,path_list,value)
     
        
class DictToTreeView(QObject):
    """
    This class is the interface to the external user.
    """
    data_sig: pyqtSignal = pyqtSignal(dict)
    output_sig: pyqtSignal = pyqtSignal(dict)
    
    def __init__(self, original_dict: dict, TreeView: QtWidgets.QTreeView, patterns=[], reset_column=False, highlight_changes=False):
        """
        Set Your dictionary and Your corresponding treeview.

        ===================== ======================== ===================================================================
        **Arguments:**        **type:**
        *data dictionary*     *dict*                    dictionary to be initialized firstly, structure will be supported
        *treeview*            *QtWidgets.QTreeView*     TreeView 
        *patterns*            *list*                    list of patterns to be filtered in keys of model_dict
        *reset_column*        *bool*                    sets reset columns enabled
        *highlight_changes*   *bool*                    displays changed values colored
        ===================== ======================== ===================================================================
        """
        super().__init__()
        self.original_dict = copy.deepcopy(original_dict)
        self.view_dict = copy.deepcopy(original_dict)
        #filter data_dict
        for x in range(len(patterns)):
            self.filter_dict(original_dict,self.view_dict,patterns[x])
        self.comp = Compare(self.original_dict)
        self.comp.Colored_Change(highlight_changes)
        self.tree = MyTree(self.view_dict, TreeView, self.comp)
        self.tree.set_color(highlight_changes)
        self.tree.EnableResetColumn(reset_column)

        #signals
        #############################################################################################
        self.data_sig.connect(self.comp.get_new_data)#extern data_sig to compare class

        self.comp.change_sig.connect(self.tree.update_standard_model)#change_dict to model class

        self.comp.item_edit.connect(self.tree.update_path_dict)#edited item updates path dict

        self.comp.org_dc.connect(self.update_org_dc)#update original_dict

        self.tree.standard_model.itemChanged.connect(self.comp.edit_item)#editing dict in GUI(manual)
        #############################################################################################


    def filter_dict(self,original_dict,data_dict,pattern):
        """
        Deletes all keys equivalent to `pattern` in the dictionary to create the model from.

        ================= ======================= ========================================
        **Arguments:**     **type:**
        *original_dict*    *dict*                   original user input dictionary
        *data_dict*        *dict*                   flexible class dicitonary
        *pattern*          *string, regEx*          pattern that sould be filtered 
        ================= ======================= ========================================
        """
        for key in original_dict:
            if key == pattern:
                del data_dict[key]
            elif isinstance(original_dict[key],dict):
                self.filter_dict(original_dict[key],data_dict[key],pattern)


    @pyqtSlot(dict)
    def update_org_dc(self, dc):
        """
        Update the original dictionary of the client.

        ================= ======================= ========================================
        **Arguments:**     **type:**
        *dc*              *dict*                   changed dict
        ================= ======================= ========================================
        """
        self.original_dict = copy.deepcopy(dc)
        self.output_sig.emit(self.original_dict)
        
            
    
class MyTree(QObject):
    """
    This class creates the actual tree with `QStandardItem`s in a `QStandardItemModel`.

    """
    def __init__(self, original_dict, TreeView, compare):
        """
        Define the dictionary that You want to display.
        Give the treeview to the MyTree instance. 
        Treeview holds the actual model. 

        ================= ======================= ========================================
        **Arguments:**    **type:**
        *original_dict*   *dict*                  dictionary from user
        *TreeView*        *QtWidgets.QTreeView*   treeView that holds the model
        *compare*         *Compare*               Instance of Compare class from DTV class 
        ================= ======================= ========================================
        """
        super().__init__()
        self.colored = False
        self.comp = compare
        self.TreeView = TreeView
        self.path_dict = {}
        #create ProxyModel 
        self.proxyModel = QSortFilterProxyModel(self)
        #create model
        model_rows = len(original_dict)
        self.standard_model = QtGui.QStandardItemModel(model_rows,6)
        #define columns, like pyqtgraph.widgets.DataTreeWidget
        name_column = QtGui.QStandardItem('name')
        self.standard_model.setHorizontalHeaderItem(0,name_column)
        type_column = QtGui.QStandardItem('type')
        self.standard_model.setHorizontalHeaderItem(1,type_column)
        value_column = QtGui.QStandardItem('value')
        self.standard_model.setHorizontalHeaderItem(2,value_column)
        path_column = QtGui.QStandardItem('path')
        self.standard_model.setHorizontalHeaderItem(3,path_column)
        default_column = QtGui.QStandardItem('default')
        #default_column.setTextAlignment(QtCore.Qt.AlignRight)
        self.standard_model.setHorizontalHeaderItem(4,default_column)
        reset_column = QtGui.QStandardItem('reset to default')
        self.standard_model.setHorizontalHeaderItem(5,reset_column)
        #append items to model
        model_row = 0
        for key in original_dict:
            item = self.insertItem(original_dict[key],key)
            #setItem(start=0,start=0,item)
            self.standard_model.setItem(model_row,0,item[0])
            self.standard_model.setItem(model_row,1,item[1])
            self.standard_model.setItem(model_row,2,item[2])
            self.standard_model.setItem(model_row,3,item[3])
            self.standard_model.setItem(model_row,4,item[4])
            self.standard_model.setItem(model_row,5,item[5])
            model_row += 1
        #set ProxyModel
        self.proxyModel.setSourceModel(self.standard_model)
        #set treeview
        self.TreeView.setModel(self.proxyModel)
        self.TreeView.resizeColumnToContents(0)
        self.TreeView.clicked.connect(self.reset_value)
        self.TreeView.setSelectionBehavior(0)
        self.TreeView.setAlternatingRowColors(True)
        #search with column 4 but not display it
        self.TreeView.setColumnHidden(3,True)
        #disable reset for values
        self.TreeView.setColumnHidden(4,True)
        self.TreeView.setColumnHidden(5,True)
        #generate path dictionary
        self.gen_path_dict(self.standard_model,self.path_dict)    
        

    def EnableResetColumn(self, reset: bool):
        """
        Set `reset` True to see the initial values in the TreeView and have a reset button.
        Default is False. 

        ================= ============================ ========================================
        **Arguments:**    **type:**
        *reset*           *bool*                       set column hidden
        ================= ============================ ========================================
        """
        self.TreeView.setColumnHidden(4,not reset)
        self.TreeView.setColumnHidden(5,not reset)
    

    @pyqtSlot(str)
    def filter_model(self, pattern):
        """
        Create a filter for Your Model via a Proxy Model.
        Search with string-patterns.
        Connect a QLineEdit.textChanged() signal.

        ================= ============================ ===============================================================
        **Arguments:**    **type:**
        *pattern*         *string*                      string-pattern which filters the first column of the treeview
        ================= ============================ ===============================================================
        """
        #recursive tree filtering
        self.proxyModel.setRecursiveFilteringEnabled(1)
        self.proxyModel.setFilterFixedString(pattern)
        #case sensivity = insensitive, e.g. upper/lower case 
        self.proxyModel.setFilterCaseSensitivity(0)
        self.proxyModel.setFilterKeyColumn(3)


    def gen_path_dict(self, item, parent_idx_dict, path="root", list_counter=0):
        """
        This funciton generates recursively an index dictionary for the update-method.

        ================= ============================ ========================================
        **Arguments:**    **type:**
        *item*            *QtGui.QStandardItem(Model)*   relative headitem
        *idx_dict*        *dict*                         created dictionary  
        *path*            *str*                          path string as prefix
        ================= ============================ ========================================
        """
        parent_prefix = path
        for row in range(item.rowCount()):
            #switch case for (model || item)
            if isinstance(item,QtGui.QStandardItemModel):
                name_child = item.item(row,0)
                type_child = item.item(row,1)
                value_child = item.item(row,2)
            else:
                name_child = item.child(row, 0)
                type_child = item.child(row,1)
                value_child = item.child(row,2)   
            #create dictionary    
            if item.hasChildren():
                #content of keys (path)
                child_idx_dict = {'name_index': name_child.index(),'type_index': type_child.index(),'value_index': value_child.index(), 'data/value': name_child.data(), 'row': row}
                #expand key (path)
                path = parent_prefix + "['{}']".format(name_child.text())
                #make difference for list
                if name_child.parent() != None:
                    type_parent_index = name_child.parent().index().siblingAtColumn(1)
                    type_parent_item = self.standard_model.itemFromIndex(type_parent_index)
                    if type_parent_item.text() == 'list':
                        path = parent_prefix + "[{}]".format(name_child.text())                 
                #add content to dict[key]
                parent_idx_dict[path] = child_idx_dict
                self.gen_path_dict(name_child,parent_idx_dict,path,list_counter)


    def insertItem(self, item, text, path='root'):
        """
        Adds an item to the model.
        4 Columns: name, type, value, path 

        ================= ============================ ========================================
        **Arguments:**    **type:**
        *item*            *dict*,*any*                  dictionary[key]
        *text*            *str*                         key  
        *path*            *str*                         prefix for path item text
        ================= ============================ ========================================
            
        ================= ================================================================== ==========================================
        **Returns:**      **type:**
        *item*            *(QtGui.QStandardItem,QtGui.QStandardItem,QtGui.QStandardItem)*    (name, type, value)
        ================= ================================================================== ==========================================
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
            dflt_item.setEditable(False)
            #create reset item with icon
            reset_item = QtGui.QStandardItem()
            reset_item.setData(icon,role=1)
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
            dflt_item.setEditable(False)
            reset_item = QtGui.QStandardItem()
            reset_item.setData(icon,role=1)
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
                temp_dflt_item.setEditable(False)
                temp_reset_item = QtGui.QStandardItem()
                temp_reset_item.setData(icon,role=1)
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
                        temp_item = self.insertItem(item[i][key],key,temp_path)
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
            dflt_item.setEditable(False)
            reset_item = QtGui.QStandardItem()
            reset_item.setData(icon,role=1)
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
            dflt_item.setEditable(False)
            reset_item = QtGui.QStandardItem()
            reset_item.setData(icon,role=1)
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
                temp_item = self.insertItem(item[key],key,path)
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
            dflt_item.setEditable(False)
            reset_item = QtGui.QStandardItem()
            reset_item.setData(icon,role=1)
            reset_item.setEditable(False)
            
        return (standard_item, type_item, value_item, path_item, dflt_item, reset_item)


    def reset_value(self, index):
        #only when reset item clicked
        if index.data(role=1):
            parent_index = index.parent()
            parent_item_list = self.standard_model.findItems(parent_index.data(),QtCore.Qt.MatchRecursive)
            parent_item = parent_item_list[0]
            parent_index_model = self.standard_model.indexFromItem(parent_item)
            type_index_model = parent_index_model.siblingAtColumn(1)
            type_item = self.standard_model.itemFromIndex(type_index_model)
            default_index = index.siblingAtColumn(4)
            value_index = index.siblingAtColumn(2)
            name_index = index.siblingAtColumn(0)
            if type_item.text() == 'list':
                list_index = int(name_index.data())
                list_value_item = parent_item.child(list_index,2)
                value_item = list_value_item
                #print("", name[i])
                print("DictToTreeView: ","{}[{}]".format(parent_item.text(),list_index)," ", value_item.text() ,"to", default_index.data())
            else:
                name_item_list = self.standard_model.findItems(name_index.data(),QtCore.Qt.MatchRecursive)
                name_item = name_item_list[0]
                name_index_model = self.standard_model.indexFromItem(name_item)
                value_index_model = name_index_model.siblingAtColumn(2)
                value_item = self.standard_model.itemFromIndex(value_index_model)
                print("DictToTreeView: ", name_index.data()," ", value_item.text() ,"to", default_index.data())
            #set new text
            value_item.setText(default_index.data())
            #disconnect the items from everything
            self.standard_model.itemChanged.disconnect()
            value_item.setForeground(QtGui.QBrush(QtGui.QColor("black")))
            #reconnect itemChanged signal with Compare method
            self.standard_model.itemChanged.connect(self.comp.edit_item)

    def ShowPathColumn(self, hide: bool):
        """
        You can show column 4 with the path in it. Default is False.

        ================= ============================ ========================================
        **Arguments:**    **type:**
        *hide*            *bool*                       set column hidden
        ================= ============================ ========================================
        """
        self.TreeView.setColumnHidden(3,not hide)


    @pyqtSlot(bool)
    def set_color(self, colored):
        """
        Take the flag colored from compare class over. 
        This needs to be set because of different update ways (manual in TreeView oder changing the input dictionary)

        ================= ============================ ========================================
        **Arguments:**    **type:**
        *colored*         *bool*                       boolean value of coloring
        ================= ============================ ========================================
        """ 
        self.colored = colored  
    
    
    @pyqtSlot(QtCore.QModelIndex,str,object)
    def update_path_dict(self, index, path, value): 
        """
        This function is made to update the path_dict when manually edited the tree.

        ================= ============================ ============================================
        **Arguments:**    **type:**
        *index*           *QtCore.QModelIndex*          index that has been edited
        *path*            *string*                      path of item for path_dict
        *value*           *int,float,str,bytes,any*     new value of item
        ================= ============================ ============================================
        """
        value_item = self.standard_model.itemFromIndex(index)
        #set item.text(), item.data()
        value_item.setText(str(value))
        #actualize path_dict
        self.path_dict[path]['data/value'] = value

    @pyqtSlot(dict)    
    def update_standard_model(self, changed_items):
        """
        Uses the `self.path_dict` to indicate the changed items in the model. Changes the item.text() and item.data().

        ================= ============================ ============================================
        **Arguments:**    **type:**
        *changed items*   *DeepDiff*                    dict of changes in the current dictionary
        ================= ============================ ============================================
        """
        #disconnect the items from everything
        self.standard_model.itemChanged.disconnect()
        #only when have been changed
        if changed_items != {}:
            #Catch Error when no file is opened but data collected (Globi) 
            if 'values_changed' in changed_items.keys():
                for i  in changed_items['values_changed']:
                    #take content from path_dict
                    value_index = self.path_dict[i]['value_index']
                    name_index = self.path_dict[i]['name_index']
                    #row = self.path_dict[i]['row']
                    #take new value from changed_items
                    new_value = changed_items['values_changed'][i]['new_value']
                    #take item from index
                    value_item = self.standard_model.itemFromIndex(value_index)
                    if self.colored == True:
                        value_item.setForeground(QtGui.QBrush(QtGui.QColor("magenta")))
                    #name_item = self.standard_model.itemFromIndex(name_index) 
                    #following would call itemChanged signal
                    value_item.setText(str(new_value))
                    #value_item.setData(new_value)
                    #actualize path_dict
                    self.path_dict[i]['data/value'] = new_value
        #reconnect itemChanged signal with Compare method
        self.standard_model.itemChanged.connect(self.comp.edit_item)


    
            

       
    


 