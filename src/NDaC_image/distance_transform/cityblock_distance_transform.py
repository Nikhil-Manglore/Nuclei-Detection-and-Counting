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

# Function of City-Block distance transformation.
#
# Input Argument:
# img = Thresholded grayscaled image.
def cityblock_distance_transform(img):

    # Initialize a numpy array whose value is set to 255 with the shape of the  input image.
    # This array assumes the largest possible distance to non-feature pixel is 255.
    distImg = np.full((img.shape[0],img.shape[1]),255, dtype = int)

    # Call the findDist function and replace each pixel with the minimum distance.
    distImg = findDist(img, distImg)

    return distImg

# Find the distance to non-feature pixel using City-Block distance trasformation.
#
# Input Argument:
# img = Thresholded grayscaled image.
# distImg = Numpy array that stores the largest possible distance.
def findDist(img, distImg):

    # Array with length of img's row
    # Ex: img.shape[0] = 3
    # arrRow = [0, 1, 2]
    arrRow = np.arange(img.shape[0])

    # Array with length of img's column 
    # Ex: img.shape[1] = 5
    # arrRow = [0, 1, 2, 3, 4]
    arrCol = np.arange(img.shape[1])

    # Matrix whose shape is same as img. All the elements in a row have the same value k
    # that represents the k-th row of the matrix.
    # Ex: img.shape = (3,3)
    # matRow = [[0,0,0]
    #           [1,1,1]
    #           [2,2,2]]
    matRow = np.matrix(np.tile(arrRow,(img.shape[1],1))).transpose() 

    # Matrix whose shape is same as img. All the elements in a column have the same value k
    # that represents the k-th row of the matrix.
    # Ex: img.shape = (3,3)
    # matCol = [[0,1,2]
    #           [0,1,2]
    #           [0,1,2]]
    matCol = np.matrix(np.tile(arrCol,(img.shape[0],1)))

    # Look through each pixel in the image.
    for r in range(img.shape[0]):
        for c in range(img.shape[1]):
            
            # If the pixel value is 0, find the distance.
            if (img[r][c] == 0):

                # distance = |i_1 - i_2| + |j_1 - j_2|
                # where (i_1,j_1) = pixel that we are looking for the distance away from 0
                #       (i_2,j_2) = pixel with value 0
                temp = np.abs(matRow - r) + np.abs(matCol - c)

                # Find the minimum distance to non-feature pixel.
                distImg = np.asarray([temp,distImg]).min(0)      
    
    return distImg
