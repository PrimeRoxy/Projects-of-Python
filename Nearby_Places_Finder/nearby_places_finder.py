import requests

def get_coordinates(api_key, location):
    # Function to get coordinates for a given location using Google Geocoding API
    geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': location,
        'key': api_key
    }

    response = requests.get(geocoding_url, params=params)
    result = response.json().get('results', [])

    if result:
        # Extract the coordinates from the result
        coordinates = result[0]['geometry']['location']
        return f"{coordinates['lat']},{coordinates['lng']}"
    else:
        return None

def get_nearby_places(api_key, location, radius_km=5, place_type=None):
    # Function to get nearby places based on user input location, radius, and optional place type
    # Get coordinates for the given location
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

        # Make API call to get nearby places
        response = requests.get(base_url, params=params)
        results = response.json().get('results', [])

        return results
    else:
        return None

def print_nearby_places(results, place_type=None):
    # Function to print nearby places with relevant information
    if results:
        print(f"\nNearby {place_type.capitalize() if place_type else 'Places'}:")
        print("-" * 50)
        for place in results:
            name = place.get('name', 'N/A')
            address = place.get('vicinity', 'N/A')
            print(f"{name}\nAddress: {address}")
            print("-" * 50)
    else:
        print(f"No relevant nearby {place_type.capitalize() if place_type else 'places'} found.")

if __name__ == "__main__":
    # Here your YOUR_GOOGLE_MAPS_API_KEY
    api_key = "YOUR_GOOGLE_MAPS_API_KEY"

    if api_key == "YOUR_GOOGLE_MAPS_API_KEY":
        print("Please replace 'YOUR_GOOGLE_MAPS_API_KEY' with your actual API key.")
    else:
        # User input for location, radius, and optional place type
        user_location = input("Enter the location: ")
        user_radius_km = input("Enter the radius in kilometers (press Enter for default 5km): ")
        user_place_type = input("Enter the specific type of place (press Enter for all places): ").lower()

        # Process user inputs and call the functions
        if user_radius_km:
            user_radius_km = float(user_radius_km)
        else:
            user_radius_km = 5  # Default radius in kilometers

        coordinates = get_coordinates(api_key, user_location)
        if coordinates:
            results = get_nearby_places(api_key, user_location, user_radius_km, user_place_type)
            print_nearby_places(results, user_place_type)
        else:
            print("Unable to get coordinates for the specified location.")
