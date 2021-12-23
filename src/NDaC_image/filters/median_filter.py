################################################################################
#11/07/2021                                                                    #
################################################################################
# Colored image shape: (num_rows, num_pixels_per_row, RGB == const 3)          #
# Grayscale image shape: (num_rows, num_pixels_per_row)                        #
# Colored image:                                                               #
#   numpy.array([ [[0, 255, 0], [RGB]], [[RGB], [RGB]], [[RGB], [RGB]] ])      #
# Grayscale image:                                                             #
#   numpy.array([ [0, 1, 2...], [intensities], [intensities] ])                #
################################################################################
import numpy as np

# Median filter
#
# Input arguments:
# img = thresholded grayscaled image
# n = kernel size (odd integer)
def median_filter(img, n):

    # Check if n is an odd integer smaller than the size of the image.
    if (n % 2) != 1:
        raise ValueError("n must be an odd integer")
    if n >= img.shape[0] or n >= img.shape[1]:
        raise ValueError("n must be an integer less than the shape of the image")

    # k = numbers of pixel that is going to be padded to avoid out of bound issue.
    k = int((n - 1) / 2)

    # imgTemp = temporary numpy array that solve the out of bound issue.
    imgTemp = np.zeros(((img.shape[0]+(n-1)),(img.shape[1]+(n-1))),dtype=int)
    imgTemp[k:(imgTemp.shape[0]-k),k:(imgTemp.shape[1]-k)] = img

    # median_img = a new numpy array that is going to keep the median value.
    median_img = np.copy(img)
    median_img = find_median(median_img, imgTemp, n)

    return median_img

# The function that finds the median of in each kernal.
#
# Input arguements:
# median_img = array that will be returned
# img = original image with padded values at the boundaries
# n = kernel size
def find_median(median_img, img, n):

    # the value that helps define the kernel size in loops
    k = int((n - 1) / 2)
    for r in range(k, img.shape[0] - k):
        for c in range(k, img.shape[1] - k):
            temp = (img[(r-k):(r+k+1),(c-k):(c+k+1)])

            # find median value
            median = np.median(temp)
            median_img[r-k][c-k] = median

    return median_img
