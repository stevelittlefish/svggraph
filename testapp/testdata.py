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
WIDGET_SALES_RAW = []
WIDGET_SALES_AVG = []

SECONDS_IN_DAY = 60 * 60 * 24


def init():
    global WIDGET_SALES_RAW
    
    now = datetime.datetime.utcnow()
    date = now - datetime.timedelta(days=366 * 4)
    start_timestamp = date.timestamp()

    while date <= now:
        day_number = (date.timestamp() - start_timestamp) / SECONDS_IN_DAY
        sin = math.sin(day_number * math.pi * 2 / 365) + 1
        print(day_number * math.pi / 365, sin)
        mult = day_number * 0.05 + 10
        rand = random.random() * mult * 2
        sales = sin * mult + rand + 5
        
        WIDGET_SALES_RAW.append((date, sales))

        date += datetime.timedelta(days=1)

    avg_width = 7
    # try and centre it
    before = avg_width // 2
    for i in range(before):
        WIDGET_SALES_AVG.append((WIDGET_SALES_RAW[i], None))
    
    for i in range(len(WIDGET_SALES_RAW) - avg_width + 1):
        tot = 0
        for j in range(i, i + avg_width):
            tot += WIDGET_SALES_RAW[j][1]
        
        WIDGET_SALES_AVG.append((WIDGET_SALES_RAW[i][0], float(tot) / avg_width))


