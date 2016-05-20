"""
Contains code for generating SVG line graphs
"""

__author__ = 'Stephen Brown (Little Fish Solutions LTD)'

import logging
import math
import decimal

import svglib

log = logging.getLogger(__name__)


class SvgLineGraphStyle(object):
    def __init__(self,
                 grid_line_colour='#bbb',
                 axis_line_colour='#333',
                 scale_text_colour='#555',
                 scale_text_size=12,
                 y_scale_text_distance=7,
                 y_scale_text_width=50,
                 x_scale_text_height=30,
                 y_scale_text_anchor='end',
                 x_scale_border=False,
                 x_label_rotation=0,
                 show_key=True,
                 key_height=34,
                 key_title='Key:',
                 key_title_text_colour='#555',
                 key_title_text_size=12,
                 key_title_width=150,
                 key_label_text_colour='#555',
                 key_label_text_size=12,
                 auto_format_y_axis=True,
                 y_label_units=None,
                 y_label_pre_units=None,
                 show_minor_x_grid_lines=True):

        self.grid_line_colour = grid_line_colour
        self.axis_line_colour = axis_line_colour
        self.scale_text_colour = scale_text_colour
        self.scale_text_size = scale_text_size
        self.y_scale_text_distance = y_scale_text_distance
        self.y_scale_text_width = y_scale_text_width
        self.x_scale_text_height = x_scale_text_height
        self.y_scale_text_anchor = y_scale_text_anchor
        self.x_scale_border = x_scale_border
        self.x_label_rotation = x_label_rotation
        self.show_key = show_key
        self.key_height = key_height
        self.key_title = key_title
        self.key_title_text_colour = key_title_text_colour
        self.key_title_text_size = key_title_text_size
        self.key_title_width = key_title_width
        self.key_label_text_colour = key_label_text_colour
        self.key_label_text_size = key_label_text_size
        self.auto_format_y_axis = auto_format_y_axis
        self.y_label_units = y_label_units
        self.y_label_pre_units = y_label_pre_units
        self.show_minor_x_grid_lines = show_minor_x_grid_lines


class SvgLineGraphSeriesStyle(object):
    def __init__(self, line_colour, point_fill_colour=None, point_outline_colour=None, line_thickness=1,
                 point_outline_thickness=1, show_points=False, show_line=True, point_radius=5, shade_under_line=False,
                 shade_colour=None):
        """
        :param line_colour: The colour of the line
        :param point_fill_colour: The fill colour of the circles rendered for each point
        :param point_outline_colour: The outline colour of the circles rendered for each point
        :param line_thickness: The line thickness
        :param point_outline_thickness: The thickness of the outline of the circles rendered for each point
        :param show_points: Whether or not to show the points
        :param show_line: Whether or not to show the line
        :param point_radius: The radius of the circles rendered for each point
        :param shade_under_line: Whether or not to shade the area under the line
        :param shade_colour: The colour to shade the area under the line (hint: make this semi-transparent)
        """
        self.line_colour = line_colour
        self.line_thickness = line_thickness
        self.point_fill_colour = point_fill_colour
        self.point_outline_colour = point_outline_colour
        self.point_outline_thickness = point_outline_thickness
        self.show_points = show_points
        self.show_line = show_line
        self.point_radius = point_radius
        self.shade_under_line = shade_under_line
        self.shade_colour = shade_colour

    def clone(self, line_colour=None, point_fill_colour=None, point_outline_colour=None, line_thickness=None,
              point_outline_thickness=None, show_points=None, show_line=None, point_radius=None, shade_under_line=None,
              shade_colour=None):
        if line_colour is None:
            line_colour = self.line_colour
        if point_fill_colour is None:
            point_fill_colour = self.point_fill_colour
        if point_outline_colour is None:
            point_outline_colour = self.point_outline_colour
        if line_thickness is None:
            line_thickness = self.line_thickness
        if point_outline_thickness is None:
            point_outline_thickness = self.point_outline_thickness
        if show_points is None:
            show_points = self.show_points
        if show_line is None:
            show_line = self.show_line
        if point_radius is None:
            point_radius = self.point_radius
        if shade_under_line is None:
            shade_under_line = self.shade_under_line
        if shade_colour is None:
            shade_colour = self.shade_colour

        return SvgLineGraphSeriesStyle(
            line_colour=line_colour,
            point_fill_colour=point_fill_colour,
            point_outline_colour=point_outline_colour,
            line_thickness=line_thickness,
            point_outline_thickness=point_outline_thickness,
            show_points=show_points,
            show_line=show_line,
            point_radius=point_radius,
            shade_under_line=shade_under_line,
            shade_colour=shade_colour
        )


