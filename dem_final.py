#      importing dependencies
import requests
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from io import BytesIO
#      importing custom functions and api_key
from custom_functions import display_map
from dotenv import load_dotenv
import os



st.title("Digital Elevation Model Downloader")

# map container
containter = st.container()
st.divider()
with st.expander("info"):
    st.text("Avilash's Project")

with st.sidebar:
    south_lat = st.number_input("Latitude (South) [-90,90]", min_value=-90.0, max_value=90.0, step=0.01, value=34.5)
    north_lat = st.number_input("Latitude (North) [-90,90]", min_value=-90.0, max_value=90.0, step=0.01, value=36.5)
    east_lon = st.number_input("Longitude (East) [-180,180]", min_value=-180.0, max_value=180.0, step=0.01, value=139.5)
    west_lon = st.number_input("Longitude (West) [-180,180]", min_value=-180.0, max_value=180.0, step=0.01, value=137.5)
    step = st.slider("Grid Line Spacing (degrees)", 0.1, 10.0, 0.5)

    if st.button("Show Map"):
        m = display_map(south_lat, north_lat, east_lon, west_lon, step)
        with containter:
            # Use st_folium to display the folium map
            st_data = st_folium(m, width=700, height=500, returned_objects=[])


    file_name_input = st.text_input("Filename: ", value = "raster")
    
    file_format = st.selectbox("File Format:", ('GeoTiff', 'Arc ASCII Grid', 'Erdas Imagine'), index=0)
    # Map file_format to file extension
    format_extension_map = {
        'GeoTiff': 'tif',
        'Arc ASCII Grid': 'asc',
        'Erdas Imagine': 'img'
    }
    file_format_extension = format_extension_map.get(file_format, 'tif')

    raster_dataset_selection = st.selectbox("Choose Global Raster Dataset:", ('SRTMGL3 (SRTM GL3 90m)',
                                                               'SRTMGL1 (SRTM GL1 30m)',
                                                               'SRTMGL1_E (SRTM GL1 Ellipsoidal 30m)',
                                                               'AW3D30 (ALOS World 3D 30m)',
                                                               'AW3D30_E (ALOS World 3D Ellipsoidal, 30m)',
                                                               'SRTM15Plus (Global Bathymetry SRTM15+ V2.1 500m)',
                                                               'NASADEM (NASADEM Global DEM)',
                                                               'COP30 (Copernicus Global DSM 30m)',
                                                               'COP90 (Copernicus Global DSM 90m)',
                                                               'EU_DTM (DTM 30m)',
                                                               'GEDI_L3 (DTM 1000m)',
                                                               'GEBCOIceTopo (Global Bathymetry 500m)',
                                                               'GEBCOSubIceTopo (Global Bathymetry 500m)'), index=0)
    # Map raster data source name to demtype for later use
    raster_type = raster_dataset_selection.split()[0]
    
    if st.button("Generate File"):
        load_dotenv()
        api_key=os.getenv("API_Key")
        url = f"https://portal.opentopography.org/API/globaldem?demtype={raster_type}&south={south_lat}&north={north_lat}&west={west_lon}&east={east_lon}&outputFormat={file_format}&API_Key={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            
            # Create an in-memory bytes buffer
            buffer = BytesIO(response.content)
            
            st.download_button(
                label="Download File",
                data=buffer,
                file_name=f'{file_name_input}.{file_format_extension}',
                mime='application/octet-stream'
            )
            
            st.success(f"File ready for download as {file_name_input}.{file_format_extension}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
