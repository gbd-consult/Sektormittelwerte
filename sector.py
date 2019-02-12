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

from qgis.core import *
from qgis.analysis import QgsZonalStatistics
from PyQt5.QtCore import QVariant
import math

def generateSectors(point, n, substeps, radius, authid):
    """Generate Sectors for a study side. Returns a QgsVectorLayer

    arguments:
    point       : source point of sector generation (QgsPointXY)
    n           : number of sectors to generate
    substeps    : Number of substeps used to render the outer edge of each sector
    radius      : radius of the resulting Sectors
    authid  : id of the Projects CRS
    """
    step = 360.0 / n
    # Start with the north facing sector
    offset = step / 2 + 90

    #layer = QgsVectorLayer("Polygon?crs=epsg:4326", "pointbuffer", "memory")
    layer = QgsVectorLayer("Polygon?crs=%s" % authid,  "pointbuffer", "memory")
    layer.startEditing()
    layer.addAttribute(QgsField("sectorID", QVariant.Int))

    for i in range(n):
        step_size = (((i + 1) * step) - (i * step)) / float(substeps)
        angles = [ ((i * step) + (x * step_size) + offset) % 360 for x in range(substeps + 1)] 

        poly = [point]
        for a in angles:
            x = (math.cos(math.radians(a)) * radius) + point.x()
            y = (math.sin(math.radians(a)) * radius) + point.y()
            poly.append(QgsPointXY(x,y))

        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPolygonXY([poly]))
        feat.setAttributes([(n - i)])
        layer.addFeatures([feat])
    layer.commitChanges()
    layer.updateExtents()
    return layer

def sectorMean(point, raster, radius, n, substeps, authid):
    """Calculate Sector Statistics for a study site, returns a list of mean values

    arguments:
    point   : coordinates of the study site (QgsPointXY)
    raster  : raster source layer
    radius  : radius for the sectors
    n           : number of sectors to generate
    substeps    : Number of substeps used to render the outer edge of each sector
    authid  : id of the Projects CRS
    """
    layer = generateSectors(point, n, substeps, radius, authid)
    stats = QgsZonalStatistics(layer, raster)
    stats.calculateStatistics(None)
    mean = []
    for sfeat in layer.getFeatures():
        # Wert auf 2 Nachkommastellen runden und NoData auf -9999 setzen
        if sfeat.attributes()[3] is not None:
            # always format with 2 decimals
            #mean_value = '{:.2f}'.format(round(sfeat.attributes()[3],  2))
            mean_value = sfeat.attributes()[3]
        else:
            mean_value = -9999
        mean.append(mean_value)
    return mean

def bufferMean(point, raster, radius, authid):
    """Calculate Buffer Statistics for a study site, returns the mean value

    arguments:
    point   : coordinates of the study site (QgsPointXY)
    raster  : raster source layer
    radius  : radius of the buffer
    authid  : id of the Projects CRS
    """
    #layer = QgsVectorLayer("Polygon?crs=epsg:4326", "pointbuffer", "memory")
    layer = QgsVectorLayer("Polygon?crs=%s" % authid,  "pointbuffer", "memory")
    layer.startEditing()
    feat = QgsFeature()
    feat.setGeometry(QgsGeometry.fromPointXY(point).buffer(radius,5))
    layer.addFeature(feat)
    layer.commitChanges()
    layer.updateExtents()
    stats = QgsZonalStatistics(layer, raster)
    stats.calculateStatistics(None)

    for f in layer.getFeatures():
        if f.attributes()[2] is not None:
            return f.attributes()[2]
            # always format with 2 decimals
            #return '{:.2f}'.format(round(f.attributes()[2],  2))
        else:
            # if NoData, set to -9999
            return -9999
