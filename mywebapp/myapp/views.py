# myapp/views.py
import requests
from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from .forms import CharacterInputForm
from .models import ComicBookStore
from .utils.recommendation import find_similar_characters_cosine, get_wikipedia_image
from .utils.stores import get_nearby_stores as utils_get_nearby_stores


def home(request):
    return render(request, 'home.html')


def recommendations(request):
    return render(request, 'recommendations.html')


def contact_us(request):
    return render(request, 'contact_us.html')


def stores_near_you(request):
    return render(request, 'stores_near_you.html')


def recommendation_page(request):
    input_character = ''
    similar_characters_cosine = []

    if request.method == 'POST':
        form = CharacterInputForm(request.POST)

        if form.is_valid():
            input_character = form.cleaned_data['character'].strip()
            df = pd.read_csv('myapp/datasets/superheroes_power_matrix.csv')
            similar_characters_cosine = find_similar_characters_cosine(input_character, df)

    else:
        form = CharacterInputForm()

    image_urls = [get_wikipedia_image(character) for character in similar_characters_cosine]

    context = {
        'form': form,
        'input_character': input_character,
        'similar_characters_cosine': zip(similar_characters_cosine, image_urls),
    }

    return render(request, 'recommendation_page.html', context)


def stores_near_you(request):
    # For simplicity, let's use coordinates for Dublin
    latitude = 53.349805
    longitude = -6.26031

    # Replace 'YOUR_GOOGLE_API_KEY' with your actual API key
    api_key = 'AIzaSyCNMNLMPlaPfeBnnJQtBQBSXAOIpMMHzJg'

    # Call the function from utils.stores to get nearby stores
    recommended_stores = utils_get_nearby_stores(latitude, longitude, api_key)

    context = {
        'recommended_stores': recommended_stores,
        'latitude': latitude,
        'longitude': longitude,
    }

    return render(request, 'stores_near_you.html', context)


def calculate_distance(lat1, lon1, lat2, lon2):
    # Implement a function to calculate the distance between two sets of coordinates
    # You can use haversine formula or another distance calculation method
    # For simplicity, let's assume a flat Earth for this example
    return ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5


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


def stores_near_you(request):
    # For simplicity, let's use coordinates for Dublin
    latitude = 53.349805
    longitude = -6.26031

    # Replace 'YOUR_GOOGLE_API_KEY' with your actual API key
    api_key = 'AIzaSyCNMNLMPlaPfeBnnJQtBQBSXAOIpMMHzJg'

    # Call the function to get nearby stores
    recommended_stores = get_nearby_stores(latitude, longitude, api_key)

    context = {
        'recommended_stores': recommended_stores,
        'latitude': latitude,
        'longitude': longitude,
    }

    return render(request, 'stores_near_you.html', context)
