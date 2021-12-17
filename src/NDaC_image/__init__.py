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
# Added: 9/20/2021 - Tikhon Pachin
from .Image import *
from .otsu import *
from .filters import *
from .general import *
from .watershed import *