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

# From color to grayscale converter. 
def to_grayscale(image):
    # Check if the input image is of correct shape. Processing wrong shape
    # may cause runtime errors. This is important because some data may already
    # be converted to grayscale and some may be corrupted.
    if len(image.shape) != 3:
        if len(image.shape) == 2:
            return image
        else:
            raise ValueError("Input array must be of shape " +
                             "(row, pixels per row, 3) or " +
                             "(row, pixels per row)")
    elif image.shape[2] != 3:
        raise ValueError("There should only be either 3 values per pixel " +
                         "for an RGB image or 1 value per pixel for " +
                         "grayscale.")

    # Initiate grayscale image array full of zeros to optimize performance.
    # This array will be later filled with data values of the grayscale image.
    # The shape of the array is the number of rows of the colored image and
    # the number of pixels per each row. There is no need to make pixels into
    # their own arrays since there is only one component (intensity) per pixel.
    gray_image = np.zeros((image.shape[0], image.shape[1]))

    # To convert a colored image into a grayscale image the following formulas
    # could be used:
    #   ITU-R Recommendation BT.709: Y = 0.2126R + 0.7152G + 0.0722B - selected
    #   ITU-R Recommendation BT.601: Y = 0.299R + 0.587G + 0.114B
    # Conversion is complete through itereation of each row and each pixel of
    # each row. Refer to the header of this file to see colored image structure
    # and grayscale image structure.
    for r, row in enumerate(image):
        for p, px in enumerate(row):
            gray_image[r][p] = 0.2126 * px[0] + 0.7152 * px[1] + 0.0722 * px[2]

    # Since grayscale images only support 0-255 integer values we must convert
    # the computed values into their appropriate integer values. This is done
    # through rounding and type casting. The converted values are returned from
    # this function. See the structure of a grayscale image in the header of
    # this file. 
    return np.round_(gray_image, decimals=0).astype(int)
