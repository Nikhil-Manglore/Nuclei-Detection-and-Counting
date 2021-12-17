################################################################################
# File collaboration:                                                          #
#   Tikhon Pachin                                                              #
################################################################################
# Grayscale image shape: (num_rows, num_pixels_per_row)                        #
# Grayscale image:                                                             #
#   numpy.array([ [0, 1, 2...], [intensities], [intensities] ])                #
################################################################################

# Importing necessary tools for the further operations.
# Tikhon Pachin - 10/3/2021
import numpy as np

class Minimum:
    def __init__(self, r, p, intensity):
        self.r = r
        self.p = p
        self.intensity = intensity
        self.connecting_pixels = []

# Working 10/03/2021
def get_watershed(img, n_dilation, mode=0):
    topographical_map = convert_image_to_topographical_map(img, 19, mode)
    cell_minima = detect_regional_minima(topographical_map, 19)
    ceiling_function = img.get_dilated_image(np.copy(topographical_map), n_dilation)

    # UNCOMMENT TO VIEW THE TOPOGRAPHICAL MAP OR THE CEILING FUNCTION
    ############################################################################
    img.view(topographical_map)
    img.view(ceiling_function)
    ############################################################################
    # UNCOMMENT TO VIEW THE LOCATIONS OF ALL CELL MINIMA
    ############################################################################
    '''for minimum in cell_minima:
        print("[r: " + str(minimum.r) + ", p: " + str(minimum.p) + "]")'''
    ############################################################################

    topographical_map = np.pad(np.copy(topographical_map), [(1, 1), (1, 1)],
                     mode="constant", constant_values=255)
    flooded_img = flood(topographical_map, cell_minima, ceiling_function)

    # UNCOMMENT TO VIEW THE TOPOGRAPHICAL MAP OR THE CEILING FUNCTION
    ############################################################################
    img.view(flooded_img)
    ############################################################################

    borders = np.copy(flooded_img)
    np.place(borders, borders > 0, 255)
    np.place(borders, borders == 0, 255 + 255)
    borders = borders - 255

    borders = img.get_edged_image(borders)

    segmented_image = np.copy(img.gray_img) + borders[1:borders.shape[0] - 1, 1:borders.shape[1] - 1]
    np.place(segmented_image, segmented_image > 255, 255)

    return segmented_image

def invert_distance_map(data):
    np.place(data, data <= 255, 255 - data * 6)
    return data

def convert_image_to_topographical_map(img, n_blur, mode):
    if mode == 0:
        preprocessed = img.get_areas_of_interest(img, 23, 9, 30)
    elif mode == 1:
        preprocessed = img.gray_img
    else:
        raise ValueError("Invalid mode option. 0 - image needs preprocessing," +
                         " 1 - image does not need preprocessing.")

    distance_map = img.get_euclidean_distance_map(preprocessed)

    # UNCOMMENT AND ADJUST AFTER TESTING IS COMPLETE
    ############################################################################
    distance_map = img.get_gaussian_blur_image(np.copy(distance_map), n_blur)
    ############################################################################

    inverted_map = invert_distance_map(np.copy(distance_map))

    return inverted_map

def detect_regional_minima(topographical_map, n):
    pad_size = topographical_map.shape[0]
    pad_img = np.pad(np.copy(topographical_map), [(pad_size, pad_size), (pad_size, pad_size)],
                     mode="constant", constant_values=255)

    position_array = []
    offset = int((n - 1) / 2)

    for r, row in enumerate(topographical_map):
        for p, px in enumerate(row):
            i = r + pad_size
            j = p + pad_size
            kernel = pad_img[i - offset:i + offset + 1, j - offset:j + offset + 1]
            minimum = np.min(kernel)
            if topographical_map[r][p] == minimum and topographical_map[r][p] < 255:
                position_array.append(Minimum(r, p, minimum))

    return position_array

def flood(t_map, minima, c_map):
    for minimum in minima:
        t_map[minimum.r][minimum.p] = 0 #c_map[minimum.r][minimum.p]
        t_map = look_around(t_map, minimum, c_map[minimum.r][minimum.p])

    return t_map

