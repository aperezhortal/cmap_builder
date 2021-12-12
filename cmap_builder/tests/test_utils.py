import pytest

from cmap_builder.utils import rgb_from_name

input_colors = (
    # (color_name, expected rgb_value)
    ("red", (1.0, 0.0, 0.0)),
    ("red_light", (1.0, 0.6, 0.6)),
    ("red_dark", (0.2, 0.0, 0.0)),
    ("red_l10", (0.2, 0.0, 0.0)),
    ("red_l80", (1.0, 0.6, 0.6)),
    ("red_s50", (1.0, 0.5, 0.5)),
    ("red_v50", (0.5, 0.0, 0.0)),
    ("yellow_v60", (0.6, 0.6, 0.0)),
    ("firebrick_s60", (0.698, 0.279, 0.279)),
)


@pytest.mark.parametrize("color_name, rgb_value", input_colors)
def test_rgb_from_name(color_name, rgb_value):
    """Test the `rgb_from_name` function."""
    assert rgb_from_name(color_name) == rgb_value
