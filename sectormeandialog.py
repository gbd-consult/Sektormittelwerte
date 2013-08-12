# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SectorMeanDialog
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

# Hilfe: Benutzung zur Ausgabe von Variablen in einem Info-Fenster
# QMessageBox.information(None, "Info:", <variable>)

import logging
# Ändere den Level zurück auf logging.WARNING(default) vor dem Release
logging.basicConfig(level=logging.WARNING)

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_sectormean import Ui_SectorMean

from qgis.core import *
from qgis.gui import *

# für die Berechung des Mittelwertes
from qgis.analysis import QgsZonalStatistics

class SectorMeanDialog(QtGui.QDialog):
    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_SectorMean()
        self.ui.setupUi(self)
        
        # connect layer list in plugin combobox 
        QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("layerWasAdded(QgsMapLayer *)"), self.add_layer)
        QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("layerWillBeRemoved(QString)"), self.remove_layer)
        
        # Lade Rasterlayer in die Combobox
        self.initVectorLayerCombobox( self.ui.InPoint, 'key_of_default_layer' )
        self.initRasterLayerCombobox( self.ui.InRast, 'key_of_default_layer' )

    def add_layer(self, layerid):
        self.initVectorLayerCombobox( self.ui.InPoint, self.ui.InPoint.currentText() )
        self.initRasterLayerCombobox( self.ui.InRast, self.ui.InRast.currentText() )
    
    # FIXME: Das Löschen von Layern wird nicht richtig übernommen
    def remove_layer(self, layerid):
        layer = QgsMapLayerRegistry.instance().mapLayer(layerid)
        self.ui.InPoint.removeItem( self.ui.InPoint.findData( layer.name() ) )
        self.ui.InRast.removeItem( self.ui.InRast.findData( layer.name() ) )
    
    def accept(self):
        # check input parameters
        if self.ui.InPoint.currentIndex()  == -1:
            QMessageBox.warning( self, self.tr( "Warning" ),
                self.tr( "Please select Point layer" ) )
            return
        if self.ui.InRast.currentIndex()  == -1:
            QMessageBox.warning( self, self.tr( "Warning" ),
                self.tr( "Please select Raster layer" ) )
            return

    # Return QgsMapLayer.RasterLayer (only gdal) from a layer name ( as string )
    def initRasterLayerCombobox(self, combobox, layerid):
        combobox.clear()
        reg = QgsMapLayerRegistry.instance()
        for ( key, layer ) in reg.mapLayers().iteritems():
            if layer.type() == QgsMapLayer.RasterLayer: combobox.addItem( layer.name(), key )
         
        idx = combobox.findData( layerid )
        if idx != -1:
            combobox.setCurrentIndex( idx )

    # Hole Liste geladener Rasterlayer
    def getRasterLayerByName( self,  myName ):
        layerMap = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in layerMap.iteritems():
            if layer.type() == QgsMapLayer.RasterLayer and layer.name() == myName:
                if layer.isValid():
                    return layer
                else:
                    return None
                    
    # Return QgsMapLayer.VectorLayer from a layer name ( as string )
    def initVectorLayerCombobox(self, combobox, default):
        combobox.clear()
        reg = QgsMapLayerRegistry.instance()
        for ( key, layer ) in reg.mapLayers().iteritems():
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Point: combobox.addItem( layer.name(), key )
         
        idx = combobox.findData( default )
        if idx != -1:
            combobox.setCurrentIndex( idx ) 

    def getVectorLayerByName( myName ):
        layermap = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Point and layer.name() == myName:
                if layer.isValid():
                    return layer
                else:
                    return None
                    
    # Rasterwert an Position
    def sampleRaster20(self, layer, x, y):
        ident = layer.dataProvider().identify(QgsPoint(x,y), QgsRaster.IdentifyFormatValue ).results()
        return ident[1]
            
    # Frage Wert für die Rasterlayer an Position [stx],[sty] ab
    def sampleRaster(self, raster_name, x, y):
        layer = self.getRasterLayerByName(raster_name)
        return self.sampleRaster20(layer, x, y)
            
    def meanBuffer(self):
        # leeren Memorylayer erzeugen mit Puffer [distm] um die Position [stx],[sty]
        vpoly = QgsVectorLayer("Polygon", "pointbuffer", "memory")
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(self.xCoord, self.yCoord)).buffer(self.bufferz0.value(),5))
        provider = vpoly.dataProvider()
        provider.addFeatures( [feature] )
        vpoly.commitChanges()
        stats = QgsZonalStatistics(vpoly, self.getRasterLayerByName( self.InRastZ.currentText() ).source())
        stats.calculateStatistics(None)
        allAttrs = provider.attributeIndexes()       
        for feature in vpoly.getFeatures():
            mean_value = feature.attributes()[2]
            return mean_value

