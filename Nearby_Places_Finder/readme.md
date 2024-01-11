# Nearby Places Finder

# Nearby Places Finder

This project includes a Python script and a Streamlit web application that allow users to find nearby places based on a specified location, radius, and optional place type using the Google Places API.

## Prerequisites

- You need a Google Maps API key to use these scripts. Obtain one from the [Google Cloud Console](https://console.cloud.google.com/).
- Ensure you have the required Python libraries installed by running:
  ```bash
  pip install requests streamlit folium

# Python Script
Replace YOUR_GOOGLE_MAPS_API_KEY in the nearby_places_finder.py script with your actual API key.

## Example usage:

You will be prompted to enter the location, radius, and specific type of place. Press Enter for default values (5km radius and all places).

Enter the location: Lake view, Bhopal
Enter the radius in kilometers (press Enter for default 5km): 2
Enter the specific type of place (press Enter for all places): Restaurant

### The script will then display the nearby places based on the provided inputs.


# Streamlit Web Application

- Ensure the required Python libraries are installed by running:
- ```bash
  pip install requests streamlit folium
# Replace YOUR_GOOGLE_MAPS_API_KEY in the nearby_places_finder.py script with your actual API key.
```bash
- streamlit run streamlit_nearby.py

# Access the app through your web browser and enter the location, radius, and specific type of place.

Usage
The Streamlit app provides a user-friendly interface to find nearby places. It includes a button to display the location of each place on an interactive map.
