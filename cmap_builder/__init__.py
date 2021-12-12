"""
Colormap builder.
"""
from colorsys import hls_to_rgb, hsv_to_rgb, rgb_to_hls, rgb_to_hsv

import numpy as np
from matplotlib import colors as mcolors

# Load all the available named colors in matplotlib
from matplotlib.colors import Normalize, LinearSegmentedColormap, ListedColormap

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


class PiecewiseNorm(Normalize):
    """
    Piecewise linear Norm.

    Normalizes data into the [0.0, 1.0] interval by performing a piecewise linear
    interpolation a non-uniform sequence of N data points over the [0-1] interval.

    The non-uniform data intervals are mapped to evenly-spaced intervals in the [0-1] interval
    using piecewise interpolation.

    (Class adapted from the `matplotlib.colors.Normalize` class).
    """

    def __init__(self, data_points, clip=False):
        """
        Constructor

        Parameters
        ----------
        data_points: array-like (1D)
            Sequence of data points indicating the data segments to map.
        clip: bool
            If True values falling outside the data_points range are mapped to 0 or 1,
            whichever is closer, and masked values are set to 1.
            If False masked values remain masked.

            Clipping silently defeats the purpose of setting the over, under, and
            masked colors in a colormap, so it is likely to lead to surprises;
            therefore the default is clip=False.
        """
        super().__init__(vmin=data_points.min(), vmax=data_points.max(), clip=clip)
        self.data_points = np.sort(np.array(data_points))

    def __call__(self, value, clip=None):
        """
        Normalize *value* data in the ``[vmin, vmax]`` interval into the
        ``[0.0, 1.0]`` interval and return it.

        Parameters
        ----------
        value
            Data to normalize.
        clip : bool
            If ``None``, defaults to ``self.clip`` (which defaults to
            ``False``).
        Notes
        -----
        If not already initialized, ``self.vmin`` and ``self.vmax`` are
        initialized using ``self.autoscale_None(value)``.
        """
        if clip is None:
            clip = self.clip

        result, is_scalar = self.process_value(value)

        self.autoscale_None(result)

        (vmin,), _ = self.process_value(self.vmin)
        (vmax,), _ = self.process_value(self.vmax)
        if vmin == vmax:
            result.fill(0)  # Or should it be all masked?  Or 0.5?
        elif vmin > vmax:
            raise ValueError("minvalue must be less than or equal to maxvalue")
        else:
            if clip:
                mask = np.ma.getmask(result)
                result = np.ma.array(
                    np.clip(result.filled(vmax), vmin, vmax), mask=mask
                )
            # ma division is very slow; we can take a shortcut
            resdat = result.data
            resdat = np.interp(
                resdat, self.data_points, np.linspace(0, 1, num=len(self.data_points))
            )
            result = np.ma.array(resdat, mask=result.mask, copy=False)
        if is_scalar:
            result = result[0]
        return result

    def inverse(self, value):
        if not self.scaled():
            raise ValueError("Not invertible until both vmin and vmax are set")

        if np.iterable(value):
            val = np.ma.asarray(value)
            return np.interp(
                val, np.linspace(0, 1, num=len(self.data_points)), self.data_points
            )

        else:
            return np.interp(
                value, np.linspace(0, 1, num=len(self.data_points)), self.data_points
            )


def build_cmap(name, cmap_def, discrete=False, uniform=False, N=512):
    """
    Build a colormap from a colormap definition (`cmap_def`) specifying the colors
    at each point across the color scale.
    The function returns a colormap, the data value indicating the boundaries of the
    color segments, and a matplotlib's normalization function.

    The colormap definition is a list where each entry represents the color at a given
    data value as:

    cmap_def = [
        (x0, color_0, [next_color_0])  # next_color_0 ignored if provided.
        (x1, color_1, [next_color_1])
        ...
        (xi, color_i, [next_color_i])
        ..
        (xn, color_n, [next_color_n])  # next_color_n is ignored if provided.
    ]
    where `color_i` represents the color immediately before the `xi` the data value.
    The optional `next_color_i` entry can be used to specify the color immediately after
    the `xi` the data value. This allow creating color maps with sharp color transitions.

    Any data interval is supported for the `xi`. For example, the same units as the data
    to plot can be used.

    Parameters
    ----------
    name: str
        Colormap name.
    cmap_def: list
        Colormap definition.
    discrete: bool
        If true, return a discrete colorbar.
        Otherwise, a linear colormap is returned.
    uniform: bool
        If true, an uniform spacing is given to each color segment, regardless their
        of their length. Otherwise, the original spacing specified in the
        colormap definition `cmap_def` is used.
    N: int
        The number of rgb quantization levels for the colorbar.
        512 by default (two times the matplotlib's defafult).

    Returns
    -------
    cmap: ColorMap
        A colormap that mapping data in the [0,1] interval to a given color.
    x_values: list
        The xi values in the colormap definition. This list can be used to place the
        colorbar ticks at the boundaries of each color segment.
    norm: Normalize
        Normalization function that maps the data values [x0, ..., xi, ...,xn] into
        the [0,1] interval. If `uniform` is true, the normalization with map the
        data values into equally spaced color segments in the [0,1] interval.
    """
    seg_data = dict()
    seg_data["red"] = list()
    seg_data["green"] = list()
    seg_data["blue"] = list()

    x_values = np.array([i[0] for i in cmap_def])
    x_min = x_values.min()
    x_max = x_values.max()
    if x_min == x_max:
        raise ValueError("The minimum and maximum x values are equal.")

    full_cmap_def = []
    for _items in cmap_def:
        if len(_items) == 3:
            x, y0_color, y1_color = _items
        elif len(_items) == 2:
            x, y0_color = _items
            y1_color = y0_color
        else:
            raise ValueError("Unexpected number of items in the colormap definition.")

        y0_color = rgb_from_name(y0_color)
        y1_color = rgb_from_name(y1_color)

        x = (x - x_min) / (x_max - x_min)
        full_cmap_def.append((x, y0_color, y1_color))

    x, y0, y1 = zip(*full_cmap_def)

    if discrete:
        y0 = np.roll(y1, 1, axis=0)

    r0, g0, b0 = zip(*y0)
    r1, g1, b1 = zip(*y1)
    if uniform:
        x = np.linspace(0, 1, num=len(x_values))
        norm = PiecewiseNorm(x_values)
    else:
        norm = Normalize(vmin=x_min, vmax=x_max)

    seg_data = dict()
    seg_data["red"] = list(zip(x, r0, r1))
    seg_data["green"] = list(zip(x, g0, g1))
    seg_data["blue"] = list(zip(x, b0, b1))
    cmap = LinearSegmentedColormap(name, seg_data, N=N)

    return cmap, list(x_values), norm
