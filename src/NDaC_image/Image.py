################################################################################
# File collaboration:                                                          #
#   Tikhon Pachin                                                              #
################################################################################
# Colored image shape: (num_rows, num_pixels_per_row, RGB == const 3)          #
# Grayscale image shape: (num_rows, num_pixels_per_row)                        #
# Colored image:                                                               #
#   numpy.array([ [[0, 255, 0], [RGB]], [[RGB], [RGB]], [[RGB], [RGB]] ])      #
# Grayscale image:                                                             #
#   numpy.array([ [0, 1, 2...], [intensities], [intensities] ])                #
################################################################################

# Import all the necessary tools for operations.
import os
import numpy as np
from .otsu import *
from .filters import *
from .general import *
from .sequences import *
from .distance_transform import *
from .watershed import *

# Map the path to the resources folder. Any image that needs to be run through
# any algorithm or logic of the code must be there. Tikhon Pachin - 9/20/2021
RESOURCES_PATH = os.path.dirname(os.path.abspath(__file__))  + "/resources/"

# The general class of an Image upon which operations are completed.
# Tikhon Pachin 9/20/2021
class ImageClass:
    # Class initialization takes in the name of the target file in the resources
    # folder. Tikhon Pachin - 9/20/2021
    def __init__(self, filename):
        self.og_img = image_uploader(filename) #np.asarray(mpimg.imread(RESOURCES_PATH + filename))
        self.gray_img = to_grayscale(self.og_img)

    # This function maps to the grayscale image viewer. The input is any image
    # that the user wants to see and the output is just a displayed plot.
    # Tikhon Pachin - 9/20/2021
    def view(self, image):
        image_viewer(image)

    # Otsu threshold retriever. Takes in a full image or a part of an image and
    # returns the desired threshold. Tikhon Pachin - 9/20/2021
    def get_otsu_threshold(self, data):
        # Diversify the threshold retrieving method to proofcheck the work of
        # the algorithm. Tikhon Pachin - 9/20/2021
        #intra_threshold = get_threshold_intra(data)
        inter_threshold = get_threshold_inter(data)

        # Compare the outputs of both methods to see if any bug or run time 
        # error was detected. Tikhon Pachin - 9/20/2021
        #if intra_threshold == inter_thredhold:
        return inter_threshold
        #else:
        #    raise RuntimeError("Error computing the threshold")

    # This function maps to the otsu threshold parser through the given image
    # (or its part). Tikhon Pachin - 9/20/2021
    def otsu_parser(self, data, threshold):
        return threshold_parser(data, threshold)

    # This function maps to the dilation filter with a filter of size n by n. 
    # n must be an odd integer - 09/21/2021 Yu-Hsuan Lin
    def get_dilated_image(self, data, n):
        return get_dilated_image(data,n)

    # This function maps to the erosion filter with a filter of size n by n. 
    # n must be an odd integer - 09/21/2021 Yu-Hsuan Lin
    def get_eroded_image(self, data, n):
        return get_eroded_image(data,n)

    # This function maps to the edge detection filter with structuring element
    # of nxn, where n must be an odd integer. Tikhon Pachin - 9/28/2021
    def get_edged_image(self, data):
        return detect_edge(data)

    def get_opening_image(self, data, n):
        return opening(data, n)

    def get_closing_image(self, data, n):
        return closing(data, n)

    # This function returns the image that has been gaussian blurred.
    # Tikhon Pachin - 10/16/2021
    def get_gaussian_blur_image(self, data, n):
        return get_gaussian_blurred_image(data, n)

    # This function detects the areas of interest on the original image.
    # Tikhon Pachin - 10/16/2021
    def get_areas_of_interest(self, data, n_blur, n_dilation, v_exposure):
        return detect_area_of_interest(data, n_blur, n_dilation, v_exposure)

    # This function implements the chessboard distance transform.
    # Tikhon Pachin - 10/18/2021
    def get_chessboard_distance_map(self, data):
        return chessboard_distance_transform(data)

    # This function implements the watershed segmentation from scratch.
    # img - image class to operate on using its own tools
    # n_dilation - kernel size to create the ceiling function
    # mode - 0 if image needs preprocessing (area of interest detection), 1 else
    # Tikhon Pachin - 11/22/2021
    def get_watershed_image(self, img, n_dilation, mode=0):
        return get_watershed(img, n_dilation, mode)

    def get_euclidean_distance_map(self, data):
        return euclidean_distance_transform(data)
        
    # This function implements the city-block distance transform.
    # Yu-Hsuan Lin - 10/25/2021
    def get_cityblock_distance_map(self, data):
        return cityblock_distance_transform(data)

    # This function filter/smooth the image by simple moving average.
    # Yu-Hsuan Lin - 11/07/2021
    def get_average_filter_image(self, data, n):
        return average_filter(data, n)

    # This function filter the image with median filter.
    # Yu-Hsuan Lin - 11/07/2021
    def get_median_filter_image(self, data, n):
        return median_filter(data, n)