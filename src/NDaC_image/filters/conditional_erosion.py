################################################################################
# File collaboration - 11/27/2021                                               #
#   Nikhil Manglore, Aubrey Gatewood, Annapoorna Prabhu                        #
################################################################################
# Colored image shape: (num_rows, num_pixels_per_row, RGB == const 3)          #
# Grayscale image shape: (num_rows, num_pixels_per_row)                        #
# Colored image:                                                               #
#   numpy.array([ [[0, 255, 0], [RGB]], [[RGB], [RGB]], [[RGB], [RGB]] ])      #
# Grayscale image:                                                             #
#   numpy.array([ [0, 1, 2...], [intensities], [intensities] ])                #
################################################################################
import cv2
from NDaC_image import *
import numpy as np
from ..otsu import *
from ..filters import *
from ..general import *
from ..sequences import *

#Parameters:
# image - area of interest detected image
# coarse_t - 
# fine_t -
def conditional_erosion(image, coarse_t, fine_t):
    coordinate_map = {"Coordinate Key":[], "Total Area":[]}


    data = getConnected_Area(image)
    num_of_components = data[0]
    area = data[1]
    top_x = data[2]
    top_y = data[3]
    width = data[4]
    height = data[5]
    coordinate = np.zeros(2)

    #for component in range(1, num_of_components):
        #coordinate[0] = top_x[component]
        #coordinate[1] = top_y[component]
        #coordinate_map["Coordinate Key"].append(coordinate)
        #coordinate_map["Total Area"].append(area)

        #first_value = list(coordinate_map.items())[component][1]
        #print(first_value)
    


    #print("Number of Components")
    #print(num_of_components)
    #print("Area")
    #print(area)
    #print("Top X")
    #print(top_x)
    #print("Top Y:")
    #print(top_y)
    #print("Width")
    #print(width)
    #print("Height")
    #print(height)
    

#Parameters:
# image - area of interest detected image
# Return Value -
# numLabels - number of components in the image
# area - area of the entire image
# Added - 11/27/2021 - Annapoorna Prabhu
def getConnected_Area(image):
    image = np.uint8(image)
    ret,image_connected = cv2.connectedComponents(image)
    image_viewer(image_connected)
    components_labels = cv2.connectedComponentsWithStats(image)
    #Labels of each component
    (numLabels, labels, stats,centroids) = components_labels
    area = np.zeros(numLabels)
    top_x = np.zeros(numLabels)
    top_y = np.zeros(numLabels)
    width = np.zeros(numLabels)
    height = np.zeros(numLabels)
    #Area of each component
    for label in range(numLabels):
        area[label] = stats[label, cv2.CC_STAT_AREA]
        top_x[label] = stats[label, cv2.CC_STAT_LEFT]
        top_y[label] = stats[label, cv2.CC_STAT_TOP]
        width[label] = stats[label, cv2.CC_STAT_WIDTH]
        height[label] = stats[label, cv2.CC_STAT_HEIGHT]
    

    return numLabels, area, top_x, top_y, width, height #number, then 5 arrays
