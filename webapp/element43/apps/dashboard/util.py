# Datetime
import datetime

# API Models
from apps.api.models import JournalEntry, MarketTransaction

# Django Aggregation
from django.db.models import Sum

def calculate_profit_stats(characters, days):
    """
    Calculates profit stats for the given characters over a certain number of days.
    """

    # Timedelta
    days_ago = datetime.date.today() - datetime.timedelta(days=days)

    dictionary = {}

    # Gets brokers fee
    dictionary['brokers_fee'] = JournalEntry.objects.filter(character__in=characters,
                                                    		ref_type_id=46,
                                                    		date__gte=days_ago).aggregate(Sum('amount'))['amount__sum']

    # Gets taxes
    dictionary['taxes'] = JournalEntry.objects.filter(character__in=characters,
                                              		  ref_type_id=54,
                                              		  date__gte=days_ago).aggregate(Sum('amount'))['amount__sum']

    # Gets gross profit
    gross_profit = MarketTransaction.objects.filter(character__in=characters,
											                      is_bid=False,
											                      date__gte=days_ago).extra(select={'amount': 'price * quantity'})
    dictionary['gross_profit'] = 0

    for entry in gross_profit:
    	dictionary['gross_profit'] += entry.amount

    return dictionary