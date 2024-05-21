import os

import requests
from requests.exceptions import RequestException

import csv

import geopy.exc
from geopy.geocoders import Nominatim

from app_logger import logger
from dotenv import load_dotenv

load_dotenv()

geolocator = Nominatim(user_agent="MyApp")
api_key = os.environ.get('API-KEY')
csv_file = "Location_Analysis.csv"

sample_response_data = {
    'Jumeirah Village Triangle': {
        'Music': ['Response for Music in JVT', 'Response for Music in JVT', 'Response for Music in JVT'],
        'Skating': ['Response for Skating in JVT', "Response for Skating in JVT", "Response for Skating in JVT"],
        'Karate': 'Response for Karate in JVT',
        'Painting': 'Response for Painting in JVT',
        'Chess': 'Response for Chess in JVT'
    },
    'JLT': {
        'Music': 'Response for Music in JLT',
        'Skating': 'Response for Skating in JLT',
        'Karate': 'Response for Karate in JLT',
        'Painting': 'Response for Painting in JLT',
        'Chess': 'Response for Chess in JLT'
    },
    "Marina": {
        'Music': 'Response for Music in Marina',
        'Skating': 'Response for Skating in Marina',
        'Karate': 'Response for Karate in Marina',
        'Painting': 'Response for Painting in Marina',
        'Chess': 'Response for Chess in Marina'
    },
    "TecOM": {
        'Music': 'Response for Music in TecOM',
        'Skating': 'Response for Skating in TecOM',
        'Karate': 'Response for Karate in TecOM',
        'Painting': 'Response for Painting in TecOM',
        'Chess': 'Response for Chess in TecOM'
    },
    "Al Quoz": {
        'Music': 'Response for Music in Al Quoz',
        'Skating': 'Response for Skating in Al Quoz',
        'Karate': 'Response for Karate in Al Quoz',
        'Painting': 'Response for Painting in Al Quoz',
        'Chess': 'Response for Chess in Al Quoz'
    },
    "Al Nahda": {
        'Music': 'Response for Music in Al Nahda',
        'Skating': 'Response for Skating in Al Nahda',
        'Karate': 'Response for Karate in Al Nahda',
        'Painting': 'Response for Painting in Al Nahda',
        'Chess': 'Response for Chess in Al Nahda'
    },
    "Silicon Analysis": {
        'Music': 'Response for Music in Silicon Analysis',
        'Skating': 'Response for Skating in Silicon Analysis',
        'Karate': 'Response for Karate in Silicon Analysis',
        'Painting': 'Response for Painting in Silicon Analysis',
        'Chess': 'Response for Chess in Silicon Analysis'
    },
    "Jebel Ali": {
        'Music': 'Response for Music in Jebel Ali',
        'Skating': 'Response for Skating in Jebel Ali',
        'Karate': 'Response for Karate in Jebel Ali',
        'Painting': 'Response for Painting in Jebel Ali',
        'Chess': 'Response for Chess in Jebel Ali'
    },
    "New Town Square, Al Quadra": {
        'Music': 'Response for Music in New Town Square, Al Quadra',
        'Skating': 'Response for Skating in New Town Square, Al Quadra',
        'Karate': 'Response for Karate in New Town Square, Al Quadra',
        'Painting': 'Response for Painting in New Town Square, Al Quadra',
        'Chess': 'Response for Chess in New Town Square, Al Quadra'
    },
    "Deira": {
        'Music': 'Response for Music in Deira',
        'Skating': 'Response for Skating in Deira',
        'Karate': 'Response for Karate in Deira',
        'Painting': 'Response for Painting in Deira',
        'Chess': 'Response for Chess in Deira'
    },
}


def read_data_from_file(filename: str):
    location_lst = []
    # Read the CSV file
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        # Skip the header row
        next(reader)
        genre = next(reader)[1:]

        # Iterate over the remaining rows to extract the locations
        location_lst.extend(row[0] for row in reader)
    genres = [category.strip() for category in genre]
    location_lst = [location.strip() for location in location_lst]
    return genres, location_lst


