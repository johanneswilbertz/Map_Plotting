# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 15:59:27 2022

Visualizee fires detected by satelites on a map.

@author: JohannesWilbertz
"""

import folium
import pandas as pd
import branca
import urllib
import os

def get_filename(url):
    """
    Parses filename from given url
    """
    if url.find('/'):
        return url.rsplit('/', 1)[1]

# Filepaths
outdir = r"C:\\Users\\JohannesWilbertz\\OneDrive - Ksilink\\Image-Data-Analysis\\Python\Map_Plotting\\Map_Plotting\\"

# File locations
url_list = ["https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Europe_24h.csv" ,
            "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Europe_48h.csv",
            "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Europe_7d.csv"
            ]

# Create folder if it does no exist
if not os.path.exists(outdir):
    os.makedirs(outdir)

# Download files
for url in url_list:
    # Parse filename
    fname = get_filename(url)
    outfp = os.path.join(outdir, fname)
    # Download the file if it does not exist already
    if not os.path.exists(outfp):
        print("Downloading", fname)
        r = urllib.request.urlretrieve(url, outfp)

# Read FIRMS data
df = pd.read_csv(outdir + "SUOMI_VIIRS_C2_Europe_24h.csv")

# Normalize brightness
df['bright_ti4'] =  df['bright_ti4']/df['bright_ti4'].max()

# Create a new map object
m = folium.Map(location=(47.5067, 34.5851), zoom_start=13)

# Go through each fire, make circle, and add to map.
for i in range(len(df)):
    if df.iloc[i]['bright_ti4'] > 0:
        folium.Circle(
            location=[df.iloc[i]['latitude'], df.iloc[i]['longitude']],
            radius=df.iloc[i]['bright_ti4'] * 250,
            weight=1,  # thickness of the border
            color='red',  # this is the color of the border
            opacity=1,  # this is the alpha for the border
            fill_color='red',  # fill is inside the circle
            fill_opacity=df.iloc[i]['bright_ti4'],  # we will make that less opaque so we can see layers

        ).add_to(m)

# # Create legend
# colormap =  branca.colormap.linear.YlOrRd_09.scale(0, 1)
# colormap = colormap.to_step(index=[0, 0.25, 0.5, 0.75, 1])
# colormap.caption = 'Normalized VIIRS signal ("Fire") brightness'
# colormap.add_to(m)

# Save map as html file
m.save('C:\\Users\\JohannesWilbertz\\OneDrive - Ksilink\\Image-Data-Analysis\\Python\Map_Plotting\\Map_Plotting\\FIRMS.html')