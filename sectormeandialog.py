# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QGIS Plugin zur Ermittlung sektorgemittelter Rasterwerte
 -------------------
        begin                : 2013-08-09
        copyright            : (C) 2013 by Geoinformatikbüro Dassau GmbH
        email                : info@gbd-consult.de
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

import logging
# change level back to logging.WARNING(default) before release
logging.basicConfig(level=logging.WARNING)

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_sectormean import Ui_SectorMean

from qgis.core import *
from qgis.gui import *

# modules to create sector circle
import math, csv
import sector

class SectorMeanDialog(QtGui.QDialog):
    def __init__(self,  iface):
        # always put the plugin dialog on top
        QDialog.__init__(self,  None, Qt.WindowStaysOnTopHint)
        # Set up the user interface from Designer.
        self.ui = Ui_SectorMean()
        self.ui.setupUi(self)
        self.messagebar = QgsMessageBar()

        self.check_vector = True

        self.iface=iface
        self.canvas=self.iface.mapCanvas()
        self.layerRegistry = QgsMapLayerRegistry.instance()
        print self.layerRegistry
        self.zoneStatTool = QgsMapToolEmitPoint(self.canvas)

        # connect start/stop interaktive display
        QObject.connect(self.ui.checkBox,SIGNAL("stateChanged(int)"),self.changeActive)
        self.ui.checkBox.setCheckState(Qt.Unchecked)

        # connect layer list in plugin combobox
        QObject.connect(self.layerRegistry, SIGNAL("layerWasAdded(QgsMapLayer *)"), self.add_layer)
        QObject.connect(self.layerRegistry, SIGNAL("layerRemoved(QString)"), self.remove_layer)


        # connect speichern als CSV
        QObject.connect(self.ui.buttonSaveAs, SIGNAL("clicked()"), self.saveCSV)

        # load raster and point layer into combobox
        self.initVectorLayerCombobox( self.ui.InPoint, 'key_of_default_layer' )
        self.initRasterLayerCombobox( self.ui.InRast, 'key_of_default_layer' )

        # set radius (z0) to calculate mean for circle
        self.buffer = self.ui.bufferz0.value()

        # set progress bar to 0
        self.ui.progressBar.setValue(0)

    # (from value tool)
    def changeActive(self):
        if self.ui.checkBox.isChecked():
            self.canvas.setMapTool(self.zoneStatTool)
            self.zoneStatTool.canvasClicked.connect(self.listen_xCoordinates)
            self.zoneStatTool.canvasClicked.connect(self.listen_yCoordinates)
            self.zoneStatTool.canvasClicked.connect(self.listen_z0)
        else:
            self.canvas.unsetMapTool(self.zoneStatTool)

    # Anzeige der Werte an und aussetellen
    def changePlot(self):
        self.changeActive(self.ui.checkBox.checkState())

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
        mean = sector.bufferMean(QgsPoint(self.xCoord, self.yCoord), \
            self.getRasterLayerByName(self.ui.InRast.currentText()), \
            self.ui.bufferz0.value())
        if mean != -9999:
            self.ui.outputMean.setText("%.2f" % float(mean))
        else:
            self.ui.outputMean.setText("kein Wert")

    def add_layer(self, layerid):
        self.check_vector = False
        self.initVectorLayerCombobox( self.ui.InPoint, self.ui.InPoint.currentText() )
        self.initRasterLayerCombobox( self.ui.InRast, self.ui.InRast.currentText() )
        self.check_vector = True

    def remove_layer(self, layerid):
        self.check_vector = False
        self.ui.InRast.clear()
        self.ui.InPoint.clear()
        self.check_vector = True
        # Add the remaining layers
        layers = self.layerRegistry.mapLayers()
        for layer in layers:
            self.add_layer(layers[layer])

    def accept(self):
        # check input parameters
        if self.ui.InPoint.currentIndex()  == -1:
            QMessageBox.warning( self, self.tr( "Warnung" ),
                self.tr( "Bitte einen Punktlayer selektieren" ) )
            return
        if self.ui.InRast.currentIndex()  == -1:
            QMessageBox.warning( self, self.tr( "Warnung" ),
                self.tr( "Bitte einen Rasterlayer selektieren" ) )
            return

    # Return QgsMapLayer.RasterLayer (only gdal) from a layer name ( as string )
    def initRasterLayerCombobox(self, combobox, layerid):
        combobox.clear()
        reg = self.layerRegistry
        for ( key, layer ) in reg.mapLayers().iteritems():
            if layer.type() == QgsMapLayer.RasterLayer: combobox.addItem( layer.name(), key )
        idx = combobox.findData( layerid )
        if idx != -1:
            combobox.setCurrentIndex( idx )

    # Hole Liste geladener Rasterlayer
    def getRasterLayerByName( self,  myName ):
        layerMap = self.layerRegistry.mapLayers()
        for name, layer in layerMap.iteritems():
            if layer.type() == QgsMapLayer.RasterLayer and layer.name() == myName:
                if layer.isValid():
                    return layer
                else:
                    return None

    # Return QgsMapLayer.VectorLayer from a layer name ( as string )
    def initVectorLayerCombobox(self, combobox, default):
        combobox.clear()
        reg = self.layerRegistry
        for ( key, layer ) in reg.mapLayers().iteritems():
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Point: combobox.addItem( layer.name(), key )
        idx = combobox.findData( default )
        if idx != -1:
            combobox.setCurrentIndex( idx )

    def getVectorLayerByName( self,  myName ):
        layermap = self.layerRegistry.mapLayers()
        for name, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Point and layer.name() == myName:
                if layer.isValid():
                    return layer
                else:
                    return None

    def checkVectorLayer( self ):
        """
        Check if the vector layer has correct layout
        :return: False if the vector layer is incorrect 
        """
        if self.check_vector is False:
            return True
        csvLayer = self.getVectorLayerByName(self.ui.InPoint.currentText())
	if csvLayer:
            fields = csvLayer.pendingFields()
            field_names = [field.name() for field in fields]
            default = [u'st', u'stlon', u'stlat', u'distm']
            # Check if first field_names match with expected fieldnames
            if len(filter(lambda (a,b): a == b, zip(field_names,default))) != len(default):
                self.iface.messageBar().pushMessage("Error", "Standortdatei hat falsche Spaltennamen.", QgsMessageBar.CRITICAL, 5)
                return False
        return True

    # Rasterwert an Position
    def sampleRaster20(self, layer, x, y):
        ident = layer.dataProvider().identify(QgsPoint(x,y), QgsRaster.IdentifyFormatValue ).results()
        return ident[1]

    # Frage Wert für die Rasterlayer an Position [stx],[sty] ab
    def sampleRaster(self, raster_name, x, y):
        layer = self.getRasterLayerByName(raster_name)
        return self.sampleRaster20(layer, x, y)

    # generate data as csv table
    def saveCSV(self):
        """
        Save the result in a CSV file
        """
        if self.checkVectorLayer() is False:
            return

        # KBS fuer das Umprojizieren definieren (Corine ist in EPSG:32632 abgelegt)
        srcCrs = QgsCoordinateReferenceSystem("EPSG:4326")
        destCrs = QgsCoordinateReferenceSystem("EPSG:32632")
        transformer = QgsCoordinateTransform(srcCrs, destCrs)
        csvLayer = self.getVectorLayerByName(self.ui.InPoint.currentText())
        csvProvider = csvLayer.dataProvider()
        csvFeature = QgsFeature()
        csvAllAttrs = csvProvider.attributeIndexes()
        # Fortschrittbalken auf Basis der Stationen
        nFeat = csvProvider.featureCount()
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setRange(0, nFeat)
        nElement = 0
        # fuer jedes Objekt eine Puffer anhand der Parameter xCoord, yCoord und distm erstellen
        # und in einen memory Layer schreiben
        pstation = [] ; pstlon =[] ; pstlat = [] ; pdistm = [] ; pxutm32 = []
        pyutm32 = [] ; pisect0 = [] ; pisectx = []; phisect = []
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

            # Wert des Fortschrittbalkens setzen
            nElement += 1
            self.ui.progressBar.setValue(nElement)
            # stlon und stlat von WGS84 nach UTM32N WGS84 transformieren
            tp = transformer.transform(stlon, stlat)
            xutm32 = tp.x()
            yutm32 = tp.y()
            # Koordinate um Zonenzahl erweitern für die Ausgabe und auf nächste Ganzzahl runden
            pxutm32.append(math.trunc(xutm32) + 32000000)
            pyutm32.append(math.trunc(yutm32))

            # Initialisiere Parameters für die Sektoren
            steps = 90 # subdivision of circle. The higher, the smoother it will be
            sectors = 12 # Anzahl der Sektoren (12 bedeutet 30 Grad pro Sektor)
            radius = float(distm) # Kreisradius aus Steuerdatei  - distm
            center = QgsPoint(xutm32,yutm32) # Koordinaten, umgerechnet aus WGS84 Koordinaten der Steuerdatei
            raster = self.getRasterLayerByName(self.ui.InRast.currentText())

            # Sector 0 contains the mean of the whole circle
            mean_total = sector.bufferMean(center, raster, radius)
            pisect0.append(mean_total)

            # Sector 1 to n contain the mean for each sector
            mean_sector = sector.sectorMean(center, raster, radius, sectors, steps)
            pisectx.append(mean_sector)

            # values for weighted means
            phisect.append([float(x) for x in feature.attributes()[4::] if x])
                

        # Setze Fortschrittbalken wieder auf 0
        self.ui.progressBar.setValue(0)

        self.standortname = self.ui.InPoint.currentText()
        self.fileName = QFileDialog.getSaveFileName(self.ui, "Save As", self.standortname + "_out.csv","Comma Separated Value (*.csv)")

        # Quit if no output was selected
        if self.fileName != "":
            with open(self.fileName, 'wb') as csvfile:
                datawriter = csv.writer(csvfile)
                round_ = lambda x: round(x,2) # round to 2 decimal digits
                # Check if we have the correct number of hisect values for weighted output
                if reduce(lambda a, b: a & b, [len(a) == sectors for a in phisect], True):
                    header = ['station', 'stlon', 'stlat',  'stx', 'sty',  'distm'] \
                    + ['isect' + str(x) for x in range(13)] \
                    + ['hisect' + str(x) for x in range(1,13)] \
                    + ['wisect' + str(x) for x in range(1,13)] \
                    + ['sumsect']
                    # write table header
                    datawriter.writerow(header)
                    for int1, fp1, fp2, fp3, fp4, int2, fp5, lst1, lst2 in zip(pstation, pstlon, pstlat, pxutm32, pyutm32, pdistm, pisect0, pisectx, phisect):
                        wisect = [round(x * y,2) for (x,y) in zip(lst1, lst2)]
                        cols = [int1, fp1, fp2, fp3, fp4, int2, round_(fp5)] \
                        + map(round_, lst1) + map(round_, lst2) + wisect + [sum(wisect)]
                        datawriter.writerow(cols)
                else: # non weighted output
                    header = ['station', 'stlon', 'stlat',  'stx', 'sty',  'distm'] \
                    + ['isect' + str(x) for x in range(13)]
                    # write table header
                    datawriter.writerow(header)
                    for int1, fp1, fp2, fp3, fp4, int2, fp5, lst1 in zip(pstation, pstlon, pstlat, pxutm32, pyutm32, pdistm, pisect0, pisectx):
                        cols = [int1, fp1, fp2, fp3, fp4, int2, round_(fp5)] + map(round_, lst1)
                        datawriter.writerow(cols)
