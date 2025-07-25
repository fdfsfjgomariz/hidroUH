# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ModelUHDialog
                                 A QGIS plugin
 PACOGOM METE DESCRIPCION
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2025-05-21
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Water and Environment Institute (INUAMA). University of Murcia
        email                : fjgomariz@um.es
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtGui import QIntValidator

#PACOGOM a ver para el filter
from qgis.core import QgsMapLayerProxyModel

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Model_UH_dialog_base.ui'))


class ModelUHDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ModelUHDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
      
        self.cb_invector.setFilters(QgsMapLayerProxyModel.HasGeometry)
        
        self.output2.setStorageMode(self.output2.StorageMode.GetDirectory)
        self.output2.fileChanged.connect(self.on_path_changed)
        
        self.ch_optimize.stateChanged.connect(self.msg_optimize_checkbox)

        self.lineEdit_interval.setValidator(QIntValidator())
        
        #routing:
        self.ch_routing.toggled.connect(self.cb_lc.setEnabled)    
        self.cb_lc.setEnabled(self.ch_routing.isChecked())
        self.cb_lc.setLayer(self.cb_invector.currentLayer())
        self.ch_routing.toggled.connect(self.cb_minl.setEnabled)    
        self.cb_minl.setEnabled(self.ch_routing.isChecked())
        self.cb_minl.setLayer(self.cb_invector.currentLayer())
        self.ch_routing.toggled.connect(self.cb_maxl.setEnabled)    
        self.cb_maxl.setEnabled(self.ch_routing.isChecked())
        self.cb_maxl.setLayer(self.cb_invector.currentLayer())
        self.ch_routing.toggled.connect(self.cb_X.setEnabled)    
        self.cb_X.setEnabled(self.ch_routing.isChecked())
        self.cb_X.setLayer(self.cb_invector.currentLayer())
        
    def on_path_changed(self):
        directorio = self.output2.filePath()
        print(f"Selected directory: {directorio}")

    def msg_optimize_checkbox(self, state):
        if state == 2:
        
            if self.input_Q.filePath() == '':
                QMessageBox.information(
                    self,
                    "Optimze stage",
                    "To perform the optimization it is mandatory to include a flow file with the same time window as the precipitation"
                )
                self.ch_optimize.nextCheckState()

