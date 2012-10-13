# API Models
from apps.api.models import APIKey, Character

# Eve_DB Models
from eve_db.models import MapSolarSystem

# utility functions
import ast
import urllib

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

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
    start: system_id of first system
    finish: system_id of last system
    security: sec level of system * 10
    invert: if true (1), use security as highest seclevel you want to enter, default (0) seclevel is the lowest you want to try to use
    """

    # Set params
    params = urllib.urlencode({'start': start, 'finish': finish, 'seclevel':security, 'invert':invert})

    response = urllib.urlopen('http://localhost:3455/path', params)

    path_list = ast.literal_eval(response.read())
    path = []

    for waypoint in path_list:
        path.append(MapSolarSystem.objects.get(id = waypoint))

    return path
