################################################################################               
#Added 09/27/2021                                                              #
################################################################################

from .dilation import *
from .erosion import *

# This method will perform the morphological operation of closing on an image
# Parameters:
# image --> the input image array that has already been parsed. The values of this array will be either 0 or 255.
# n --> the window size that the user wants. Ex. 3x3, 5x5, 7x7
# Return Value: the closed image array
def closing(image, n):

    dilated_image = get_dilated_image(image, n)
    eroded_image = get_eroded_image(dilated_image, n)

    return eroded_image
