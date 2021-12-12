# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------
import configparser
import os
import sys
from pathlib import Path

project = "cmap_builder"
copyright = "2021, Andrés Pérez Hortal"
author = "Andrés Pérez Hortal"

# Get release number from the setup.cfg file
setup_cfg_path = os.path.join(os.path.dirname(__file__), "../setup.cfg")
config = configparser.ConfigParser()
config.read(setup_cfg_path)
release = config["metadata"]["version"]

# Add sources to the path env variable
DOCS_DIR = Path(__file__).parent
PROJECT_ROOT = (DOCS_DIR / "../").resolve()

sys.path.insert(1, str(PROJECT_ROOT))
sys.path.insert(1, str(PROJECT_ROOT / "examples"))
sys.path.insert(1, ".")

# -- General configuration ---------------------------------------------------
extensions = [
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "nbsphinx",
    "nbsphinx_link",
    "sphinx_gallery.load_style",
    "sphinx.ext.mathjax",
    "m2r2",
]
exclude_patterns = ["_build", "**.ipynb_checkpoints"]

html_theme = "sphinx_rtd_theme"

html_domain_indices = True
autosummary_generate = True
numpydoc_show_class_members = False
autosummary_imported_members = True
