import folium
from streamlit_folium import st_folium

def draw_grid(map_obj, bounds, step):
    south, west, north, east = bounds
    lat_lines = list(frange(south, north, step))
    lon_lines = list(frange(west, east, step))
    
    # Draw latitude lines within the bounds of the map
    for lat in lat_lines:
        if south <= lat <= north:
            folium.PolyLine([(lat, west), (lat, east)], color="blue", weight=0.3, opacity=0.5).add_to(map_obj)
            folium.Marker([lat, west], icon=folium.DivIcon(html=f'<div style="font-size: 10pt; color: black">{lat:.1f}°</div>')).add_to(map_obj)
            folium.Marker([lat, east], icon=folium.DivIcon(html=f'<div style="font-size: 10pt; color: black">{lat:.1f}°</div>')).add_to(map_obj)

    # Draw longitude lines within the bounds of the map
    for lon in lon_lines:
        if west <= lon <= east:
            folium.PolyLine([(south, lon), (north, lon)], color="blue", weight=0.3, opacity=0.5).add_to(map_obj)
            folium.Marker([south, lon], icon=folium.DivIcon(html=f'<div style="font-size: 10pt; color: black">{lon:.1f}°</div>')).add_to(map_obj)
            folium.Marker([north, lon], icon=folium.DivIcon(html=f'<div style="font-size: 10pt; color: black">{lon:.1f}°</div>')).add_to(map_obj)

def frange(start, stop, step):
    # Helper function to create range with float steps
    while start < stop:
        yield round(start, 6)
        start += step

def calculate_zoom_level(lat_delta, lon_delta):
    # Simple function to determine zoom level based on the size of the bounding box
    if lat_delta <= 0.1 and lon_delta <= 0.1:
        return 12
    elif lat_delta <= 0.5 and lon_delta <= 0.5:
        return 10
    elif lat_delta <= 1.0 and lon_delta <= 1.0:
        return 8
    elif lat_delta <= 5.0 and lon_delta <= 5.0:
        return 6
    else:
        return 4

def display_map(south_lat, north_lat, east_lon, west_lon, step):
    # Calculate the center of the bounding box
    center_lat = (north_lat + south_lat) / 2
    center_lon = (east_lon + west_lon) / 2

    # Create a folium map centered at the bounding box
    m = folium.Map(location=[center_lat, center_lon],
                   zoom_start = calculate_zoom_level(north_lat - south_lat, east_lon - west_lon),
                   tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',  # Esri Topo Map tiles
                   attr='Map data © Esri, DeLorme, NAVTEQ')

    # Add the bounding box rectangle to the map
    folium.Rectangle(
        bounds=[[south_lat, west_lon], [north_lat, east_lon]],
        color="red",
        fill=True,
        fill_opacity=0
    ).add_to(m)

    # Add grid lines
    draw_grid(m, [south_lat, west_lon, north_lat, east_lon], step)

    return m