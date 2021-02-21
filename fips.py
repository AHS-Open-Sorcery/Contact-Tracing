import pgeocode
import requests
import urllib


def get_fips(zip):
    nomi = pgeocode.Nominatim('us')
    lat = nomi.query_postal_code(zip)['latitude']
    lon = nomi.query_postal_code(zip)['longitude']
    # Encode parameters
    params = urllib.parse.urlencode({'latitude': lat, 'longitude': lon, 'format': 'json'})
    # Contruct request URL
    url = 'https://geo.fcc.gov/api/census/block/find?' + params

    # Get response from API
    response = requests.get(url)

    # Parse json in response
    data = response.json()

    # Print FIPS code
    return(data['County']['FIPS'])