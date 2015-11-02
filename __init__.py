# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SectorMean
                                 A QGIS plugin
 Ermittlung sektorgemittelter Rasterwerte
                             -------------------
        begin                : 2013-08-09
        copyright            : (C) 2013 by Geoinformatikbuero Dassau GmbH
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
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "Sektormittelwerte"


def description():
    return "Ermittlung sektorgemittelter Rasterwerte"


def version():
    return "Version 0.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "2.0"

def author():
    return "Otto Dassau"

def email():
    return "dassau@gbd-consult.de"

def classFactory(iface):
    # load SectorMean class from file SectorMean
    from sectormean import SectorMean
    return SectorMean(iface)
