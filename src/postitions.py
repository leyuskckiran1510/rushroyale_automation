og_size = (338, 601)
og_window = (354, 640)
unit_area = [[54, 348], [288, 491]]


spwanner = [[127, 494], [213, 531]]


hero = [[266, 534], [331, 594]]

deck = [
    [[13, 546], [49, 580]],
    [[66, 545], [102, 583]],
    [[116, 547], [152, 580]],
    [[168, 547], [203, 581]],
    [[219, 545], [258, 580]],
]


def scale_coordinates(new_screen, old_screen, coordinates):
    old_width, old_height = old_screen
    new_width, new_height = new_screen

    scaled_coordinates = []
    for coord in coordinates:
        scaled_x = int(coord[0] * new_width / old_width)
        scaled_y = int(coord[1] * new_height / old_height)
        scaled_coordinates.append([scaled_x, scaled_y])

    return scaled_coordinates


def resize_poses(new_screen, change):
    # global unit_area, hero, deck, spwanner
    # hero = scale_coordinates(new_screen, og_size, hero)
    # spwanner = scale_coordinates(new_screen, og_size, spwanner)
    if len(change) > 0 and len(change[0]) > 0 and isinstance(change[0][0], list):
        _deck = []
        for d in change:
            _deck.append(scale_coordinates(new_screen, og_size, d))
        change = _deck.copy()
    else:
        change = scale_coordinates(new_screen, og_size, change)
    return change


# average colors for empty ground
empty = [
    [49.0, 131.0, 139.0],
    [40.0, 133.0, 121.0],
    [64.0, 175.0, 166.0],
    [45.0, 142.0, 130.0],
    [70.0, 165.0, 150.0],
    [54.0, 175.0, 145.0],
    [71.0, 170.0, 157.0],
    [59.0, 178.0, 155.0],
    [77.0, 185.0, 162.0],
    [51.0, 162.0, 148.0],
    [78.0, 187.0, 170.0],
    [54.0, 175.0, 146.0],
    [60.0, 140.0, 137.0],
    [52.0, 156.0, 131.0],
    [65.0, 161.0, 143.0],
]
