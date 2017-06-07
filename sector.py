from qgis.core import *
from qgis.analysis import QgsZonalStatistics
from PyQt4.QtCore import QVariant
import math

def generateSectors(point, n, substeps, radius):
    """Generate Sectors for a study side. Returns a QgsVectorLayer

    arguments:
    point       : source point of sector generation (QgsPoint)
    n           : number of sectors to generate
    substeps    : Number of substeps used to render the outer edge of each sector
    radius      : radius of the resulting Sectors
    """
    step = 360.0 / n
    # Start with the north facing sector
    offset = step / 2 + 90

    layer = QgsVectorLayer("Polygon?crs=epsg:4326", "pointbuffer", "memory")
    layer.startEditing()
    layer.addAttribute(QgsField("sectorID", QVariant.Int))

    for i in range(n):
        step_size = (((i + 1) * step) - (i * step)) / float(substeps)
        angles = [ ((i * step) + (x * step_size) + offset) % 360 for x in range(substeps + 1)] 

        poly = [point]
        for a in angles:
            x = (math.cos(math.radians(a)) * radius) + point.x()
            y = (math.sin(math.radians(a)) * radius) + point.y()
            poly.append(QgsPoint(x,y))

        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPolygon([poly]))
        feat.setAttributes([(n - i)])
        layer.addFeatures([feat])
    layer.commitChanges()
    layer.updateExtents()
    return layer

def sectorMean(point, raster, radius, n, substeps):
    """Calculate Sector Statistics for a study site, returns a list of mean values

    arguments:
    point   : coordinates of the study site (QgsPoint)
    raster  : raster source layer
    radius  : radius for the sectors
    n           : number of sectors to generate
    substeps    : Number of substeps used to render the outer edge of each sector
    """
    layer = generateSectors(point, n, substeps, radius)
    stats = QgsZonalStatistics(layer, raster.source())
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

def bufferMean(point, raster, radius):
    """Calculate Buffer Statistics for a study site, returns the mean value

    arguments:
    point   : coordinates of the study site (QgsPoint)
    raster  : raster source layer
    radius  : radius of the buffer
    """
    layer = QgsVectorLayer("Polygon?crs=epsg:4326", "pointbuffer", "memory")
    layer.startEditing()
    feat = QgsFeature()
    feat.setGeometry(QgsGeometry.fromPoint(point).buffer(radius,5))
    layer.addFeature(feat)
    layer.commitChanges()
    layer.updateExtents()
    stats = QgsZonalStatistics(layer, raster.source())
    stats.calculateStatistics(None)

    for f in layer.getFeatures():
        if f.attributes()[2] is not None:
            return f.attributes()[2]
            # always format with 2 decimals
            #return '{:.2f}'.format(round(f.attributes()[2],  2))
        else:
            # if NoData, set to -9999
            return -9999
