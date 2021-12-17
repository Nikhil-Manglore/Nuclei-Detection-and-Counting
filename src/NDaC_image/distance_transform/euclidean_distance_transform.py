################################################################################
# File collaboration:                                                          #
#   Niharika Narra, Lydia Hanna                                                #
################################################################################
# Colored image shape: (num_rows, num_pixels_per_row, RGB == const 3)          #
# Grayscale image shape: (num_rows, num_pixels_per_row)                        #
# Colored image:                                                               #
#   numpy.array([ [[0, 255, 0], [RGB]], [[RGB], [RGB]], [[RGB], [RGB]] ])      #
# Grayscale image:                                                             #
#   numpy.array([ [0, 1, 2...], [intensities], [intensities] ])                #
################################################################################

#importing the necessary modules 
import numpy as np
import math as m
from PIL import Image

#Euclidean distance tranform function creates a distance map from a binary input image to
#return the minimum distance from each pixel to the nearest boundary element.
def euclidean_distance_transform(img):
    #Creates an array filled with values of 255 for the final output
    distImg = np.full((img.shape[0],img.shape[1]),255, dtype =float)

    #Calculates the distance between the pixel and the boundary element
    distImg = get_distance(img,distImg)

    return distImg

#The getDistance function calculates the distance between the pixel and the nearest non-feature element
# using the distance formula.
def get_distance (img, distImg):
    #iterates through each pixel of the image
    for row in range(0, len(img)):
        for col in range(0, len(img[row])): 
            #checks for a non-feature pixel
            if img[row][col].all() == 0:
                #if it is a non-feature pixel, update the distance map to a value of 0
                distImg[row][col] = 0
            #for feature pixels    
            else:
                n = 0
                find_element = True
                #until non-feature element is found
                while find_element: 
                    #increment the border of the search by 1
                    n+=1
                    #pad the image to avoid out of bound errors when searching for non-feature pixels on the border pixels
                    temp = np.pad(img, n, 'constant', constant_values=255)
                    #iterates through each pixel in the window of search
                    for r in range(row, row+2*n+1):
                        for c in range(col, col+2*n+1):
                            #checks for a non-feature pixel
                            if(temp[r][c] == 0):
                                #calculates the distance using the distance formula
                                temp_distance = m.sqrt((row-r+n)**2 + (col-c+n)**2) 
                                #checks if the current calculated distance is less than the previous distance
                                #this finds the minimum distance from the feature pixel to the non-feature pixel.
                                if temp_distance < distImg[row][col]:
                                    #updates the distance map with the calculates distance 
                                    distImg[row][col] = round(temp_distance)
                                    #non-feature element is found
                                    find_element = False
                                else:
                                    find_element = False
    #returns the distance map                                
    return distImg.astype(int)
