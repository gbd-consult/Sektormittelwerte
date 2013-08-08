sectormean
==========

Sektorgemittelter Parameter z0

Es wird die Datei corine2006_z0-utm.grid mit Werten des Parameters Rauigkeitslänge z0 in Meter vorgegeben. Diese Datenmatrix deckt ganz Deutschland ab. Das horizontale Gittermaß ist 100 m. Datengrundlage ist CORINE2006 in UTM32. Als Steuerung wird eine ASCII-Datei (bspw. mm_2012.dat) vorgegeben, die folgenden Aufbau hat:

:: 

	st, stlon, stlat, distm
	104320, 6.523752, 50.832055, 2000


* [st] ist eine Punktbezeichnung
* die Koordinaten [stlon], [stlat] sind in dezimalen Geograden angegeben
* die Distanz von diesem Punkt [distm] hat die Einheit Meter. 

Die Datei kann nur eine oder bis zu mehreren hundert Zeilen umfassen. Mit Bezug auf die Grafik in Datei Aufgabe_sector_z0.pdf soll eine Funktion unter QGIS erstellt werden, die je Steuerzeile ausgehend vom angegebenen Punkt [stlon], [stlat] einen 12-fach sektorierten Kreis erstellt mit dem Radius [distm]. Der Sektor 1 ist nord-zentriert. Für jeden der 12 Sektoren soll das (arithmetische) Flächenmittel des Parameters z0 der Datenmatrix bestimmt werden. Das Ergebnis soll in eine ASCII-Datei geschrieben werden, die gegenüber der Steuer-Datei den Namenszusatz '_out' erhält (mm_2012_out.dat).

::

	st, isect, sectz0
	104320, -1, 0.311
	104320, 1, 0.435
	104320, 2, 0.217

Bei dem Wert isect=-1 steht der Mittelwert über den gesamten Kreis.
