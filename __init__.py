"""
Package for drawing SVG graphs
"""

import logging

from .linegraphrender import SvgLineGraph, SvgLineGraphStyle, SvgLineGraphSeriesStyle
from .piechartrenderer import SvgPieChart, SvgPieChartStyle, SvgPieChartItemStyle
from .hbarchartrenderer import SvgHBarChart, SvgHBarChartStyle
from .version import VERSION

__author__ = 'Stephen Brown (Little Fish Solutions LTD)'

log = logging.getLogger(__name__)

