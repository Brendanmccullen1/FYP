import requests

def get_nearby_stores(latitude, longitude, api_key):
        # Set up the Google Places API endpoint
        endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

        # Define parameters for the API request
        params = {
            'location': f"{latitude},{longitude}",
            'radius': 1000,  # Adjust the radius as needed (in meters)
            'type': 'store',  # You may need to adjust the type based on the available categories
            'key': api_key,  # Replace with your Google Places API key
        }

        try:
            # Make the API request
            response = requests.get(endpoint, params=params)
            response.raise_for_status()

            # Parse the JSON response
            data = response.json()

            # Extract store information from the response
            stores = [
                {
                    'name': place['name'],
                    'address': place.get('vicinity', 'Address not available'),
                }
                for place in data.get('results', [])
            ]

            return stores

        except requests.RequestException as e:
            print(f"Error fetching nearby stores: {e}")
            return []