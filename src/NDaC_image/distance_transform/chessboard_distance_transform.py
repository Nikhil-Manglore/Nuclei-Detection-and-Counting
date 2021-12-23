################################################################################
# Colored image shape: (num_rows, num_pixels_per_row, RGB == const 3)          #
# Grayscale image shape: (num_rows, num_pixels_per_row)                        #
# Colored image:                                                               #
#   numpy.array([ [[0, 255, 0], [RGB]], [[RGB], [RGB]], [[RGB], [RGB]] ])      #
# Grayscale image:                                                             #
#   numpy.array([ [0, 1, 2...], [intensities], [intensities] ])                #
################################################################################

# Importing necessary tools for the further operations.
import numpy as np

# This function returns the distance map for an image.
def chessboard_distance_transform(img):
    # Create the initial state of the distance map, which is an image of zeroes.
    distance_map = np.copy(img)
    np.place(distance_map, distance_map == 255, 0)

    # Calculate the disatnce for each pixel in the image.
    for r, row in enumerate(img):
        for p, px in enumerate(row):
            distance_map[r][p] = determine_distance(img, r, p, px)

    return distance_map

# This function determines the distance to the closest non-feature pixel. This
# is the chess transform.
def determine_distance(img, r, p, px):
    # If the pixel is non-feature - the distance to the non-feature pixel is 0.
    if px == 0:
        return 0

    # Pad the image, so that there are no indexing issues.
    pad_size = max(np.shape(img)[0], np.shape(img)[1])
    pad_img = np.pad(np.copy(img), [(pad_size, pad_size), (pad_size, pad_size)],
                     mode="constant", constant_values=255)

    # Update indexing according to the padding parameters.
    r = r + pad_size
    p = p + pad_size

    # The distance to the closest non-feature element.
    n_start = 1
    n = n_start

    # The minimum is the minimum value within the kernel. The moment the minimum
    # switches from 255 to 0 - non-feature element is detected.
    minimum = 255
    
    # Continue the search until the non-feature element is found.
    while minimum != 0:
        # If the kernel size is the size of the padded image - throw an error.
        if (r - n == 0 or r + n == np.shape(pad_img)[0] or
            p - n == 0 or p + n == np.shape(pad_img)[1]):
            raise ValueError("Image does not have non-feature elements.")

        # Update the minimum to detect non-feature elements.
        minimum = np.amin(np.copy(pad_img)[r - n:r + n, p - n:p + n])

        # Return an appropriate value on the 255 scale if non-feature element is
        # detected.
        if minimum == 0:
            indexes = np.where(np.copy(pad_img)[r - n:r + n, p - n:p + n] == 0)
            distance = 0
            for i, el in enumerate(indexes[0]):
                if max(abs(indexes[0][i] - n), abs(indexes[1][i] - n)) > distance:
                    distance = max(abs(indexes[0][i] - n), abs(indexes[1][i] - n))
            if distance >= 255:
                return 255
            else:
                return distance
        
        # Update the distance if no non-feature elements were found.
        else:
            n = n + 1
