import arcpy
home = r"C:\Users\Rdebbout\Downloads\SpatialData"
shp = arcpy.MakeFeatureLayer_management("{}/NHDPlus16/NHDWaterbodies.shp".format(home))
fldList = arcpy.ListFields(shp)
for fld in fldList:
    print fld.name
rows = arcpy.SearchCursor(shp)
row = rows.next()
totalSize = 0
recordsCounted = 0 
while row:
    totalSize += row.getValue('AREASQKM')
    recordsCounted += 1
    row = rows.next()
average = totalSize / recordsCounted

arcpy.Statistics_analysis("NHDWaterbodies_Layer", "./outTable.dbf", [["AREASQKM","MEAN"]])
