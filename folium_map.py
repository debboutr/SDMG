# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 14:05:48 2016

This is a script to walk through json file creation for foium map

@author: Rdebbout
"""
import sys
import pandas as pd
import geopandas as gpd
from datetime import datetime as dt
from StreamCat_functions import findUpstreamNpy
DL_dir = r'/home/rick/Downloads/SpatialData'
zone = '16'
lakes = gpd.GeoDataFrame.from_file('%s/NHDPlus%s/NHDWaterbodies.shp' % (DL_dir, zone)).to_crs({'init' :'epsg:5070'})
cats = gpd.GeoDataFrame.from_file('%s/NHDPlus%s/NHDCatchment.shp' % (DL_dir, zone)).to_crs({'init' :'epsg:5070'}) 
lookup = pd.read_csv('%s/lookupCOMS%s.csv' % (DL_dir, zone))
lks = gpd.GeoDataFrame()
bsn = gpd.GeoDataFrame()
miss = gpd.GeoDataFrame()
start = dt.now()
for idx, row in lookup.iterrows():
    lake = lakes.ix[lakes.COMID == row.wbCOMID]
    catbas = findUpstreamNpy(zone, int(row.catCOMID), DL_dir)
    basin = cats.ix[cats.FEATUREID.isin(catbas)]
    try: 
        diffgeom = lake['geometry'].difference(basin.unary_union.buffer(0))
        pct = diffgeom.area / lake.area * 100
        if pct.values[0] > 20:
            lks = pd.concat([lks, lake])
            bsn = pd.concat([bsn, basin])
            miss = pd.concat([miss, gpd.GeoDataFrame(data={'COMID': row.wbCOMID,'PCT': pct}, geometry=diffgeom)])
    except:
        print row.wbCOMID
        continue
print "Time to process loop: {}".format(dt.now()-start)
lks.to_crs({'init' :'epsg:4326'}).to_file(r"%s\lks.json" % DL_dir, driver="GeoJSON")
bsn.to_crs({'init' :'epsg:4326'}).to_file(r"%s\bsn.json" % DL_dir, driver="GeoJSON")
miss.to_crs({'init' :'epsg:4326'}).to_file(r"%s\miss.json" % DL_dir, driver="GeoJSON")

import folium


lat_Center = lks.unary_union.centroid.y
lon_Center = lks.unary_union.centroid.x

def color(pct):
    if pct <= 50:
        col='darkpurple'
    elif 50 < pct <= 75:
        col='pink'
    elif pct > 75:
        col='red'
    return col


f_map=folium.Map(location=[lat_Center , lon_Center],zoom_start=6,tiles="Stamen Terrain")
fg=folium.FeatureGroup(name="Lake Points")
for lat,lon,name,pct in zip(miss['geometry'].centroid.map(lambda p: p.y),miss['geometry'].centroid.map(lambda p: p.x),miss['COMID'],miss['PCT']):    
    fg.add_child(folium.Marker(location=[lat,lon],popup="NHD Waterbody COMID: %s" % int(name),
                                   icon=folium.Icon(icon_color='white', color=color(pct))))
f_map.add_child(fg)
f_map.add_child(folium.GeoJson(data=open(r'%s\lks.json' % DL_dir),
                name='NHD Lake',
                style_function=lambda x: {'fillColor':'blue', 
                                          'fill_opacity': 0.2, 
                                          'color':'none'}))
f_map.add_child(folium.GeoJson(data=open(r'%s\bsn.json' % DL_dir),
                name='Catchment Basin',
                style_function=lambda x: {'fillColor':'grey', 
                                          'fill_opacity': 0.74,
                                          'color':'white'}))
f_map.add_child(folium.GeoJson(data=open(r'%s\miss.json' % DL_dir),
                name='Missed Area',
                style_function=lambda x: {'fillColor':'red', 
                                          'fill_opacity': 0.2, 
                                          'color':'none'}))
f_map.add_child(folium.LayerControl())
f_map.save(outfile=r'%s\lakesPoint.html' % DL_dir)
