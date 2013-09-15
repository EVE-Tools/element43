import re
from django import template

register = template.Library()


def key(d, key_name):
    """
    Performs a dictionary lookup.
    """

    try:
        return d[key_name]
    except KeyError:
        return 0

register.filter('key', key)


def sec0to1(val):
    """
    Converts the system security values into values between 0 and 1
    """
    retval = 0.0

    if val < 0:
        retval = 0.0
    elif val > 1:
        retval = 1.0
    else:
        retval = round(val, 1)

    return retval

register.filter('sec0to1', sec0to1)


def sec0to10(val):
    """
    Converts the system security values into values between 0 and 10
    """
    retval = val * 10

    if retval < 0:
        retval = 0
    elif retval > 10:
        retval = 10
    else:
        retval = int(round(retval))

    return retval

register.filter('sec0to10', sec0to10)


def is_igb(request):
    """
    Checks the headers for IGB headers.
    """

    if 'HTTP_EVE_TRUSTED' in request.META:
        return True

    return False

register.filter('is_igb', is_igb)


def igb_is_trusted(request):
    """
    Checks the headers for IGB trust.
    """

    if request.META['HTTP_EVE_TRUSTED'] == 'Yes':
        return True

    return False

register.filter('igb_is_trusted', igb_is_trusted)


def css_error(field):
    """
    Returns " error" if field has an error.
    """

    if field.errors:
            return " has-error"

    return ""

register.filter('css_error', css_error)


def top(list_to_truncate, number):
    """
    Returns top n elements of a list.
    """

    return list_to_truncate[0:number]

register.filter('top', top)


def truncate_station_name(name_to_truncate):
    """
    Trancates a station's name
    """
    sublist = name_to_truncate.rpartition(' - ')

    return sublist[0] + ' - ' + re.sub(r'[a-z ]', '', sublist[2])

register.filter('truncate_station_name', truncate_station_name)
