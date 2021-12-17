#Aubrey Gatewood 9/20/21
#image uploader takes string name of image to be processed
#searches in SourceImages for the image
#and returns it as a numpy array
from PIL import Image
import numpy as np
import os
import os.path
import shutil
#supposed to make it so that it just opens from a folder in general and people put what they want in there. 

# Switched String_name_of_file to filename. The original name was too verbose.
# Switch was made for clarity.
# Tikhon Pachin - 10/12/2021
def image_uploader(filename):
    RESOURCES_PATH = os.path.dirname(os.path.abspath(__file__))
    #gets current directory
    o = RESOURCES_PATH + "/resources/"
    # Switched SourceImages to resources - standard nomenclature.
    # Tikhon Pachin - 10/12/2021

    if os.path.exists(o + filename):
        file = o + filename
        with Image.open(file) as im:
            imageArray = np.array(im)
            #opens image as a numpy array
            return imageArray
    else:
        # Switched print statement to Error raise. This stops the execution of 
        # the code, so that we don't waste computational power and time.
        # Tikhon Pachin - 10/12/2021
        raise ValueError('could not find ' + filename + ' in the folder SourceImages. Please add it to the folder to process it')