# Importing necessary tools for the further operations.
import numpy as np

# Check if the input image is in correct shape and if the image has already been
# thresholded. 
# 
# Variables:
# img = array that stores the image
def image_check(img):
    if len(img.shape) != 2:
        raise ValueError("Input array must be of shape (row, pixels per row)")
    '''else:
        boolean_map_0 = img == 0
        boolean_map_255 = img == 255
        num_of_0 = boolean_map_0.sum()
        num_of_255 = boolean_map_255.sum()
        if (num_of_0 + num_of_255) != (img.shape[0] * img.shape[1]):
            raise ValueError("The image must only contain 0 and 255 values.")'''
    
    return

# Dilation filter with shape nxn. Convert each pixel to the maximum value 
# in the filter window. Maxmium value is find by comparing the all the values except 
# the the middle pixel using a n by n window 
#
# Variable:
# img = the array that stores the thresholded grayscale image
# n = desired shape of the filtering window (nxn). n must be a odd number
def get_dilated_image(img,n):
    # Check if the image is in right shape and has either 0 or 255 grayscale 
    # values pixels
    image_check(img)

    # Check if n is an odd integer smaller than the size of the image.
    if (n % 2) != 1:
        raise ValueError("n must be an odd integer")
    if n >= img.shape[0] or n >= img.shape[1]:
        raise ValueError("n must be a integer less than the shape of the image")

    # Copy the image to a new variable. This will be used to store the maximum pixel
    # value in the filtering window.
    new_img = np.copy(img)
    
    # Creating an nested array that has two more rows at the beginning and the end
    # of the array (i.e. imgTemp = [new, new, old, ..., old, new, new]). In each imgTemp[] array
    # there will be two more elements at the beginning and the end of the array 
    # (e.g. imgTemp[10[new, new, old, ..., old, new, new]]) The array is created to avoid out-of-bound 
    # issue when parsing through each pixel in the dilation process. The temporary element values in the 
    # array is set to 0. This will not change the result because dilation is looking for the maximum
    # value, which is 255, in a thresholded grayscale image.
    extra = int((n - 1) / 2) # the extra rows / elements needed add to avoid out-of-bound
    imgTemp = np.zeros(((img.shape[0]+(n-1)),(img.shape[1]+(n-1))),dtype=int)
    imgTemp[extra:(imgTemp.shape[0]-extra),extra:(imgTemp.shape[1]-extra)] = img
    image_check(imgTemp)

    # Parse every pixel through a n by n filtering window for dilataion process.
    new_img = dilation(new_img, imgTemp,n)
    return new_img

# A nxn filtering window for dilation process. 
#
# Variables:
# new_img = the array that will store the maximum value of the in each filtering window in 
#           the dilation process.
# img = the array that stores the original thresholded grayscale image. This should be an array
#       that has been created to avoid out of bound issue.
# n = the shape of the filtering window - n x n, where n is a odd integer
def dilation(new_img, img,n):
    k = int((n - 1) / 2) # the value that help avoid out-of-bound issue
    for r in range(k, img.shape[0] - k): # Avoid the first k and the last k rows
        for c in range(k, img.shape[1] - k): # Avoid the first k and the last k elements
            temp = (img[(r-k):(r+k+1),(c-k):(c+k+1)]) # temporary array as a filtering window

            # placing the maximum value for the pixel 
            maxVal = np.max(temp) 
            new_img[r-k][c-k] = maxVal

    return new_img
