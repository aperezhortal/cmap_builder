"""
Helper functions.

.. autosummary::
    :toctree: ../generated/

    rgb_from_name
    plot_colortable
"""
from colorsys import hls_to_rgb, hsv_to_rgb, rgb_to_hls, rgb_to_hsv

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

named_colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)


def _color_modifier_value(color_modifier, field):
    """Get the vale of the the color modifier type, if any."""
    try:
        field_value = int(color_modifier.replace(field, ""))
    except ValueError:
        raise ValueError(f"Invalid color modifier: {color_modifier}")

    if (field_value < 0) or (field_value > 100):
        raise ValueError(f'Invalid value for "{field}" field: {color_modifier}')
    return field_value / 100.0


def rgb_from_name(named_color_ref):
    """
    Returns the RGB values of a named color (in the 0-1 range).
    The color name supports the following color modifiers suffixes:

    - "_l#": HLS lightness (L) modifier (0 to 100 range).
      For example, "yellow_l75" changes the lightness to 0.75.
    - "_s#": HSV saturation (S) modifier (0 to 100 range).
      For example, "yellow_s75" changes the saturation to 0.75.
    - "_v#": HSV value (V, or brightness) modifier (0 to 100 range).
      For example, "yellow_v75" changes the brightness (value) to 0.75.
    - "_light": Make color lighter. Same as the "_l10" modifier.
    - "_dark": Make color darker. Same as the "_l80" modifier.
    """
    color_modifiers_count = named_color_ref.count("_")

    if color_modifiers_count == 0:
        rgb_color = named_colors[named_color_ref]
        rgb_color = mcolors.to_rgba(rgb_color)[:3]
    elif color_modifiers_count == 1:
        named_color, hsv_args = named_color_ref.split("_", 2)[:2]
        named_color, color_modifier = named_color_ref.split("_")

        rgb_color = named_colors[named_color]
        rgb_color = mcolors.to_rgba(rgb_color)[:3]

        hls_color = np.array(rgb_to_hls(*rgb_color))
        hsv_color = np.array(rgb_to_hsv(*rgb_color))

        if color_modifier.endswith("dark"):
            color_modifier = "l10"
        elif color_modifier.endswith("light"):
            color_modifier = "l80"

        if "l" in color_modifier:
            hls_color[1] = _color_modifier_value(color_modifier, "l")
            rgb_color = hls_to_rgb(*hls_color)
        elif "v" in color_modifier:
            hsv_color[2] = _color_modifier_value(color_modifier, "v")
            rgb_color = hsv_to_rgb(*hsv_color)
        elif "s" in color_modifier:
            hsv_color[1] = _color_modifier_value(color_modifier, "s")
            rgb_color = hsv_to_rgb(*hsv_color)
        else:
            raise ValueError(f"Invalid color modifier: {hsv_args}")

    else:
        color_modifiers = named_color_ref.split("_", 1)[1]
        raise ValueError(f"Unsupported color modifiers: {color_modifiers}")
    rgb_color = tuple(round(f, 3) for f in rgb_color)
    return rgb_color


def plot_colortable(show=True):
    """
    Plot matplotlib's named color table.

    Adapted from:
    https://matplotlib.org/stable/gallery/color/named_colors.html
    """

    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 12
    topmargin = 40

    # Sort colors by hue, saturation, value and name.
    by_hsv = sorted(
        (tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))), name)
        for name, color in named_colors.items()
    )
    names = [name for hsv, name in by_hsv]

    n = len(names)
    ncols = 4
    nrows = n // ncols + int(n % ncols > 0)

    width = cell_width * 4 + 2 * margin
    height = cell_height * nrows + margin + topmargin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.patch.set_facecolor("white")  # Add white background to figure
    fig.subplots_adjust(
        margin / width,
        margin / height,
        (width - margin) / width,
        (height - topmargin) / height,
    )
    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * (nrows - 0.5), -cell_height / 2.0)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()
    ax.set_title("Named colors", fontsize=24, loc="left", pad=10)

    for i, name in enumerate(names):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(
            text_pos_x,
            y,
            name,
            fontsize=14,
            horizontalalignment="left",
            verticalalignment="center",
        )

        ax.add_patch(
            Rectangle(
                xy=(swatch_start_x, y - 9),
                width=swatch_width,
                height=18,
                facecolor=named_colors[name],
                edgecolor="0.7",
            )
        )

    if show:
        plt.show()
    else:
        return fig
