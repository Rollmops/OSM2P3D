import shapefile

shp = open('RDX7824.shp', 'rb')
dbf = open('RDX7824.dbf', 'rb')

r = shapefile.Reader(shp=shp, dbf=dbf)
shapes = r.shapes()
records = r.records()

assert(len(shapes) == len(records))

print shapes[0].shapeType
print shapes[0].points

shp.close()
dbf.close()