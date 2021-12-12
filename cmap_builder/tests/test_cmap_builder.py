from cmap_builder import build_cmap


def test_cmap_builder():
    """Test the cmap builder."""
    cmap_def = [
        (0, "red_dark"),
        (2, "red_light", "orange_light"),
        (4, "orange_dark", "blue_light"),
        (8, "blue_dark", "purple_light"),
        (9, "purple_dark", "green_light"),
        (10, "green_dark"),
    ]

    quantization_levels = 280

    my_cmap, my_ticks, my_norm = build_cmap(
        "test",  # Name of the colormap
        cmap_def,
        uniform=True,
        N=quantization_levels,
    )

    expected_segment_data = {
        "red": [
            (0.0, 0.2, 0.2),
            (0.2, 1.0, 1.0),
            (0.4, 0.2, 0.6),
            (0.6000000000000001, 0.0, 1.0),
            (0.8, 0.2, 0.6),
            (1.0, 0.0, 0.0),
        ],
        "green": [
            (0.0, 0.0, 0.0),
            (0.2, 0.6, 0.859),
            (0.4, 0.129, 0.6),
            (0.6000000000000001, 0.0, 0.6),
            (0.8, 0.0, 1.0),
            (1.0, 0.2, 0.2),
        ],
        "blue": [
            (0.0, 0.0, 0.0),
            (0.2, 0.6, 0.6),
            (0.4, 0.0, 1.0),
            (0.6000000000000001, 0.2, 1.0),
            (0.8, 0.2, 0.6),
            (1.0, 0.0, 0.0),
        ],
    }

    assert expected_segment_data == my_cmap._segmentdata
    assert quantization_levels == my_cmap.N