def look_around(t_map, minimum, c_value):
    new_minima = []

    if (t_map[minimum.r - 1][minimum.p - 1] < c_value) and (t_map[minimum.r - 1][minimum.p - 1] != 0):
        new_minima.append(Minimum(minimum.r - 1, minimum.p - 1, c_value))
    if (t_map[minimum.r - 1][minimum.p] < c_value) and (t_map[minimum.r - 1][minimum.p] != 0):
        new_minima.append(Minimum(minimum.r - 1, minimum.p, c_value))
    if (t_map[minimum.r - 1][minimum.p + 1] < c_value) and (t_map[minimum.r - 1][minimum.p + 1] != 0):
        new_minima.append(Minimum(minimum.r - 1, minimum.p + 1, c_value))
    if (t_map[minimum.r][minimum.p - 1] < c_value) and (t_map[minimum.r][minimum.p - 1] != 0):
        new_minima.append(Minimum(minimum.r, minimum.p - 1, c_value))
    if (t_map[minimum.r][minimum.p] < c_value) and (t_map[minimum.r][minimum.p] != 0):
        new_minima.append(Minimum(minimum.r, minimum.p, c_value))
    if (t_map[minimum.r][minimum.p + 1] < c_value) and (t_map[minimum.r][minimum.p + 1] != 0):
        new_minima.append(Minimum(minimum.r, minimum.p + 1, c_value))
    if (t_map[minimum.r + 1][minimum.p - 1] < c_value) and (t_map[minimum.r + 1][minimum.p - 1] != 0):
        new_minima.append(Minimum(minimum.r + 1, minimum.p - 1, c_value))
    if (t_map[minimum.r + 1][minimum.p] < c_value) and (t_map[minimum.r + 1][minimum.p] != 0):
        new_minima.append(Minimum(minimum.r + 1, minimum.p, c_value))
    if (t_map[minimum.r + 1][minimum.p + 1] < c_value) and (t_map[minimum.r + 1][minimum.p + 1] != 0):
        new_minima.append(Minimum(minimum.r + 1, minimum.p + 1, c_value))

    while len(new_minima) != 0:
        for loc_minimum in new_minima: 
            t_map[loc_minimum.r][loc_minimum.p] = 0 #c_value
            new_minima.remove(loc_minimum)
            neighbors = check_neighbors(t_map, loc_minimum, c_value)

        for neighbor in neighbors:
            new_minima.append(neighbor)

    return t_map

def check_neighbors(t_map, minimum, c_value):
    new_minima = []

    if (t_map[minimum.r - 1][minimum.p - 1] < c_value) and (t_map[minimum.r - 1][minimum.p - 1] != 0):
        new_minima.append(Minimum(minimum.r - 1, minimum.p - 1, c_value))
    if (t_map[minimum.r - 1][minimum.p] < c_value) and (t_map[minimum.r - 1][minimum.p] != 0):
        new_minima.append(Minimum(minimum.r - 1, minimum.p, c_value))
    if (t_map[minimum.r - 1][minimum.p + 1] < c_value) and (t_map[minimum.r - 1][minimum.p + 1] != 0):
        new_minima.append(Minimum(minimum.r - 1, minimum.p + 1, c_value))
    if (t_map[minimum.r][minimum.p - 1] < c_value) and (t_map[minimum.r][minimum.p - 1] != 0):
        new_minima.append(Minimum(minimum.r, minimum.p - 1, c_value))
    if (t_map[minimum.r][minimum.p] < c_value) and (t_map[minimum.r][minimum.p] != 0):
        new_minima.append(Minimum(minimum.r, minimum.p, c_value))
    if (t_map[minimum.r][minimum.p + 1] < c_value) and (t_map[minimum.r][minimum.p + 1] != 0):
        new_minima.append(Minimum(minimum.r, minimum.p + 1, c_value))
    if (t_map[minimum.r + 1][minimum.p - 1] < c_value) and (t_map[minimum.r + 1][minimum.p - 1] != 0):
        new_minima.append(Minimum(minimum.r + 1, minimum.p - 1, c_value))
    if (t_map[minimum.r + 1][minimum.p] < c_value) and (t_map[minimum.r + 1][minimum.p] != 0):
        new_minima.append(Minimum(minimum.r + 1, minimum.p, c_value))
    if (t_map[minimum.r + 1][minimum.p + 1] < c_value) and (t_map[minimum.r + 1][minimum.p + 1] != 0):
        new_minima.append(Minimum(minimum.r + 1, minimum.p + 1, c_value))

    return new_minima
