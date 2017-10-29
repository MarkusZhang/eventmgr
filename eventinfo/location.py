import requests
import json
from geopy.distance import great_circle

map_api_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='

def get_lng_lat(address):
    """
        * given address string, return the longitude and latitude of it
    """
    # TODO: currently just return the first entry of google map's response, which is not accurate
    url=map_api_url + address
    response=requests.get(url)
    json_obj=json.loads(response.text)
    try:
        latitude=json_obj['results'][0]['geometry']['location']['lat']
        longitude=json_obj['results'][0]['geometry']['location']['lng']
        can_find=True
    except:
        # google map cannot find that address
        latitude=longitude=-1
        can_find=False
    return can_find,longitude,latitude


def is_within_distance(lng1,lat1,lng2,lat2,distance):
    p1=(lng1,lat1)
    p2=(lng2,lat2)
    actual_distance=great_circle(p1, p2).kilometers
    return actual_distance<=distance