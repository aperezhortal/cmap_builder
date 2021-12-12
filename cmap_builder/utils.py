"""
Helper functions.
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from cmap_builder import named_colors


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
