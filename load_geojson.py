import geopandas
import matplotlib.pyplot as plt

# import GeoJSON data set
az = geopandas.read_file("biotic_communities_AZ.geojson")

# set index variable (querying 'area' will return area for each FID)
az = az.set_index("FID")
print(az.columns.tolist())

print(az['AREA'])

# plot the area over the geometry
az.plot('AREA', legend=True)
plt.title("Geographic areas of AZ Biotic Communities")
plt.show()
