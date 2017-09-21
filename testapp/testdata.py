"""
Test data for drawing graphs
"""

import logging
import datetime
import math
import random

__author__ = 'Stephen Brown (Little Fish Solutions LTD)'

log = logging.getLogger(__name__)

# List of key pairs (date, num_sold)
WIDGET_SALES = []

SECONDS_IN_DAY = 60 * 60 * 24

def init():
    global WIDGET_SALES
    
    now = datetime.datetime.utcnow()
    date = now - datetime.timedelta(days=366 * 4)
    start_timestamp = date.timestamp()

    while date <= now:
        day_number = (date.timestamp() - start_timestamp) / SECONDS_IN_DAY
        sin = math.sin(day_number / 365) + 1
        mult = day_number * 0.05 + 10
        rand = random.random() * mult * 0.3
        sales = sin * mult + rand
        
        WIDGET_SALES.append((date, sales))

        date += datetime.timedelta(days=1)
