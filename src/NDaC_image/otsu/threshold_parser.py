################################################################################
# Import necessary tools for further operations
import numpy as np

# Parameters:
# Image - A 2D array that contains all the pixel values of an image
# Threshold - The threshold value that was calculated.
# Return Value - The array with all the values of the pixels converted to either 0 or 255.
# This function will loop over all the pixel values and will set them to 0 or 255 depending on whether or not they are greater than the threshold value.

def threshold_parser(image, threshold):
    np.place(image, image <= threshold, 0)
    np.place(image, image > threshold, 255)

    return image
