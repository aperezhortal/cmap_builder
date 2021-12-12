==============================================
Welcome to the Colormap builder documentation!
==============================================

Cmap_builder is a simple tool to create custom colormaps for matplotlib.

Why using this tool?
====================

Matplotlib allows creating different types colormaps using the
`ListedColormap <https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.ListedColormap.html#matplotlib.colors.ListedColormap>`_) or `LinearSegmentedColormap <https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html#matplotlib.colors.LinearSegmentedColormap>`_ classes. However, they are either limited in scope (ListedColormap or LinearSegmentedColormap.from_list) or require defining the mapping for each primary color (r,g,b).

The cmap_builder.build_cmap()` function provided by this package exposes a simple interface to create complex colormaps simply by specifying the colors at different points across the color scale.

The colormap definition required by `build_cmap` is a list of (data value, color, [next_color]) tuples like the following::

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
the `xi` the data value. This allows creating color maps with sharp color transitions.

The `xi` values are not restricted to the [0,1] interval as in the matplotlib tools.
Instead, any data interval is supported for the `xi`.
Hence, we can use the same units as the data we want to plot, making the definition of
colormaps easier.

Documentation
=============

The documentation is divided in two sections.

:ref:`example_gallery`
~~~~~~~~~~~~~~~~~~~~~~

This sections contains the tutorials explainig how to use this library, and a developers reference.

:ref:`dev_reference`
~~~~~~~~~~~~~~~~~~~~~

The documentation of each library module.

.. toctree::
    :maxdepth: 1
    :caption: Contents:

    gallery/index
    dev_reference/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
