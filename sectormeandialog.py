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
# aendere den Level zurück auf logging.WARNING(default) vor dem Release
logging.basicConfig(level=logging.WARNING)

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_sectormean import Ui_SectorMean

from qgis.core import *
from qgis.gui import *

# fuer die Berechung des Mittelwertes
from qgis.analysis import QgsZonalStatistics

# fuer den Sektorkreis
from shapely.geometry import Point, Polygon
import math
import csv

class SectorMeanDialog(QtGui.QDialog):
    def __init__(self,  iface):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_SectorMean()
        self.ui.setupUi(self)
        
        self.iface=iface
        self.canvas=self.iface.mapCanvas()
              
        # connect layer list in plugin combobox 
        QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("layerWasAdded(QgsMapLayer *)"), self.add_layer)
        QObject.connect(QgsMapLayerRegistry.instance(), SIGNAL("layerWillBeRemoved(QString)"), self.remove_layer)
        
        # connect Interaktive Anzeige starten/stoppen
        QObject.connect(self.ui.cbxActive,SIGNAL("stateChanged(int)"),self.changeActive)
        
        # Immer im nicht aktivierten Modus starten
        self.ui.cbxActive.setCheckState(Qt.Unchecked)
        
        # connect speichern als CSV
        QObject.connect(self.ui.buttonSaveAs, SIGNAL("clicked()"), self.saveCSV)

        # Lade Rasterlayer in die Combobox
        self.initVectorLayerCombobox( self.ui.InPoint, 'key_of_default_layer' )
        self.initRasterLayerCombobox( self.ui.InRast, 'key_of_default_layer' )

        # Setze Radius (z0) für die Berechnung der Mittelwertes des Gesamtkreises
        self.buffer = self.ui.bufferz0.value()

    # (from value tool)
    def changeActive(self):
        if self.ui.cbxActive.isChecked():
            QObject.connect(self.canvas, SIGNAL("xyCoordinates(const QgsPoint &)"), self.listen_xCoordinates)
            QObject.connect(self.canvas, SIGNAL("xyCoordinates(const QgsPoint &)"), self.listen_yCoordinates)
            QObject.connect(self.canvas, SIGNAL("xyCoordinates(const QgsPoint &)"), self.listen_z0)           
        else:
            QObject.disconnect(self.canvas, SIGNAL("xyCoordinates(const QgsPoint &)"), self.listen_xCoordinates)
            QObject.disconnect(self.canvas, SIGNAL("xyCoordinates(const QgsPoint &)"), self.listen_yCoordinates)
            QObject.disconnect(self.canvas, SIGNAL("xyCoordinates(const QgsPoint &)"), self.listen_z0)

    # Anzeige der Werte an und aussetellen
    def changePlot(self):
        self.changeActive(self.ui.cbxActive.checkState())
        
    # Gebe X-Koordinate an Mousepositon aus und überschreibe vorherige (append ergänzt)
    def listen_xCoordinates(self, point):
        if point.x():
            x = point.x()
            self.ui.outputXEdit.setText("%d" % (x))
            self.xCoord = x
    
    # Gebe Y-Koordinate an Mouseposition aus und überschreibe Vorherige (append ergänzt)
    def listen_yCoordinates(self, point):
        if point.y():
            y = point.y()
            self.ui.outputYEdit.setText("%d" % (y))
            self.yCoord = y
            
    # Gebe Mittelwert der Rauhigkeit an Mousepositon aus und überschreibe vorherige (append ergänzt)
    def listen_z0(self, point):
         mean = float(self.meanBuffer())
         self.ui.outputMean.setText("%.2f" % (mean))

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

    def getVectorLayerByName( self,  myName ):
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

    # Berechne Mittelwert fuer Gesamtkreis an Mouseposition 
    def meanBuffer(self):
        # leeren Memorylayer erzeugen für den Puffer z0 um die Mousepoition
        vpoly = QgsVectorLayer("Polygon", "pointbuffer", "memory")
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(self.xCoord, self.yCoord)).buffer(self.ui.bufferz0.value(),5))
        provider = vpoly.dataProvider()
        provider.addFeatures( [feature] )
        vpoly.commitChanges()
        stats = QgsZonalStatistics(vpoly, self.getRasterLayerByName( self.ui.InRast.currentText() ).source())
        stats.calculateStatistics(None)
        allAttrs = provider.attributeIndexes()       
        for feature in vpoly.getFeatures():
            mean_value = feature.attributes()[2]
            return mean_value

    # Erstelle einen Kreis aus 12 Sektoren
    def sectorCircle(self):  
        # Initialisiere Parameters für die Sektoren
        steps = 90 # subdivision of circle. The higher, the smoother it will be
        sectors = 12.0 # number of sectors in the circle (12 means 30 degrees per sector)
        radius = distm # circle radius
        start = 345.0 # start of circle in degrees
        # FIXME: nicht exakt geschlossen
        end = 344.99999999 # end of circle in degrees
        center = Point(xCoord, yCoord)
        
        # prepare parameters
        if start > end:
            start = start - 360
        else:
            pass
        step_angle_width = (end-start) / steps
        sector_width = (end-start) / sectors
        steps_per_sector = int(math.ceil(steps / sectors))
        
        # helper function to calculate point from relative polar coordinates (degrees)
        def polar_point(origin_point, angle,  distance):
            return [origin_point.x + math.sin(math.radians(angle)) * distance, origin_point.y + math.cos(math.radians(angle)) * distance]
        
        features = []
        for x in xrange(0,int(sectors)):
            segment_vertices = []
        
        # first the center and first point
        segment_vertices.append(polar_point(center, xCoord, yCoord))
        segment_vertices.append(polar_point(center, start + x*sector_width,radius))
        
        # then the sector outline points
        for z in xrange(1, steps_per_sector):
            segment_vertices.append((polar_point(center, start + x * sector_width + z * step_angle_width,radius)))
        
        # then again the center point to finish the polygon
        segment_vertices.append(polar_point(center, start + x * sector_width+sector_width,radius))
        segment_vertices.append(polar_point(center, xCoord, yCoord))
        sectorcircle = segment_vertices
        return sectorcircle
        
    def saveCSV(self):
        # CSV Layer auslesen
        csvLayer = self.getVectorLayerByName(self.ui.InPoint.currentText())
        csvProvider = csvLayer.dataProvider()
        csvFeature = QgsFeature()
        csvAllAttrs = csvProvider.attributeIndexes()
        # fuer jedes Objekt eine Puffer anhand der Parameter xCoord, yCoord und distm erstellen
        # und in einen memory Layer schreiben
        pmean = [] ; psektnr = [] ; pstation = []
        smean = []
        kreisnr = -1
        for feature in csvLayer.getFeatures():
            self.station = feature.attributes()[0]
            self.xCoord = feature.attributes()[1]
            self.yCoord = feature.attributes()[2]
            self.distm = feature.attributes()[3]         

            # Erzeugen des Mittelwertes ueber den Gesamtkreis
            # leeren Memorylayer erzeugen mit Radius [distm] um die Position [stx],[sty]
            vpoly = QgsVectorLayer("Polygon", "pointbuffer", "memory")
            pFeature = QgsFeature()
            pFeature.setGeometry(QgsGeometry.fromPoint(QgsPoint(self.xCoord, self.yCoord)).buffer(self.distm,5))
            pProvider = vpoly.dataProvider()
            pProvider.addFeatures( [pFeature] )
            vpoly.commitChanges()
            pStats = QgsZonalStatistics(vpoly, self.getRasterLayerByName( self.ui.InRast.currentText() ).source())
            pStats.calculateStatistics(None)
            vAllAttrs = pProvider.attributeIndexes()       
            for vfeat in vpoly.getFeatures():
                pmean_value = vfeat.attributes()[2]
                pmean.append(pmean_value)
                pstation.append(self.station)
                psektnr.append(kreisnr)

