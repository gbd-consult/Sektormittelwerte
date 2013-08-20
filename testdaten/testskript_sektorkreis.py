from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from qgis.analysis import QgsZonalStatistics


import math
import csv
from shapely.geometry import Point, Polygon
import pyproj

# Initialisiere Parameters fuer die Sektoren
steps = 90 # subdivision of circle. The higher, the smoother it will be
sectors = 12.0 # Anzahl der Sektoren (12 bedeutet 30 Grad pro Sektor)
radius = 2000 # Kreisradius aus Steuerdatei 
start = 345.0 # Start des Kreises in Degrees
# FIXME: nicht exakt geschlossen
end = 344.99999999 # Ende des Kreises in Degrees
center = Point(32422073,5951502) # Koordinaten, umgerechnet aus WGS84 Koordinaten der Steuerdatei
  
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
    segment_vertices.append(polar_point(center, 32422073, 5951502))
    segment_vertices.append(polar_point(center, start + x*sector_width,radius))
                
    # then the sector outline points
    for z in xrange(1, steps_per_sector):
        segment_vertices.append((polar_point(center, start + x * sector_width + z * step_angle_width,radius)))
        
        # then again the center point to finish the polygon
        segment_vertices.append(polar_point(center, start + x * sector_width+sector_width,radius))
        segment_vertices.append(polar_point(center, 32422073,5951502))
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
    sStats = QgsZonalStatistics(spoly, "/home/dassau/arbeit/github/sectormean/testdaten/corine2006_z0_utm32.zip")
    sStats.calculateStatistics(None)
    sAllAttrs = sProvider.attributeIndexes()
    # FIXME: Testen, was smean enthaelt
    for sfeat in spoly.getFeatures():
        smean_value = sfeat.attributes()[2]
        smean.append(smean_value)
        print smean