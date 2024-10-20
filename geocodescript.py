import pandas as pd
import googlemaps
import time

# Load the CSV file
file_path = 'litter-fine-data-2021-2023.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Initialize Google Maps Geocoding client
API_KEY = '{KEY}'  # Replace with your actual Google Maps API key
gmaps = googlemaps.Client(key=API_KEY)

# Function to geocode a location using Google Maps API
def geocode_location(location):
    try:
        geocode_result = gmaps.geocode(location + ", Dublin, Ireland")
        if geocode_result:
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            return lat, lng
        else:
            return None, None
    except Exception as e:
        print(f"Error geocoding {location}: {e}")
        return None, None

# Apply geocoding to the Location column
coordinates = []
for location in data['Location']:
    lat, lng = geocode_location(location)
    coordinates.append((lat, lng))
    time.sleep(0.1)  # Adding a small delay to avoid hitting rate limits

# Add the coordinates to the DataFrame
data[['Latitude', 'Longitude']] = pd.DataFrame(coordinates, index=data.index)

# Save the updated DataFrame to a new CSV
output_file_path = 'litter-fine-data-geocoded.csv'
data.to_csv(output_file_path, index=False)

print(f"Geocoded data saved to {output_file_path}")