#            # Erzeugen von Mittelerten fuer 12 Sektoren
#            # leeren Memorylayer erzeugen mit 12 Sektoren, dem Radius [distm] um die Position [stx],[sty]
#            spoly = QgsVectorLayer("Polygon", "pointbuffer", "memory")
#            sFeature = QgsFeature()
#            #sfeature.setGeometry(QgsGeometry.fromPoint(QgsPoint(xCoord, yCoord)).buffer(distm,5))
#            sProvider = spoly.dataProvider()
#            sProvider.addFeatures( [sFeature] )
#            spoly.commitChanges()
#            sStats = QgsZonalStatistics(spoly, self.getRasterLayerByName( self.ui.InRast.currentText() ).source())
#            sStats.calculateStatistics(None)
#            sAllAttrs = sProvider.attributeIndexes()       
#            for sfeat in spoly.getFeatures():
#                smean_value = sfeat.attributes()[2]
#                smean.append(smean_value)
#                stat.append(station)

        self.standortname = self.ui.InPoint.currentText()
        self.fileName = QFileDialog.getSaveFileName(self.iface.mainWindow(), "Save As", self.standortname + "_out.csv","Comma Separated Value (*.csv)")                

        # Test: Ausgabe als CSV
        with open(self.fileName, 'wb') as csvfile:
            datawriter = csv.writer(csvfile)
            for int1, int2, fp1 in zip(pstation, psektnr,  pmean):
                datawriter.writerow((int1, int2, fp1))
