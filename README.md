Sektormittelwerte
=================

Sektorgemittelter Parameter z0
------------------------------


Es wird die Datei corine2006_z0-utm.grid mit Werten des Parameters Rauigkeitslänge z0 in Meter vorgegeben. Diese Datenmatrix deckt ganz Deutschland ab. Das horizontale Gittermaß ist 100 m. Datengrundlage ist CORINE2006 in UTM32. Als Steuerung wird eine ASCII-Datei (bspw. mm_2012.dat) vorgegeben, die folgenden Aufbau hat:


	st, stlon, stlat, distm
	104320, 6.523752, 50.832055, 2000


* [st] ist eine Punktbezeichnung
* die Koordinaten [stlon], [stlat] sind in dezimalen Geograden angegeben
* die Distanz von diesem Punkt [distm] hat die Einheit Meter.

Die Datei kann nur eine oder bis zu mehreren hundert Zeilen umfassen. Mit Bezug auf die Grafik in Datei Aufgabe_sector_z0.pdf soll eine Funktion unter QGIS erstellt werden, die je Steuerzeile ausgehend vom angegebenen Punkt [stlon], [stlat] einen 12-fach sektorierten Kreis erstellt mit dem Radius [distm]. Der Sektor 1 ist nord-zentriert. Für jeden der 12 Sektoren soll das (arithmetische) Flächenmittel des Parameters z0 der Datenmatrix bestimmt werden. Das Ergebnis soll in eine ASCII-Datei geschrieben werden, die gegenüber der Steuer-Datei den Namenszusatz '_out' erhält (mm_2012_out.dat)._


	st, isect, sectz0
	104320, -1, 0.311
	104320, 1, 0.435
	104320, 2, 0.217

Bei dem Wert isect=-1 steht der Mittelwert über den gesamten Kreis.

Installation
------------

Das Plugin wird über das [Plugin Repository der Geoinformatikbüro Dassau GmbH](https://plugins.gbd-consult.de) bereitgestellt. Sie können das Repository über den QGIS Pluginmanager einbinden.

<img src="/images/repodetails.png" width="300">

Das Plugin selbst ist ein Dock Widget und kann über das Menü Ansicht -> Bedienfelder geladen werden.


Bedienung
---------
## Wenn Sie das Sektormittelwerte-Tool geöffnet haben, finden Sie folgendes Fenster vor:

## <img src="/images/sektor_blank.png" width="300">

Ein Beispieldatensatz mit einem QGIS Projekt ist im Ordner [testdaten](./testdaten) abgelegt.

## <img src="/images/sektor_filled.png" width="300">


Das Plugin wurde zuletzt im Juli 2019 aktualisiert.

## Lizenz

Dieses Programm ist freie Software. Es kann unter der den Bedingungen der [GNU General Public License](./LICENSE) weitergegeben und/oder verändert werden. Entweder unter der Version 2 oder einer späteren Version der GPL.
