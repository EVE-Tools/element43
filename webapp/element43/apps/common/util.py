# Models
from django.contrib.auth.models import User

# API Models
from apps.api.models import APIKey, Character

# Eve_DB Models
from eve_db.models import StaStation
from eve_db.models import MapRegion
from eve_db.models import MapSolarSystem

# utility functions
import datetime
import pytz
import ast
import urllib

def validate_characters(user, access_mask):
    """
    Returns characters of a user that match a given minimum access mask.
    """
    
    # Get keys
    keys = APIKey.objects.filter(user = user)
    characters = []
    
    for key in keys:
        # Do a simple bitwise operation to determine if we have sufficient rights with this key.
        if ((access_mask & key.accessmask) == access_mask):
            # Get all chars from that key which have sufficient permissions.
            characters = Character.objects.filter(apikey = key)
    
    return characters
    
def find_path(start, finish, security=5, invert=0):
    """
    Returns a list of system objects which represent the path. 
    min_sec and invert are optional.
    """
    
    # Set params
    params = urllib.urlencode({'start': start, 'finish': finish, 'seclevel':security, 'invert':invert})
                               
    response = urllib.urlopen('http://localhost:3455/path', params)
    
    path_list = ast.literal_eval(response.read())
    path = []
    
    for waypoint in path_list:
        path.append(MapSolarSystem.objects.get(id = waypoint))
    
    return path
