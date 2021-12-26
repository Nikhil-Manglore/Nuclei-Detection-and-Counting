## Added 09/21/2021
import numpy as np
from PIL import Image 

## imageViewer: Function that takes in an array and show it as a grayscale image.
## img: A list or a numpy array with shape greater than (1,1). 

def image_viewer(img):
    if (np.shape(img)[0] == 0) or (np.shape(img)[1] == 0):
        raise ValueError("Shape of array has to be greater or equal to (1,1)")

    img = Image.fromarray(img.astype(np.uint8))
    img.show()
    return