class SvgLineGraphSeries(object):
    def __init__(self, name, data, style):
        self.name = name
        self.data = data
        self.style = style

    @property
    def num_points(self):
        return len(self.data)

    @property
    def has_data(self):
        return self.num_points > 0


class SvgLineGraph(object):
    def __init__(self, x_labels=None, style=None, y_interval=None):

        self.x_labels = x_labels
        # List of all series in the graph
        self.series = []
        # Range of y values
        self.y_min = 0
        self.y_max = 0
        # Number of data points
        self.x_range = 0
        if x_labels:
            self.x_range = len(x_labels)

        self.style = style if style else SvgLineGraphStyle()
        self.y_interval = y_interval

    def add_series(self, name, series_data, series_style):
        """
        Add a series to the graph
        :param series_data: A list of data points (must be numeric)
        """
        series = SvgLineGraphSeries(name, series_data, series_style)
        self.series.append(series)

        for y in series_data:
            if y < self.y_min:
                self.y_min = y

            if y > self.y_max:
                self.y_max = y

        x_range = len(series_data)
        if x_range > self.x_range:
            self.x_range = x_range

    def get_default_y_interval(self):
        """
        :return: A sensible (math) interval for the y coord
        """
        # Calculate a sensible y_interval
        delta_y = self.y_max - self.y_min
        # Aim for about 10 divisions
        target = int(delta_y / 10)
        if target < 1:
            log.warn('Not supported: y_intervals < 0. Defaulting to 1')
            return 1
        else:
            num_digits = len(str(target))
            exp = num_digits - 1
            if target <= 10 ** exp:
                return 10 ** exp
            elif target <= 2 * 10 ** exp:
                return 2 * 10 ** exp
            elif target <= 5 * 10 ** exp:
                return 5 * 10 ** exp
            else:
                return 10 ** (exp + 1)

    def render(self, width, height, view_box_mode=False):
        """
        :return: String containing SVG render of line graph
        """
        style = self.style

        svg = svglib.SvgGenerator()
        svg.begin(width, height, view_box_mode=view_box_mode)

        y_label_width = style.y_scale_text_width
        x_label_height = style.x_scale_text_height
        key_height = style.key_height if style.show_key else 0

        left_margin = y_label_width
        right_margin = 4
        top_margin = style.scale_text_size / 2
        bottom_margin = x_label_height + key_height + 2

        x_plot_size = width - left_margin - right_margin
        y_plot_size = height - top_margin - bottom_margin

        has_data = False
        for series in self.series:
            if series.has_data:
                has_data = True
                break

        if not has_data:
            svg.rect(left_margin, top_margin, x_plot_size, y_plot_size, stroke='#aaa', fill='transparent')
            svg.text('(no data to display)', left_margin + x_plot_size / 2, top_margin + y_plot_size / 2,
                     anchor='middle', alignment_baseline='middle',
                     fill='#999')
            svg.end()
            return svg.get_svg()

        # Calculate scales etc for x coords
        x_math_offset = 0
        x_math_range = self.x_range - 1
        x_math_interval = 1

        x_steps = x_math_range - x_math_offset
        if x_steps == 0:
            x_steps = 1

        x_screen_offset = left_margin
        x_screen_range = x_plot_size
        x_screen_interval = float(x_screen_range) / x_steps

        # Calculate scales etc for y coords
        y_math_interval = self.y_interval if self.y_interval else self.get_default_y_interval()
        y_math_offset = math.floor(self.y_min / y_math_interval) * y_math_interval

        # This is fudging it, as we kind if need to round in both directions for graphs that are both +ve and -ve
        y_range = (self.y_max - self.y_min) / y_math_interval
        if self.y_min < 0 and self.y_max > 0:
            y_range += 1

        y_math_range = math.ceil(y_range) * y_math_interval

        y_steps = int(y_math_range / y_math_interval)

        if y_steps == 0:
            y_steps = 1

        y_screen_offset = bottom_margin
        y_screen_range = y_plot_size
        y_screen_interval = y_screen_range / y_steps

        def x_math_to_screen(math_x):
            """
            Convert mathematical x coord to screen x coord
            """
            return x_screen_offset + (math_x - x_math_offset) * x_screen_interval

        def y_math_to_screen(math_y):
            """
            Convert mathematical y coord to screen x coord
            """
            return height - y_screen_offset - ((math_y - y_math_offset) / y_math_interval) * y_screen_interval

        # Draw the grid
        x_screen_min = x_math_to_screen(x_math_offset)
        x_screen_max = x_math_to_screen(x_math_offset + x_math_range)
        # Handle degenerate case!
        if x_screen_max == x_screen_min:
            x_screen_max = x_math_to_screen(x_math_offset + 1)

        y_screen_min = y_math_to_screen(y_math_offset)
        y_screen_max = y_math_to_screen(y_math_offset + y_math_range)

        for x_step in range(x_steps + 1):
            if style.show_minor_x_grid_lines or self.x_labels[x_step]:
                screen_x = x_math_to_screen(x_step)
                colour = style.axis_line_colour if x_step == 0 else style.grid_line_colour
                svg.line(screen_x, y_screen_min, screen_x, y_screen_max, stroke=colour)

        if x_steps == 1:
            # Add an extra line down the middle
            svg.line(x_screen_min + x_plot_size / 2, y_screen_min, x_screen_min + x_plot_size / 2, y_screen_max, stroke=style.grid_line_colour)

        for y_step in range(y_steps + 1):
            math_y = y_step * y_math_interval + y_math_offset
            screen_y = y_math_to_screen(math_y)
            colour = style.axis_line_colour if math_y == 0 else style.grid_line_colour
            svg.line(x_screen_min, screen_y, x_screen_max, screen_y, stroke=colour)

        # Scale
        for y_step in range(y_steps + 1):
            math_y = y_step * y_math_interval + y_math_offset
            screen_y = y_math_to_screen(math_y)
            y_value = decimal.Decimal(int(y_math_offset + y_step * y_math_interval))

            if style.auto_format_y_axis:
                if y_value >= 1000000:
                    y_label = '%sm' % (y_value / 1000000)
                elif y_value >= 1000:
                    y_label = '%sk' % (y_value / 1000)
                else:
                    y_label = str(y_value)
            else:
                y_label = str(y_value)

            y_label = '%s%s%s' % (style.y_label_pre_units if style.y_label_pre_units else '',
                                  y_label,
                                  style.y_label_units if style.y_label_units else '')

            svg.text(y_label, x_screen_offset - style.y_scale_text_distance,
                     screen_y, anchor=style.y_scale_text_anchor, font_size=style.scale_text_size,
                     fill=style.scale_text_colour, alignment_baseline='middle')

        if x_steps == 1:
            svg.text(self.x_labels[0], x_screen_min + x_screen_range / 2,
                     y_screen_min + style.x_scale_text_height / 2 + 1,
                     anchor='middle', font_size=style.scale_text_size,
                     fill=style.scale_text_colour, alignment_baseline='middle')
        else:
            for x_step in range(x_steps + 1):
                if style.x_scale_border and x_step == 0:
                    continue

                if style.x_scale_border and x_step == x_steps:
                    continue

                screen_x = x_math_to_screen(x_step)

                if style.x_label_rotation:
                    screen_y = y_screen_min + style.scale_text_size / 3 + 1
                    anchor = 'start'
                    transform = svglib.rotation_transform(style.x_label_rotation, screen_x, screen_y)
                else:
                    screen_y = y_screen_min + style.x_scale_text_height / 2 + 1
                    transform = None
                    if x_step == x_steps and not style.x_label_rotation:
                        anchor = 'end'
                    else:
                        anchor = 'middle'

                if x_step < len(self.x_labels):
                    svg.text(self.x_labels[x_step], screen_x,
                             screen_y, anchor=anchor, font_size=style.scale_text_size,
                             fill=style.scale_text_colour, alignment_baseline='middle',
                             transform=transform)

        # Border around scale
        if style.x_scale_border:
            svg.line(x_screen_min, y_screen_min, x_screen_min, y_screen_min + style.x_scale_text_height, stroke=style.grid_line_colour)
            svg.line(x_screen_max, y_screen_min, x_screen_max, y_screen_min + style.x_scale_text_height, stroke=style.grid_line_colour)
            svg.line(x_screen_min, y_screen_min + style.x_scale_text_height, x_screen_max, y_screen_min + style.x_scale_text_height, stroke=style.grid_line_colour)

        # Draw the key
        if style.show_key:
            key_x_offset = style.key_title_width
            key_y_offset = height - style.key_height
            key_width = width - right_margin - key_x_offset
            key_item_width = key_width / len(self.series)
            key_square_offset = 10
            key_square_size = style.key_height - key_square_offset * 2

            svg.text(style.key_title, x_screen_min, key_y_offset + style.key_height / 2 + 1,
                     fill=style.key_title_text_colour, font_size=style.key_title_text_size, alignment_baseline='middle')

            i = 0
            for series in self.series:
                x = key_x_offset + i * key_item_width
                y = key_y_offset + key_square_offset

                svg.rect(x, y, key_square_size, key_square_size, fill=series.style.line_colour)
                svg.text(series.name, x + key_square_size + key_square_offset, key_y_offset + style.key_height / 2 + 1,
                         alignment_baseline='middle', font_size=style.key_label_text_size,
                         fill=style.key_label_text_colour)
                i += 1

        # Calculate screen coordinates for each of the series
        for series in self.series:
            # Create a list of points
            series._screen_points = []

            for i in range(series.num_points):
                math_x = i * x_math_interval
                math_y = series.data[i]

                screen_x = x_math_to_screen(math_x)
                screen_y = y_math_to_screen(math_y)

                series._screen_points.append((screen_x, screen_y))

        if x_steps == 1:
            # Degenerate case - 1 point!
            # Shade under lines
            for series in self.series:
                if series.style.shade_under_line:
                    points = [
                        (x_screen_min, y_screen_min),
                        (x_screen_min, series._screen_points[0][1]),
                        (x_screen_max, series._screen_points[0][1]),
                        (x_screen_max, y_screen_min)
                    ]

                    svg.polygon(points, fill=series.style.shade_colour)

            # Plot the lines
            for series in self.series:
                if series.style.show_line:
                    x1, y1 = x_screen_min, series._screen_points[0][1]
                    x2, y2 = x_screen_min + x_plot_size, series._screen_points[0][1]

                    svg.line(x1, y1, x2, y2, stroke=series.style.line_colour,
                             stroke_width=series.style.line_thickness)

            # Plot the points
            for series in self.series:
                if series.style.show_points:
                    x, y = series._screen_points[0]
                    svg.circle(x_screen_min + x_plot_size / 2, y, series.style.point_radius, series.style.point_outline_colour,
                               series.style.point_fill_colour, series.style.point_outline_thickness)

        else:
            # Normal conditions - draw a proper line graph
            # Shade under lines
            for series in self.series:
                if series.style.shade_under_line:
                    p_first = (series._screen_points[0][0], y_screen_min)
                    p_last = (series._screen_points[-1][0], y_screen_min)

                    svg.polygon([p_first] + series._screen_points + [p_last], fill=series.style.shade_colour)

            # Plot the lines
            for series in self.series:
                if series.style.show_line:
                    for i in range(series.num_points - 1):
                        x1, y1 = series._screen_points[i]
                        x2, y2 = series._screen_points[i + 1]

                        svg.line(x1, y1, x2, y2, stroke=series.style.line_colour,
                                 stroke_width=series.style.line_thickness)

            # Plot the points
            for series in self.series:
                if series.style.show_points:
                    for point in series._screen_points:
                        x, y = point
                        svg.circle(x, y, series.style.point_radius, series.style.point_outline_colour,
                                   series.style.point_fill_colour, series.style.point_outline_thickness)

        svg.end()
        return svg.get_svg()