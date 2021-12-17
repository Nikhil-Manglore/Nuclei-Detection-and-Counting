#edge blurring/ noise smoothing
import numpy as np
import math as m
from PIL import Image

#This function takes a grayscale image and applys a blur to it in order to get rid of some noise
#To do this, it iterates through each pixel, applies factors to it and its surrounding pixels a 3x3 
#kernel, adds it up, and applies the new value to a blank array
#the edges are left black for now
#input MUST be black and white
def blur_img(bw):
    newImg_array = np.zeros((len(bw), len(bw[0])))
    #iterates through eachrow (except the borders)
    for row in range(1, len(bw) -1):
        #iterates through each column (except the borders)
        for col in range(1, len(bw[row])-1):
            #creates an array with the surrounding pixels and modifys them bases on the kernel
            values = [[(bw[row - 1][col - 1]/16), (bw[row - 1][col]/8), (bw[row - 1][col + 1]/16)], 
                    [(bw[row][col - 1]/8), (bw[row][col]/4), (bw[row][col + 1]/8)], 
                    [(bw[row + 1][col - 1]/16), (bw[row  + 1][col]/8), (bw[row + 1][col + 1]/16)]]
            #adds up all the values from the modified surrounding pixels
            sumVal = np.sum(values)
            newImg_array[row][col] = sumVal/3 #divide by 3 becasue each pixel has multiple values of the grayscale in it

    #returns array of blurred image
    return newImg_array

def blurImage(img, n):
    k = int((int(n)-1)/2)
    padImg = np.pad(img, pad_width=k, mode='constant',constant_values=0)
    newImg = np.empty((len(img), len(img[0])))
    for row in range(k, len(padImg)-k):
        for col in range(k, len(padImg)-k):
            window = getImageWindow(padImg, n, row, col)
            filter = createFilter(n)
            sum = 0
            for r in range(0, n):
                for c in range(0, n):
                    sum += (window[r][c]*filter[r][c])
            newImg[row-k][col-k] = sum/256/3
    return newImg

def getImageWindow(img, n, r, c):
    window = np.empty((n,n))
    r-=1
    c-=1
    colInImg = c
    for row in range(0,n):
        for col in range(0,n):
            window[row][col] = img[r][c][0]
            c+=1
        r+=1
        c=colInImg
    return window

def createFilter(n):
    kernel = np.empty((n,n))
    corner = 2**(7-n)
    k = m.floor(n/2)

    rowVal = corner
    value = corner

    for row in range(len(kernel)):
        for col in range(len(kernel[row])):
            if col < k:
                kernel[row][col] = value
                value *= 2
            else:
                kernel[row][col] = value
                value /= 2
        if row < k:
            rowVal *= 2
        else:
            rowVal /= 2
        value = rowVal
    return kernel
