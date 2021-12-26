# edge detection
import numpy as np 
import math as m

#This function takes an image array and performs sobel edge
# detection using a 3x3 kernal filter
def detect_edge(img):
    imgTemp = np.pad(img, pad_width=1, mode='constant',constant_values=0)
    #in the x direction
    x_array = np.zeros((len(img), len(img[0])))
    #iterates through each row and column(except the borders)
    for row in range(1, len(imgTemp)-1):
        for col in range(1, len(imgTemp[row])-1):
            #creates an array with the surrounding pixels and modifys them bases on the kernel            
            values = [[(imgTemp[row - 1][col - 1]*-1), (0), (imgTemp[row - 1][col + 1])], 
                     [(imgTemp[row][col - 1]*-2), (0), (imgTemp[row][col + 1]*2)], 
                     [(imgTemp[row + 1][col - 1]*-1), (0), (imgTemp[row + 1][col + 1])]]
            #adds up all the values from the modified surrounding pixels
            sumVal = np.sum(values)
            x_array[row-1][col-1] = sumVal/3 #divide by 3 becasue each pixel has multiple values in it

    #in the y direction
    y_array = np.zeros((len(img), len(img[0])))
    #iterates through each row and column(except the borders)
    for row in range(1, len(imgTemp) -1):
        for col in range(1, len(imgTemp[row])-1):
            #creates an array with the surrounding pixels and modifys them bases on the kernel            
            values = [[(imgTemp[row - 1][col - 1]*-1), (imgTemp[row - 1][col]*-2), (imgTemp[row - 1][col + 1]*-1)], 
                     [(0), (0), (0)], 
                     [(imgTemp[row + 1][col - 1]), (imgTemp[row + 1][col]*2), (imgTemp[row + 1][col + 1])]]
            #adds up all the values from the modified surrounding pixels
            sumVal = np.sum(values)
            y_array[row-1][col-1] = sumVal/3 #divide by 3 becasue each pixel has multiple values in it

    #combining the x and y direction 
    edgeImg = np.zeros((len(img), len(img[0])))
    #iterates through each row and column (except the borders)
    for row in range(0, len(img)):
        for col in range(0, len(img[row])):
            #adding the x and y direction values for each value 
            #the square root of the x direction squared plus the y direction squared

            edgeImg[row][col] = m.sqrt((x_array[row][col])**2 + (y_array[row][col])**2)

    np.place(edgeImg, edgeImg > 0, 255)

    return edgeImg
