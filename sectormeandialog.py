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

# Module fuer den Sektorkreis
import math
import csv
try:
    from shapely.geometry import Point, Polygon
except ImportError:
    QMessageBox.warning( self, self.tr( "Sektormittelwert: Fehler" ), self.tr( "Python Modul shapely ist nicht installiert" ) )

# Module fuers Umprojizieren
try:
	import pyproj
except ImportError:
	QMessageBox.warning( self, self.tr( "Sektormittelwert: Fehler" ), self.tr( "Python Modul pyproj ist nicht installiert" ) )

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

        # KBS fuer das Umprojizieren definieren (Corine ist in 32632 abgelegt)
        self.wgs84 = pyproj.Proj("+init=EPSG:4326")
        self.utm32wgs84 = pyproj.Proj("+init=EPSG:32632")

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
        
    def saveCSV(self):
        # CSV Layer auslesen
        csvLayer = self.getVectorLayerByName(self.ui.InPoint.currentText())
        csvProvider = csvLayer.dataProvider()
        csvFeature = QgsFeature()
        csvAllAttrs = csvProvider.attributeIndexes()
        # fuer jedes Objekt eine Puffer anhand der Parameter xCoord, yCoord und distm erstellen
        # und in einen memory Layer schreiben
        pstation = [] ; pstlon =[] ; pstlat = [] ; pdistm = [] ; pxutm32 = [] ; pyutm32 = [] ; pisect0 = [] ; smean = [] ; wktfeatures = []
        # Fuer jede Station in der CSV Datei
        for feature in csvLayer.getFeatures():
            station = feature.attributes()[0]
            pstation.append(station)
            stlon = feature.attributes()[1]
            pstlon.append(stlon)
            stlat = feature.attributes()[2]
            pstlat.append(stlat)
            distm = feature.attributes()[3] 
            pdistm.append(distm)
            
            # stlon und stlat von WGS84 nach UTM32N WGS84 transformieren
            xutm32, yutm32 = pyproj.transform(self.wgs84, self.utm32wgs84, stlon, stlat)
            # Koordinate um Zonenzahl erweitern für die Ausgabe
            pxutm32.append(xutm32 + 32000000)
            pyutm32.append(yutm32)
            
            # Erzeugen des Mittelwertes ueber den Gesamtkreis
            # leeren Memorylayer erzeugen mit Radius [distm] um die Position [stx],[sty]
            vpoly = QgsVectorLayer("Polygon", "pointbuffer", "memory")
            pFeature = QgsFeature()
            pFeature.setGeometry(QgsGeometry.fromPoint(QgsPoint(xutm32, yutm32)).buffer(distm,5))
            pProvider = vpoly.dataProvider()
            pProvider.addFeatures( [pFeature] )
            vpoly.commitChanges()
            pStats = QgsZonalStatistics(vpoly, self.getRasterLayerByName( self.ui.InRast.currentText() ).source())
            pStats.calculateStatistics(None)
            vAllAttrs = pProvider.attributeIndexes()       
            for vfeat in vpoly.getFeatures():
                isect0 = vfeat.attributes()[2]
                pisect0.append(isect0)

            # Initialisiere Parameters für die Sektoren
            steps = 90 # subdivision of circle. The higher, the smoother it will be
            sectors = 12.0 # Anzahl der Sektoren (12 bedeutet 30 Grad pro Sektor)
            radius = distm # Kreisradius aus Steuerdatei 
            start = 345.0 # Start des Kreises in Degrees
            # FIXME: nicht exakt geschlossen
            end = 344.99999999 # Ende des Kreises in Degrees
            center = Point(xutm32, yutm32) # Koordinaten, umgerechnet aus WGS84 Koordinaten der Steuerdatei
        
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
            
            wktfeatures = []
            for x in xrange(0,int(sectors)):
                segment_vertices = []
            
                # first the center and first point
                segment_vertices.append(polar_point(center, xutm32, yutm32))
                segment_vertices.append(polar_point(center, start + x*sector_width,radius))
                
                # then the sector outline points
                for z in xrange(1, steps_per_sector):
                    segment_vertices.append((polar_point(center, start + x * sector_width + z * step_angle_width,radius)))
        
                # then again the center point to finish the polygon
                segment_vertices.append(polar_point(center, start + x * sector_width+sector_width,radius))
                segment_vertices.append(polar_point(center, xutm32, yutm32))
                sectorcircle = segment_vertices    
        
                # create circle features as WKT
                wktfeature  = Polygon(sectorcircle).wkt
                
            # Erzeugen von Mittelerten fuer 12 Sektoren
            # leeren Memorylayer erzeugen mit 12 Sektoren auf Basis von sectorCircle()
            spoly = QgsVectorLayer("Polygon", "pointbuffer", "memory")
            sFeature = QgsFeature()
            sFeature.setGeometry(QgsGeometry.fromWkt(wktfeature))
            sProvider = spoly.dataProvider()
            sProvider.addFeatures( [sFeature] )
            spoly.commitChanges()
            sStats = QgsZonalStatistics(spoly, self.getRasterLayerByName( self.ui.InRast.currentText() ).source())
            sStats.calculateStatistics(None)
            sAllAttrs = sProvider.attributeIndexes()
            # FIXME: Testen, was smean enthält
            for sfeat in spoly.getFeatures():
                smean_value = sfeat.attributes()[2]
                smean.append(smean_value)
                

        self.standortname = self.ui.InPoint.currentText()
        self.fileName = QFileDialog.getSaveFileName(self.iface.mainWindow(), "Save As", self.standortname + "_out.csv","Comma Separated Value (*.csv)")                

        # Ausgabe als CSV Datei mit einer Zeile für jede Station
        header = ['station', 'stlon', 'stlat',  'stx', 'sty',  'distm',  'isect0',  'isect1', 'isect2', 'isect3', 'isect4', 
        'isect5', 'isect6', 'isect7', 'isect8',  'isect9', 'isect10', 'isect11', 'isect12']
        with open(self.fileName, 'wb') as csvfile:
            datawriter = csv.writer(csvfile)		
            # schreibe Kopfzeile
            datawriter.writerow(header)
            # schreibe Daten
            for int1, fp1, fp2, fp3, fp4, int2, fp5, lst1 in zip(pstation, pstlon, pstlat, pxutm32, pyutm32, pdistm, pisect0, smean):
                datawriter.writerow((int1, fp1, fp2, fp3, fp4, int2, fp5, lst1))
