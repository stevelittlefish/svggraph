"""
Package for drawing SVG graphs
"""

__author__ = 'Stephen Brown (Little Fish Solutions LTD)'

import logging

from .linegraphrender import SvgLineGraph, SvgLineGraphStyle, SvgLineGraphSeriesStyle
from .piechartrenderer import SvgPieChart, SvgPieChartStyle, SvgPieChartItemStyle
from .hbarchartrenderer import SvgHBarChart, SvgHBarChartStyle

log = logging.getLogger(__name__)