import os

from geopy.geocoders import Nominatim
import requests
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

###################################################################################
# api_key = os.environ.get('API-KEY')
# geocoding_api_key = os.environ.get('GOOGLE-GEOCODING-API')
# loc = "B-202 & 203, 2ND FLOOR, SUMEL BUSINESS PARK-3, OPP.NEW CLOTH MARKET, RAIPUR, AHMEDABAD."
# pin_code = 380002
# api_response = requests.get(
#     'https://maps.googleapis.com/maps/api/geocode/json?address={0}&components=locality:{1}|country:IN&key={2}'.format(loc, pin_code, geocoding_api_key))
#
# api_response_dict = api_response.json()
# if api_response_dict['status'] == 'OK':
#     latitude = api_response_dict['results'][0]['geometry']['location']['lat']
#     longitude = api_response_dict['results'][0]['geometry']['location']['lng']
#     print('Latitude:', latitude)
#     print('Longitude:', longitude)
###################################################################################

###################################################################################
# geolocator = Nominatim(user_agent="MyApp")
# location = geolocator.geocode(loc)
# print(location)
# print(location.latitude)
# print(location.longitude)
###################################################################################

###################################################################################
# serper_api_key = os.environ.get('SERPER-API')
geocoding_api_key = os.environ.get('GOOGLE-GEOCODING-API')

import requests
import json
import csv


def read_addresses_from_csv(file_path):
    addresses = []

    with open(file_path, mode='r', encoding='utf-8', newline='') as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)

        for row in csv_reader:
            address = {
                'ADDRESS': row[0],
                'PIN CODE': row[3],
                'E-MAIL ID': row[4]
            }
            addresses.append(address)
    return addresses


def get_lat_long_for_address(address, pin_code, flag=0):
    # url = "https://google.serper.dev/places"
    # payload = json.dumps({
    #     "q": address,
    #     "gl": "in"
    # })
    # headers = {
    #     'X-API-KEY': serper_api_key,
    #     'Content-Type': 'application/json'
    # }
    # response = requests.request("POST", url, headers=headers, data=payload)
    # data = json.loads(response.text)

    api_response = requests.get(
        'https://maps.googleapis.com/maps/api/geocode/json?address={0}&components=locality:{1}|country:IN&key={2}'.format(
            address, pin_code, geocoding_api_key))

    api_response_dict = api_response.json()

    # if 'places' not in data or len(data['places']) <= 0 and not flag:
    if api_response_dict['status'] != 'OK' and not flag:
        address = ' '.join(address.split(',')[1:]).strip()
        return get_lat_long_for_address(address, pin_code, 1)

    # if 'places' not in data or len(data['places']) <= 0:
    if api_response_dict['status'] != 'OK':
        return None, None

    # lat = data['places'][0]['latitude']
    # long = data['places'][0]['longitude']
    lat = api_response_dict['results'][0]['geometry']['location']['lat']
    long = api_response_dict['results'][0]['geometry']['location']['lng']
    return lat, long


def write_data_into_csv(new_file_path, address_list):
    record_count = 0
    # Create a new CSV file to store the results
    with open(new_file_path, mode='w', newline='') as csv_file:
        fieldnames = ['E-MAIL ID', 'ADDRESS', 'PIN CODE', 'LATITUDE', 'LONGITUDE']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for address_info in address_list:
            address = address_info['ADDRESS']
            pin_code = address_info['PIN CODE']
            lat, lon = get_lat_long_for_address(address, pin_code)

            writer.writerow({
                'E-MAIL ID': address_info['E-MAIL ID'],
                'ADDRESS': address_info['ADDRESS'],
                'PIN CODE': address_info['PIN CODE'],
                'LATITUDE': lat,
                'LONGITUDE': lon
            })
            record_count += 1
            print(f"{address_info['E-MAIL ID']} ::: DATA ADDED.")
    return f"COMPLETED WITH TOTAL RECORD ::: {record_count}"


# Specify the path to your CSV file
# csv_file_path = './Address_files/Remaining_PM_Copy.csv'
# csv_file_path = './Address_files/AADAT_Copy.csv'
# csv_file_path = './Address_files/PM_Copy.csv'
# csv_file_path = './Address_files/AGENT_Copy.csv'
csv_file_path = './Address_files/AM_Copy.csv'

# new_csv_file_path = 'google_outputs_file/output_Remaining_PM_Copy.csv'
# new_csv_file_path = 'google_outputs_file/output_AADAT_Copy.csv'
# new_csv_file_path = 'google_outputs_file/output_PM_Copy.csv'
# new_csv_file_path = 'google_outputs_file/output_AGENT_Copy.csv'
new_csv_file_path = 'google_outputs_file/output_AM_Copy.csv'

# Call the function to read addresses from the CSV file
address_lst = read_addresses_from_csv(csv_file_path)
# print(address_list)
result = write_data_into_csv(new_csv_file_path, address_lst)
print(result)
#######################################################################
