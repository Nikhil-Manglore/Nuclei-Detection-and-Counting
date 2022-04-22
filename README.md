# Nuclei-Detection-And-Counting 
--------------------------------------------------------------------------------------------------------------------------------------------
During my Fall 2021 semester I was an undergraduate student researcher under Purdue University's Vertically Integrated Projects. My research was based around image processing techniques and implementations. This program utilizes mathematical morphology, pre-processing methods such as gaussian nlurring, and the watershed segmentation in order to segment heavilyg clustered nuclei within images of cells.
--------------------------------------------------------------------------------------------------------------------------------------------

Abstract: <br/>
Nuclei segmentation on microscopy images has been a topic of interest for over 10 years. There are multiple
different algorithms that have been developed to target the issue. This project focuses specifically on
Watershed segmentation with some preliminary image processing to segment and count nuclei. Nuclei
segmentation is an important step in cancer detection and prediction.
Watershed segmentation is a method that analyzes an image as if it is a topographical map. Controlled
flooding of the image produces the edges between basins, which are the borders of the cells. To get the
topographical image, the preprocessing detects the areas of interest on the image and then the algorithm
applies a distance transform on the image. Three different transforms are available and they are Chessboard,
City-block and Euclidean transforms.
Image preprocessing includes important filters such as image dilation, erosion, opening, closing, blurring and
Otsu’s thresholding. These filters are heavily employed for image noise reduction. Without this step the
topographical image of the cells would be inaccurate.
The project was split into proof of concept, algorithm altering and noise reduction. Proof of concept utilized
some preexistent tools to segment the nuclei. Algorithm altering step implemented and adjusted the algorithm
from scratch. <br/>
The output of nuclei segmentation is an image that shows the borders between the cells and a number that
corresponds to the number of cells in the image. This output is a preliminary processing method for further
research that may be conducted on such images.
<br/>
<br/>
Mentors: <br/>
Edward Delp, College of Engineering, Electrical & Computer Engineering <br/>
Carla Zoltowski, Purdue University
