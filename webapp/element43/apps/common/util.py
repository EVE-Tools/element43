# Models
from django.contrib.auth.models import User

# API Models
from apps.api.models import APIKey, Character

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