def write_data_from_file(filename: str, response_data: dict):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        existing_data = list(reader)
    # Get the categories from the second row
    categories = existing_data[1][1:]
    categories = list(filter(lambda element: element != '', categories))

    # Append the response data to the existing data
    for row in existing_data[1:]:
        location = row[0]
        if location in response_data:
            row += [''] * len(categories)
            for category in categories:
                index = categories.index(category) + 1
                if category in response_data[location]:
                    row[index] = response_data[location][category]
                else:
                    row[index] = ''
        else:
            row.extend([''] * len(categories))

    # Write the updated data to the CSV file
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(existing_data)
    logger.info("Data has been written to the CSV file.")
    return "Data has been written to the CSV file."


def request_google_search_api(latitude, longitude, search_type, visiting_loc):
    keyword = f"{search_type} class"
    try:
        # url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=10000&type={search_type}&keyword={keyword}&rankby=prominence&key={api_key}"
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={keyword} in {visiting_loc}&location={latitude},{longitude}&radius=10000&key={api_key}"

        payload = {}
        headers = {}

        # Fetch up to 20 places per request and maximum up to 60 places
        response = requests.get(url=url, headers=headers, data=payload)
        if response and response.json()['status'] == 'OK':
            results = response.json()['results']
            lst_places = []
            for places in results[:10]:
                place_id = None
                try:
                    place_id = places['place_id']
                    logger.info(f"Place Found ::: ID: {place_id} SEARCH_TYPE: {search_type}")
                    url1 = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
                    places_response = requests.get(url1, headers=headers)

                    if places_response.json()['status'] == 'OK':
                        individual_place_result = places_response.json()['result']

                        places_result = {
                            'status': 'Success',
                            'name': individual_place_result.get('name', None),
                            'address': individual_place_result.get('formatted_address', None),
                            'phone_no': individual_place_result.get('formatted_phone_number', None),
                            'international_phone_no': individual_place_result.get('international_phone_number', None),
                            'url': individual_place_result.get('url', None),
                            # 'reviews': individual_place_result.get('reviews', None)
                        }
                    else:
                        places_result = {'status': f'{place_id} Not Found'}
                    lst_places.append(places_result)
                except Exception as err:
                    logger.info(f"PLACES EXCEPTION OCCURRED ::: {err}")
                    places_result = {'status': f'{place_id} Not Found'}
            return lst_places
        else:
            logger.warning(f"API REQUEST NO RESPONSE ::: {response.json()['results']}")
            return response.json()
    except RequestException as err:
        logger.error(f"Request Exception Occurred ::: {err}")
        return None
    except Exception as err:
        logger.error(f"General Exception Occurred ::: {err.__class__.__name__} ::: {err.args}")


def get_location(genres: list, locations: list):
    try:
        for loc in locations:
            places_categories_response = {}
            visiting_loc = f'{loc},Dubai'
            if location := geolocator.geocode(visiting_loc):
                print(f"Address: {location.address}, Latitude:{location.latitude}, Longitude: {location.longitude}")
                categories_response = {}
                for category in genres:
                    response = request_google_search_api(latitude=location.latitude, longitude=location.longitude,
                                                         search_type=category, visiting_loc=visiting_loc)
                    categories_response[category] = response
                places_categories_response[loc] = categories_response
                logger.info(places_categories_response)
                response = write_data_from_file(filename=csv_file, response_data=places_categories_response)
                print(response)
        return "Process Completed"

    except geopy.exc.GeopyError as err:
        logger.error(f"Geopy Error Occurred ::: {err}")
    except Exception as err:
        logger.error(f"General Exception Occurred ::: {err.__class__.__name__} ::: {err.args}")


genres_lst, location_lst = read_data_from_file(csv_file)
result = get_location(genres=genres_lst, locations=location_lst)
print(result)
#
# write_data_from_file(csv_file, sample_response_data)
