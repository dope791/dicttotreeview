#Anleitung für den Nutzer von 'DictToTreeView'
#Erstelle eine Instanz von der Klasse 'DictToTreeView' und initialisiere diese mit deinem Dictionary und einer TreeView
#Verbinde dein Ausgangssignal der sich ändernden Daten mit dem Datensignal (data_sig) der Instanz DictToTreeView
#Verbinde das Outputsignal (output_sig) mit deiner Aktualisierungsmethode für das dictionary um die manuelle Datenänderung zu übernehmen
#Inkrementierung des Wertes bei ['ALINE']['e_SensorType'] 

import sys
sys.path.append('.')
from PyQt5 import QtWidgets
from usercode import DummySensor, MainWindow
from dicttotreeview import DictToTreeView 


from pprintpp import pprint as pp





if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()


    #dummy sensor
    ##########################################################################################################
    sensor = DummySensor()
    ##########################################################################################################

    #dicttotreeview 
    ##########################################################################################################
    myInstance = DictToTreeView(sensor.data_dict, window.TreeView, reset_column=True, highlight_changes=True)
    myInstance.tree.ShowPathColumn(True)#Flag for path column (4) 
    ##########################################################################################################
    
    #signals
    ##########################################################################################################
    sensor.sensor_data_sig.connect(myInstance.data_sig)#connect input data
    myInstance.output_sig.connect(sensor.update_dc)#connect output data

    window.ui.lineEdit.textChanged.connect(myInstance.tree.filter_model)#activate SearchingLine 
    ##########################################################################################################


    window.show() 
    sys.exit(app.exec_())

    


    

   
   
    

    

