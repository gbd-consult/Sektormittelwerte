# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Sektormittelwerte
                                 A QGIS plugin
 Ermittlung sektorgemittelter Rasterwerte
                              -------------------
        begin                : 2013-08-09
        copyright            : (C) 2013 by Otto Dassau
        email                : dassau@gbd-consult.de
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from sectormeandialog import SectorMeanDialog
import os.path


class SectorMean:
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'sectormean_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = SectorMeanDialog(self.iface)

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/sectormean/icon.png"),
            u"Sektorgemittelte Rasterwerte", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # check if Raster menu available
        if hasattr(self.iface, "addPluginToRasterMenu"):
            # Raster menu and toolbar available
            self.iface.addRasterToolBarIcon(self.action)
            self.iface.addPluginToRasterMenu("&Argusoft", self.action)
        else:
            # there is no Raster menu, place plugin under Plugins menu as usual
            self.iface.addToolBarIcon(self.action)
            self.iface.addPluginToMenu("&Argusoft", self.action)

    def unload(self):
        # check if Raster menu available and remove our buttons from appropriate
        # menu and toolbar
        if hasattr(self.iface, "addPluginToRasterMenu"):
            self.iface.removePluginRasterMenu("&Argusoft",self.action)
            self.iface.removeRasterToolBarIcon(self.action)
        else:
            self.iface.removePluginMenu("&Argusoft",self.action)
            self.iface.removeToolBarIcon(self.action) 
    
    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass
