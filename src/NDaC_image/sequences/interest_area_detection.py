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

# Area of interest detector. 
# Note: img is ImageClass object.
def detect_area_of_interest(img, n_blur, n_dilation, v_exposure):
    # Remove the noise on the image that prevents general detection of the area
    # of interest. 
    blurred_image = img.get_gaussian_blur_image(np.copy(img.gray_img), n_blur)

    # Threshold the image after the noise removal.
    blur_otsu_threshold = img.get_otsu_threshold(np.copy(blurred_image))
    blur_otsu_img = img.otsu_parser(np.copy(blurred_image), blur_otsu_threshold)

    # Dilated the thresholded image to cover surplus ground to make sure that
    # nothing important is missing from the area of interest.
    dilated_image = img.get_dilated_image(np.copy(blur_otsu_img), n_dilation)

    # Increase the intensity of each pixel in the areas of interest, so that
    # Otsu's thresholding does pick up on the dark foregrounds.
    exposure_mask = np.copy(dilated_image)
    np.place(exposure_mask, exposure_mask == 255, v_exposure)
    masked_img = np.copy(img.gray_img) + exposure_mask

    # Threshold the image to get the areas of interest.
    exp_otsu_threshold = img.get_otsu_threshold(np.copy(masked_img))
    area_of_interest = img.otsu_parser(np.copy(masked_img), exp_otsu_threshold)
    
    return area_of_interest
