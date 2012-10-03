from django import template

register = template.Library()

#
# The humanize_time filter is based on the following script:
#
# https://github.com/liudmil-mitev/experiments/blob/master/time/humanize_time.py
#

INTERVALS = [1, 60, 3600, 86400, 604800, 2419200, 29030400]
NAMES = [('second', 'seconds'),
         ('minute', 'minutes'),
         ('hour',   'hours'),
         ('day',    'days'),
         ('week',   'weeks'),
         ('month',  'months'),
         ('year',   'years')]

def humanize_time(amount, units):
    """
    Humanizes time. 
    
    For example: 6000 seconds = 1 hour 40 minutes.
    """
    amount = int(amount)

    unit = map(lambda a: a[1], NAMES).index(units)
    # Convert to seconds
    amount = amount * INTERVALS[unit]

    result = ""
    for i in range(len(NAMES)-1, -1, -1):
        a = amount // INTERVALS[i]
        if a > 0:
            result += "%d %s " % (a, NAMES[i][1 % a])
            amount -= a * INTERVALS[i]

    return result

register.filter('humanize_time', humanize_time)