import pandas as pd
import folium
from folium.plugins import HeatMap

# Load the geocoded CSV file
file_path = 'litter-fine-data-geocoded.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Initialize a folium map centered around Dublin
dublin_coords = [53.3498, -6.2603]  # Coordinates for Dublin
map_dublin = folium.Map(location=dublin_coords, zoom_start=12)

# Add points to the map
points_added = 0
for _, row in data.iterrows():
    if not pd.isna(row['Latitude']) and not pd.isna(row['Longitude']):
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(row['Location'] + '<br>(Issue Date: ' + row['Issue_Date'].replace(' 00:00', '') + ')', max_width=200),
            icon=folium.Icon(color='blue', icon='glyphicon-trash')
        ).add_to(map_dublin)
        points_added += 1

# Optionally, add a heatmap to visualize density of points
heat_data = [[row['Latitude'], row['Longitude']] for _, row in data.iterrows() if not pd.isna(row['Latitude']) and not pd.isna(row['Longitude'])]
HeatMap(heat_data).add_to(map_dublin)

# Save the map to an HTML file
output_file_path = 'index.html'
map_dublin.save(output_file_path)

print(f"Map saved to {output_file_path} with {points_added} points")
