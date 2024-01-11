import streamlit as st
import requests
import folium

def get_coordinates(api_key, location):
    geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': location,
        'key': api_key
    }

    response = requests.get(geocoding_url, params=params)
    result = response.json().get('results', [])

    if result:
        coordinates = result[0]['geometry']['location']
        return f"{coordinates['lat']},{coordinates['lng']}"
    else:
        return None

def get_nearby_places(api_key, location, radius_km=5, place_type=None):
    coordinates = get_coordinates(api_key, location)

    if coordinates:
        base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'location': coordinates,
            'radius': int(radius_km * 1000),  # Convert km to meters
            'key': api_key
        }

        if place_type:
            params['type'] = place_type

        response = requests.get(base_url, params=params)
        results = response.json().get('results', [])

        return results
    else:
        return None

def create_map(latitude, longitude, name):
    map_center = [latitude, longitude]
    map_object = folium.Map(location=map_center, zoom_start=15)
    folium.Marker(location=map_center, popup=name).add_to(map_object)
    return map_object

def print_nearby_places(results, place_type=None):
    if results:
        st.subheader(f"Nearby {place_type.capitalize() if place_type else 'Places'}:")
        for place in results:
            name = place.get('name', 'N/A')
            address = place.get('vicinity', 'N/A')
            
            if st.button(f"Show on Map: {name}", key=f"map_button_{name}"):
                latitude = place['geometry']['location']['lat']
                longitude = place['geometry']['location']['lng']
                map_object = create_map(latitude, longitude, name)
                st.write(f"**{name}**\n*Address:* {address}")
                st.write("Showing location on map...")
                st.markdown(folium.Figure().add_child(map_object)._repr_html_(), unsafe_allow_html=True)
                st.markdown("---")
            else:
                st.write(f"**{name}**\n*Address:* {address}")
                st.markdown("---")
    else:
        st.warning(f"No relevant nearby {place_type.capitalize() if place_type else 'places'} found.")

def main():
    st.title("Nearby Places Finder")

    api_key = "YOUR_GOOGLE_MAPS_API_KEY"  # Replace with your API key

    user_location = st.text_input("Enter the location:")
    user_radius_km = st.text_input("Enter the radius in kilometers (press Enter for default 5km):")
    user_place_type = st.text_input("Enter the specific type of place (press Enter for all places):").lower()

    if user_radius_km:
        user_radius_km = float(user_radius_km)
    else:
        user_radius_km = 5  # Default radius in kilometers

    if st.button("Find Nearby Places"):
        coordinates = get_coordinates(api_key, user_location)
        if coordinates:
            results = get_nearby_places(api_key, user_location, user_radius_km, user_place_type)
            print_nearby_places(results, user_place_type)
        else:
            st.warning("Unable to get coordinates for the specified location.")

if __name__ == "__main__":
    main()
