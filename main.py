import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def italy():

    url = 'https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_provinces.geojson'
    italy = gpd.read_file(url)

    pop_data = pd.read_csv('population.csv')
    pop_data['population'] = pop_data['population'].str.replace(',', '')
    pop_data['population'] = pop_data['population'].astype(int)

    # Convert italy GeoDataFrame to GeoSeries
    italy_geom = italy.geometry

    # Merge population data with italy GeoSeries
    italy_merged = pd.concat([italy_geom, pop_data], axis=1)

    # Convert merged data to GeoDataFrame
    italy_merged = gpd.GeoDataFrame(italy_merged, geometry='geometry')

    # Define the bins and labels for population ranges
    bins = [0, 50000, 100000, 150000, 200000, 250000, 300000, 400000, 500000, 1000000, 2000000, 2500000, 3000000]
    labels = ['< 50k', '50k-100k', '100k-150k', '150k-200k', '200k-250k', '250k-300k', '300k-400k', '400k-500k', '500k-1M', '1M-2M', "2.5M >"]

    # Create a colormap for the choropleth map
    cmap = plt.cm.YlGn

    # Normalize the colormap based on population density
    norm = colors.BoundaryNorm(bins, cmap.N)

    # Plot Italy with population density
    fig, ax = plt.subplots(figsize=(10, 10))
    italy_merged.plot(column='population', cmap=cmap, norm=norm, edgecolor='black', facecolor='#F0F0F0', ax=ax)

    # Create a custom legend for the choropleth map
    legend_elements = [plt.Rectangle((0, 0), 1, 1, color=cmap(norm(bins[i]))) for i in range(len(bins) - 1)]
    legend_labels = [f'{labels[i]}' for i in range(len(labels) - 1)]
    ax.legend(legend_elements, legend_labels, loc='upper right', fontsize='small', title='Population density \nof Italy in 2022')


    plt.show()
    plt.savefig('italy_population_density.png', dpi=300, bbox_inches='tight')

italy()