import geopandas
import matplotlib.pyplot as plt

# import GeoJSON data set
az = geopandas.read_file("Arizona_County_Boundaries.geojson")

# set index variable (querying 'area' will return area for each county name)
az = az.set_index("NAME")
# print(az.columns.tolist())

# add a new feature that was not included in the dataset
az['population'] = None

# data that will populate new feature
populations = {"APACHE"    :66021.0,
               "COCHISE"   :125447.0,
               "COCONINO"  :145101.0,
               "GREENLEE"  :9563.0,
               "MARICOPA"  :4420568.0,
               "MOHAVE"    :213267.0,
               "NAVAJO"    :106717.0,
               "PIMA"      :1043433.0,
               "PINAL"     :425264.0,
               "SANTA CRUZ":47669.0,
               "YAVAPAI"   :236209.0,
               "LA PAZ"    :16557.0,
               "YUMA"      :203881.0,
               "GILA"      :53272.0,
               "GRAHAM"    :38533.0}

# populate the new feature with values
for i in populations:
    az.at[i, "population"] = populations[i]


# add another new feature that was not included in the dataset
az['population_density'] = None
for i, dat in az.iterrows():
    az.at[i, "population_density"] = az.at[i, "population"] / az.at[i, "Area_Acres"]


fig, axs = plt.subplots(1, 3)
fig.suptitle("AZ County Size, Pop., Pop. Density")

axs[0].set_title("Area Acres")
az.plot(ax=axs[0], column='Area_Acres', cmap='viridis')

axs[1].set_title("Population")
az.plot(ax=axs[1], column='population', cmap='viridis')

axs[2].set_title("Population Density")
az.plot(ax=axs[2], column='population_density', cmap='viridis')

plt.show()

