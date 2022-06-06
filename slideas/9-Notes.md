https://darribas.org/gds_course/content/slides/block_D_iii.html#/choropleths (good content on classification)

etrs = world.to_crs('+proj=vandg +lon_0=0 +x_0=0 +y_0=0 +R_A +a=6371000 +b=6371000 +units=m +no_defs')
print("The CRS (projection) for this data is: {0}".format(etrs.crs))
fig, ax = plt.subplots(1,1,figsize=(10,10))
etrs.plot(ax=ax)

laea = world.to_crs('+proj=laea +lon_0=-74 +x_0=0 +y_0=0 +lat_0=40 +no_defs')
print("The CRS (projection) for this data is: {0}".format(etrs.crs))
fig, ax = plt.subplots(1,1,figsize=(10,10))
laea.plot(ax=ax)