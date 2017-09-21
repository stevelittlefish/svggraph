"""
Main blueprint for test app
"""

import logging

from flask import Blueprint, render_template
from littlefish import colourutil

import svggraph
import testdata

__author__ = 'Stephen Brown (Little Fish Solutions LTD)'

log = logging.getLogger(__name__)

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/line-graph')
def line_graph():
    x_labels = []

    raw_data = testdata.WIDGET_SALES_RAW[-365 * 2:]

    raw = []

    for item in raw_data:
        date = item[0]
        if date.day == 1:
            x_labels.append(date.strftime('%d %b %Y'))
        else:
            x_labels.append('')
        
        raw.append(item[1])

    graph_style = svggraph.SvgLineGraphStyle(
        key_title='',
        key_title_width=110,
        key_title_text_size=11,
        key_label_text_size=11,
        key_max_rows=2,
        key_order_in_columns=True,
        show_minor_x_grid_lines=False,
        x_label_rotation=45,
        x_scale_text_height=80,
        right_margin=80,
        y_min_intervals=3,
        y_minor_interval=10,
    )

    base_series_style = svggraph.SvgLineGraphSeriesStyle(
        line_colour='#000000',
        show_points=False,
        show_line=False,
        point_radius=3,
        line_thickness=2,
    )

    line_chart = svggraph.SvgLineGraph(x_labels=x_labels, style=graph_style)

    colour_raw = '#33bb22'
    colour_avg = '#d33682'
    colour_avg2 = '#6666ff'
    
    raw_series = line_chart.add_series(
        'Widget Sales', raw,
        base_series_style.clone(
            show_points=True,
            point_outline_colour=colourutil.html_color_to_rgba(colour_raw, 0.7),
            point_fill_colour=colourutil.html_color_to_rgba(colour_raw, 0.5),
            key_colour=colourutil.blend_html_colour_to_white(colour_raw, 0.6),
            key_shape='circle'
        ))
    
    line_chart.add_series(
        '30 Day Rolling Average', raw_series.get_rolling_average(30),
        base_series_style.clone(
            show_line=True,
            line_colour=colour_avg2
        ))

    line_chart.add_series(
        '7 Day Rolling Average', raw_series.get_rolling_average(7),
        base_series_style.clone(
            show_line=True,
            line_colour=colour_avg,
        ))
    
    svg = line_chart.render(800, 500, view_box_mode=True)

    return render_template('line_graph.html', svg=svg)
