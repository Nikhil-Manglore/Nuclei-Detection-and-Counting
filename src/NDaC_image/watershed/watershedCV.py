################################################################################
# Colored image shape: (num_rows, num_pixels_per_row, RGB == const 3)          #
# Grayscale image shape: (num_rows, num_pixels_per_row)                        #
# Colored image:                                                               #
#   numpy.array([ [[0, 255, 0], [RGB]], [[RGB], [RGB]], [[RGB], [RGB]] ])      #
# Grayscale image:                                                             #
#   numpy.array([ [0, 1, 2...], [intensities], [intensities] ])                #
################################################################################

# Import all the necessary tools for further operations. 

import cv2 
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg 
from ..otsu import *
from ..filters import *
from ..general import *
from ..sequences import *


# Parameters: image - initial input image
# Return Value: pixel_array - the array of pixels that were obtained from the input image
# This function takes in an initial input image and returns an array that contains all the pixel values. Added 10/3/2021
def image_to_array(image):
    pixel_array = to_grayscale(image)
    
    return pixel_array

#Parameters: pixel_array - the grayscale image
#Return value - parsed_image - the image obtained after thresholding.
#This function takes in the grayscale image as pixels, performs thresholding on it, and returns an binarized image. Added 10/3/2021
def parse_image(pixel_array):
    threshold = get_threshold_inter(pixel_array)
    parsed_image = threshold_parser(pixel_array, threshold)
    return parsed_image

# Parameters:
# parsed_image - the binarized image obtained after thresholding and parsing
# n - window size used for performing opening
# Return value - opened_image - The image obtained after opening on the foreground of the image
# This function performs opening (erosion followed by dilation) on the binarized image, to obtain markers for watershed segmentation. Added 10/3/2021
def perform_opening(parsed_image, n):
    opened_image = opening(parsed_image, n)
    return opened_image

# Parameters:
# parsed_image - the thresholded image
# Return value - dilated_image - The image obtained after dilation
# This function performs dilation on the thresholded image. Added 10/3/2021
def bg_dilation(parsed_image):
    dilated_image = get_dilated_image(parsed_image)
    return dilated_image

# Parameters:
# dilated_image - the image obtained after dilation
# closed_image - the image obtained after closing
# Return value - markers - An array the size of the original image that contains all the markers used for watershed transform. 
# This function gets all the markers used to perform the watershed transform/segmentation of the image. Added 10/3/2021
def get_markers(closed_image):
    # The regions that are definitely a part of the foreground are the ones that are obtained after performing opening on
    # the original image.
    sure_fg = np.uint8(closed_image) #not sure about this
    kernel = np.ones((3,3),np.uint8)
    sure_bg = cv2.dilate(sure_fg, kernel,iterations=3) #using this instead of our dilation method so that the data types going into 
    #the cv2.subtract method are the same. This is necessary so that we can use the distance transform instead of just
    #the opened image for the sure foreground
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(sure_fg,cv2.DIST_L2,5)
    #ret, sure_fg = cv2.threshold(dist_transform,0.5*dist_transform.max(),255,0)
    #sure_fg = dist_transform
    sure_fg = np.uint8(sure_fg)
    
    #dilated_image = np.uint8(dilated_image)
    unknown = cv2.subtract(sure_bg, sure_fg)
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    # Now, mark the region of unknown foreground/background quality with zero
    markers[unknown==255] = 0
    return markers
      
# Parameters: opened_image - The array that is obtained after performing opening on the foreground of the image
# Return value -  grayscale_image - The converted grayscale array after the watershed method has been performed
# This method takes in the markers and the grayscale_image and performs the watershed method by using the OpenCV function.
def marker_watershed(markers, grayscale_img):
    markers = cv2.watershed(grayscale_img, markers)
    grayscale_img[markers == -1] = [255,0,0] 
    return grayscale_img  
    
# # Parameters: 
# # input_image - The original image used
# # window_size - The strel used to perform opening of the image, can be varied by the user.
# # Return value -  watershed_image - The converted grayscale array after the watershed method has been performed
# # This method performs the watershed transformation on the grayscale image by consolidating all the methods above. 
def perform_watershed(input_image, window_size, n_blur, n_dilation, v_exposure):
    #final_pixel_array = image_to_array(input_image)
    #image_viewer(final_pixel_array)
    #final_blurred_image = get_gaussian_blurred_image(final_pixel_array,23)
    #final_edge_detection_image = detect_edge(final_blurred_image) # Testing
    #final_parsed_image = parse_image(final_blurred_image)
    #image_viewer(final_parsed_image)

    final_parsed_image = detect_area_of_interest(input_image, n_blur, n_dilation, v_exposure)
    for index in range(6): # Ran erosion six times
        final_parsed_image = get_eroded_image(final_parsed_image, 3)
        #image_viewer(final_parsed_image)
    final_parsed_image = get_dilated_image(final_parsed_image, 3)
    image_viewer(final_parsed_image)
    opened_image = perform_opening(final_parsed_image, window_size)
    #image_viewer(opened_image)
    closed_image = closing(opened_image,window_size)
    #image_viewer(closed_image)
    returned_markers = get_markers(closed_image)
    #returned_markers = returned_markers*6 #Testing
    #image_viewer(returned_markers)
    watershed_image = marker_watershed(returned_markers, input_image.og_img)
    image_viewer(watershed_image)

    return watershed_image
