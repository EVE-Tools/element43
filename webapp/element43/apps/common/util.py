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

def pathfind(start_system, finish_system, seclevel, invert):
    """
    Queries the pathfinder daemon for path, returns list of system objects in order
    """
    post_params = urllib.urlencode({'start': start_system, 'finish': finish_system, 'seclevel':seclevel, 'invert':invert})
    path_response = urllib.urlopen('http://localhost:3455/path', post_params)
    full_path = ast.literal_eval(path_response.read())
    
    response = {}
    path = []
    for system in full_path:
        system_object = MapSolarSystem.objects.get(id = system)
        path.append(system_object)
    
    return path