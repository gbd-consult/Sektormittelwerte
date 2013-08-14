# Buffer CSV Layers and write to csv

from PyQt4.QtGui import *  
import qgis.analysis
import csv

pLayer = iface.activeLayer()
pProvider = pLayer.dataProvider()
feature = QgsFeature()
AllAttrs = pProvider.attributeIndexes()
feature = QgsFeature()
mean = [] ; sektnr = [] ; stat = [] # ; rwert = [] ; hwert = [] ; distanz = []
kreisnr = -1
for feature in pLayer.getFeatures():
    station = feature.attributes()[0]
    xCoord = feature.attributes()[1]
    yCoord = feature.attributes()[2]
    distm = feature.attributes()[3]
    print station, xCoord, yCoord, distm
    vpoly = QgsVectorLayer("Polygon", "pointbuffer", "memory")
    feature = QgsFeature()
    feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(xCoord,yCoord)).buffer(distm,5))
    provider = vpoly.dataProvider()
    provider.addFeatures( [feature] )
    vpoly.commitChanges()
    stats = qgis.analysis.QgsZonalStatistics(vpoly,"/arbeit/github/sectormean/testdaten/corine2006_z0_test.tif")
    stats.calculateStatistics(None)
    allAttrs = provider.attributeIndexes()       
    for vfeat in vpoly.getFeatures():
        mean_value = vfeat.attributes()[2]
        mean.append(mean_value)
        stat.append(station)
        sektnr.append(kreisnr)
        # rwert.append()
        # hwert.append()
        # distanz.append()
               
with open('/home/dassau/output.csv', 'wb') as csvfile:
    datawriter = csv.writer(csvfile)
    for int1, int2, fp1 in zip(stat, sektnr, mean):
        datawriter.writerow((int1, int2, fp1))
            