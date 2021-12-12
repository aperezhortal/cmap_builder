# Colormap builder

A simple tool to create custom colormaps for matplotlib.

## Usage

Matplotlib allows creating different types colormaps using the 
[ListedColormap](https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.ListedColormap.html#matplotlib.colors.ListedColormap) or [LinearSegmentedColormap](https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html#matplotlib.colors.LinearSegmentedColormap) classes.
However, they are either limited in scope (ListedColormap or LinearSegmentedColormap.from_list) or require defining the mapping for each primary color (r,g,b).

The cmap_builder.build_cmap()` function provided by this package exposes a simple interface to create complex colormaps simply by specifying the colors at different points across the color scale. This approach was largely inspired by the way of defining colormaps in the [legs](https://domutils.readthedocs.io/en/stable/legsTutorial.html) module in the [domutils package] (https://domutils.readthedocs.io).

The colormap definition required by `build_cmap` is a list of (data value, color, [next_color]) tuples like the following:
```
cmap_def = [
    (x0, color_0, [next_color_0])  # next_color_0 ignored if provided.
    (x1, color_1, [next_color_1])
    ...
    (xi, color_i, [next_color_i])
    ..
    (xn, color_n, [next_color_n])  # next_color_n is ignored if provided.
]
```
where `color_i` represents the color immediately before the `xi` the data value.
The optional `next_color_i` entry can be used to specify the color immediately after
the `xi` the data value. This allows creating color maps with sharp color transitions.
Here, the `xi` values are not restricted to the [0,1] interval as in the matplotlib tools. Instead, any data interval is supported for the `xi`. Hence, we can use the same units as the data we want to plot, making the definition of
colormaps easier.

#### Example

For example, the following code creates a colormap that:

- From 0 to 2 varies from dark to light green.
- From 2, 4 varies from dark to light purple.
- From 4-8 varying from dark to light orange.
- From 8-9 varies from dark to light yellow.
- From 9-10 varies from dark to light green.

```python
from cmap_builder import build_cmap
cmap_def = [
    # (value, color)
    (0, "red_dark"),
    (2, "red_light", "orange_light"),
    (4, "orange_dark", "blue_light"),
    (8, "blue_dark", "purple_light"),
    (9, "purple_dark", "green_light"),
    (10, "green_dark"),
]

my_cmap, my_ticks, my_norm = build_cmap(
    "my_colormap", # Name of the colormap
    cmap_def, # Colormap definition
    uniform=True, 
    N=700,  # color palette quantization levels.
)

# uniform=True creates norm that maps the input values to equally 
# spaced color segments 
```

Check the [project's example gallery](#) for a short tutorial showcasing other the capabilities of this library.

## Installation

You can install the packagge directly from github using:
```console
pip install git+https://github.com/aperezhortal/cmap_builder.git
```

Alternatively, you can install the package from the source by cloning the project
and then running:
```console
pip install .  # Regular installation
# or 
pip install -e .  # Install in development mode]()
```