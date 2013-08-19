#!/usr/bin/env python

###############################################################################
#
# MODULE:       
# AUTHOR:       Otto Dassau <dassau@gbd-consult.de>
# PURPOSE:	Create sector layer as shape file. Based on an idea by 
#		chriserik		
#
# COPYRIGHT:    (c) 2013 Otto Dassau - Geoinformatik Buero Dassau
#               This program is free software under the GNU General Public
#               License (>=v2) for details.
#
#               This program is distributed in the hope that it will be useful,
#               but WITHOUT ANY WARRANTY; without even the implied warranty of
#               MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#               GNU General Public License for more details.
###############################################################################

from shapely.geometry import Point, Polygon
import math
from osgeo import ogr

# initial parameters for segmentation
steps = 90 # subdivision of circle. The higher, the smoother it will be
sectors = 12.0 # number of sectors in the circle (12 means 30 degrees per sector)
radius = 90.0 # circle radius
start = 315.0 # start of circle in degrees
end = 45.0 # end of circle in degrees
center = Point(23,42)

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
    segment_vertices.append(polar_point(center, 0,0))
    segment_vertices.append(polar_point(center, start + x*sector_width,radius))

    # then the sector outline points
    for z in xrange(1, steps_per_sector):
        segment_vertices.append((polar_point(center, start + x * sector_width + z * step_angle_width,radius)))

    # then again the center point to finish the polygon
    segment_vertices.append(polar_point(center, start + x * sector_width+sector_width,radius))
    segment_vertices.append(polar_point(center, 0,0))
    #print segment_vertices
    
    # create feature as WKT
    features = Polygon(segment_vertices).wkt
    print features

## prepare geojson feature collection
#res = geojson.FeatureCollection(
    #features = features
#)

## write to file
#f = open('sector.json', 'w')
#f.write(geojson.dumps(res))
#f.close()


