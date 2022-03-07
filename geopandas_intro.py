import geopandas
import matplotlib.pyplot as plt

path_to_data = geopandas.datasets.get_path("nybb")
gdf = geopandas.read_file(path_to_data)

gdf = gdf.set_index("BoroName")

gdf["area"] = gdf.area
gdf['boundary'] = gdf.boundary
gdf['centroid'] = gdf.centroid

first_point = gdf['centroid'].iloc[0]
gdf['distance'] = gdf['centroid'].distance(first_point)
# gdf['distance'].mean()

gdf.plot("area", legend=True)
# gdf.explore("area", legend=False) # not supported by my current version of geopandas running on python3.6.8
plt.title("Geographic area of NY boroughs")
plt.show()

gdf = gdf.set_geometry("centroid")
gdf.plot("area", legend=True)
plt.title("Centroids of NY boroughs")
plt.show()

ax = gdf["geometry"].plot()
gdf["centroid"].plot(ax=ax, color="black")
plt.title("Centroids plotted over geometry")
plt.show()


gdf = gdf.set_geometry("geometry")
gdf["convex_hull"] = gdf.convex_hull
ax = gdf["convex_hull"].plot(alpha=.5)  # saving the first plot as an axis and setting alpha (transparency) to 0.5
gdf["boundary"].plot(ax=ax, color="white", linewidth=0.5) # passing the first plot and setting linewitdth to 0.5
plt.title("Convex hulls plotted over geometry")
plt.show()


# buffering the active geometry by 10 000 feet (geometry is already in feet)
gdf["buffered"] = gdf.buffer(10000)
# buffering the centroid geometry by 10 000 feet (geometry is already in feet)
gdf["buffered_centroid"] = gdf["centroid"].buffer(10000)

ax = gdf["buffered"].plot(alpha=0.5)
gdf["buffered_centroid"].plot(ax=ax, color="red", alpha=0.5)
gdf["boundary"].plot(ax=ax, color="white", linewidth=0.5)
plt.title("10,000ft buffer around centroids and convex hull")
plt.show()


# get a polygon of Brooklyn
brooklyn = gdf.loc["Brooklyn", "geometry"]
print("Boroughs within 10k ft of Brooklyn: ", gdf["buffered"].intersects(brooklyn))


gdf["within"] = gdf["buffered_centroid"].within(gdf) #per record check if centroid within current geometry
gdf = gdf.set_geometry("buffered_centroid")
ax = gdf.plot("within", legend=True, categorical=True, legend_kwds={'loc':"upper left"}) # using categorical plot and setting the position of the legend
gdf["boundary"].plot(ax=ax, color="black", linewidth=0.5) # passing the first plot and setting linewitdth to 0.5
plt.title("Boundaries >10,000ft from respective centroid")
plt.show()

print("\nCurrent Coordinate Reference System (CRS): ", gdf.crs)

gdf = gdf.set_geometry("geometry")
boroughs_4326 = gdf.to_crs("EPSG:4326")
boroughs_4326.plot()
print("\nNew Coordinate Reference System (CRS): ", gdf.crs)
plt.title("New Coordinate Reference System")
plt.show()

