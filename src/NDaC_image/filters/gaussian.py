################################################################################
# Grayscale image shape: (num_rows, num_pixels_per_row)                        #
# Grayscale image:                                                             #
#   numpy.array([ [0, 1, 2...], [intensities], [intensities] ])                #
################################################################################

# Importing necessary tools for the further operations.
import numpy as np
import math

# Gaussian blurring on the preprocessed image (otsu). 
# Technique: for each pixel - combined weighted values of surrounding pixels by
# the Gaussian distribution.
# img - image to be processed, n - kernel size
def get_gaussian_blurred_image(img, n):
    # Check if the input image is of correct shape. Processing wrong shape
    # may cause runtime errors.
    if len(img.shape) != 2:
        raise ValueError("Input array must be of shape (row, pixels per row)")

    # Check if the kernel size is correct.
    if n % 2 == 0 | n <= 1:
        raise ValueError("Kernel size must be an odd number greater than 1.")

    # Copy the image to a new variable. This variable will be used to store
    # the new image. The old image will be used to calculate the new pixel
    # values that will be stored in the new image variable. This operation must
    # be a copy, since simple assignment of the array to another variable will
    # use the same memory and updating the new image will also update old image.
    new_img = np.copy(img)
    pad_size = round((n - 1) / 2)
    img = np.pad(img, [(pad_size, pad_size), (pad_size, pad_size)],
                     mode="constant", constant_values=0)

    # Parse through the image.
    new_img = parse_image_gaussian(new_img, img, n)
    
    return new_img

# Parse through the image applying the gaussian structuring element.
def parse_image_gaussian(new_img, img, n):
    # Calculate the weights in the gaussian structuring element.
    gaussian_sel = calculate_gaussian_sel(n)

    for r in range(0, new_img.shape[0], 1):
        for p in range(0, new_img.shape[1], 1):
            # Calculate the weighted values of the image within the kernel size.
            values = img[r:r + n, p:p + n] * gaussian_sel

            # Convert the values to add up to 255 scale to correctly adjust the 
            # final value to the maximum intensity withing the image (255).
            multiplier = 1 / np.sum(gaussian_sel)
            values = multiplier * values

            # Sum all the values within the kernel to get the final value of the
            # center pixel.
            new_img[r][p] = np.sum(values)

    print(gaussian_sel)
    return new_img

# Function to output the weights of each value within the kernel.
def calculate_gaussian_sel(n):
    # Instantiate the structuring element by creating the n size kernel of 0s.
    gaussian_sel = np.zeros((n, n))

    # Calculate the pad size to process the edges of the image.
    pad_size = round((n - 1) / 2)

    # Get the variance for the Gaussian equation.
    variance = get_variance_gaussian(n, pad_size)

    # For each value in the kernel calculate its weight using the 2D Gaussian
    # equation.
    for i in range(-pad_size, pad_size + 1, 1):
        for j in range(-pad_size, pad_size + 1, 1):
            gaussian_sel[i + pad_size][j + pad_size] = (1 / (2 * math.pi * variance * variance)) * math.exp(-(i ** 2 + j ** 2) / (2 * variance * variance))

    return gaussian_sel

# Get the variance withing the kernel.
def get_variance_gaussian(n, pad_size):
    mean = 0
    variance = 0

    for i in range(-pad_size, pad_size + 1, 1):
        variance += ((i - mean) ** 2) / n

    return variance
