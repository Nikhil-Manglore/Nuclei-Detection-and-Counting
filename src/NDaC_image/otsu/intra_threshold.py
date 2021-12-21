################################################################################
# Colored image shape: (num_rows, num_pixels_per_row, RGB == const 3)          #
# Grayscale image shape: (num_rows, num_pixels_per_row)                        #
# Colored image:                                                               #
#   numpy.array([ [[0, 255, 0], [RGB]], [[RGB], [RGB]], [[RGB], [RGB]] ])      #
# Grayscale image:                                                             #
#   numpy.array([ [0, 1, 2...], [intensities], [intensities] ])                #
################################################################################

# Importing necessary tools for the further operations. Tikhon Pachin - 9/6/2021
import numpy as np

# Threshold detector through itra-cluster variance maximization.
def get_threshold_intra(image):
    # Check if the input image is of correct shape. Processing wrong shape
    # may cause runtime errors. This is important because data must be in
    # grayscale. All other color palettes must raise an error.
    # If the color palette is correct then we need to convert the image from
    # the coding convention into math convention. Otsu's threshold is calculated
    # based on the 1-256 levels of grayscale, rather than 0-255. 
    if len(image.shape) != 2:
        raise ValueError("Input array must be of shape (row, pixels per row)")
    else:
        image = image + 1

    # For the maximization problem we need to find the value for the threshold
    # that will maximize the variance between two clusters. The variance will
    # always be positive and, thus, the minimum variance is 0, which will be
    # the initial value for comparison. Initial threshold will also be 0 since
    # we need to parse through all values in the range of 1-256 and 0 would mean
    # that the threshold has not yet been detected. 
    variance = 0
    threshold = 0

    # Now, for each threshold we need to find the variance between clusters.
    # The following is the equation for intra-cluster variance:
    #   - var^2 = prob0 * prob1 * (mean1 - mean0)^2
    # To find the variance for a set threshold we must calculate each clusters'
    # probability and mean.
    for t in range(1, 257, 1):
        prob0 = get_cluster_probability(t, 0, image)
        prob1 = get_cluster_probability(t, 1, image)
        mean0 = get_cluster_mean(t, 0, image, prob0)
        mean1 = get_cluster_mean(t, 1, image, prob1)
        computed_variance = get_intra_variance(prob0, prob1, mean0, mean1)

        # Maximization task: if the variance is larger than the previous
        # variance then we discard previous variance and update it to the new
        # variance and assign the new threshold. 
        if computed_variance > variance:
            threshold = t
            variance = computed_variance
    
    # Remember that Otsu's method is operated on the 1-256 scale and the
    # threshold is also determined on that scale. It must be converted to
    # 0-255 scalse by subtracting 1.
    return threshold - 1

# Intra-cluster variance detector. 
def get_intra_variance(prob0, prob1, mean0, mean1):
    # Intra-cluster variance formula:
    #   var^2 = probab0 * probab1 * (mean1 - mean0)^2
    return prob0 * prob1 * ((mean1 - mean0) ** 2)

# Cluster mean detector. 
def get_cluster_mean(t, cluster, image, probab):
    # If the probability of the cluster is 0 then the returned mean should also
    # be zero, since it may not be appropriately calculated.
    if probab == 0:
        return 0

    # Initial values are the total cluster level mean, which is zero and the
    # total number of pixels in the image. 
    cluster_level_mean = 0
    total_pixels = image.shape[0] * image.shape[1]

    # Depending on the cluster number the following is the equstion for the
    # cluster level mean:
    #   cluster_level_mean = sum(level * level_probability)
    #   level_probability = level_pixels / total_pixels
    if cluster == 0:
        for i in range(1, t + 1, 1):
            level_pixels = (image == i).sum()
            level_mean = level_pixels * i / total_pixels
            cluster_level_mean += level_mean
    elif cluster == 1:
        for i in range(t + 1, 257, 1):
            level_pixels = (image == i).sum()
            level_mean = level_pixels * i / total_pixels
            cluster_level_mean += level_mean

    # The total mean of a cluster is the following:
    #   cluster_mean = cluster_level_mean / cluster_probability
    # This must be rounded. 
    return round(cluster_level_mean / probab, 3)


# Cluster probability detector. 
def get_cluster_probability(t, cluster, image):
    # Initial values are the total number of pixels in the image and the
    # threshold boolean map of the image.
    total_pixels = image.shape[0] * image.shape[1]
    bool_map = get_threshold_boolean_map(image, t)

    # Sum the number of pixels that are either lower or higher than the
    # threshold based on the cluster at which we are currently looking.
    # False corresponds to values that are less than or equal to the threshold.
    # True corresponds to values that are bigger than the threshold.
    if cluster == 0:
        cluster_pixels = (bool_map == False).sum()
    elif cluster == 1:
        cluster_pixels = (bool_map == True).sum()

    # The total probability of a cluster is the number of pixels in the
    # cluster divided by the total number of pixels in the image.
    return round(cluster_pixels / total_pixels, 3)

# Image to threshold based boolean map converter. 
def get_threshold_boolean_map(image, t):
    return image > t
