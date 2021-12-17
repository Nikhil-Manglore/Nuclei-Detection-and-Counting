################################################################################
# File collaboration:                                                          #
#   Yu-Hsuan Lin - 11/15/2021                                                  #
################################################################################
# Colored image shape: (num_rows, num_pixels_per_row, RGB == const 3)          #
# Grayscale image shape: (num_rows, num_pixels_per_row)                        #
# Colored image:                                                               #
#   numpy.array([ [[0, 255, 0], [RGB]], [[RGB], [RGB]], [[RGB], [RGB]] ])      #
# Grayscale image:                                                             #
#   numpy.array([ [0, 1, 2...], [intensities], [intensities] ])                #
################################################################################

import numpy as np

def get_ceiling(topographicalMap, cell_minima, n):
    img = minimaMap(topographicalMap, cell_minima)

    extra = 1 # the extra rows / elements needed add to avoid out-of-bound
    regionTemp = np.zeros(((img.shape[0]+2),(img.shape[1]+2)),dtype=int)
    regionTemp[extra:(regionTemp.shape[0]-extra),extra:(regionTemp.shape[1]-extra)] = img
    region, numMin = findRegion(regionTemp)

    extra = int((n-1)/2)
    hieghtTemp = np.zeros(((img.shape[0]+(n-1)),(img.shape[1]+(n-1))),dtype=int)
    hieghtTemp[extra:(hieghtTemp.shape[0]-extra),extra:(hieghtTemp.shape[1]-extra)] = img

    height = np.copy(img)
    height = findHeight(hieghtTemp, height, region, n)

    ceilingImg = findCeiling(region, height, numMin)

    return ceilingImg

def minimaMap(topographical, minima):
    img = np.copy(topographical)
    for element in minima:
        row = element.r
        pos = element.p
        img[row][pos] = 0

    return img

def findRegion(img):
    count = 0
    minimumCount = 0
    check = 0
    k = 1
    region = np.zeros((img.shape[0]-k,img.shape[1]-k),dtype=int)
    checkRegion = np.zeros((img.shape[0]-k,img.shape[1]-k),dtype=int)
    for r in range(k, img.shape[0] - k):
        for c in range(k, img.shape[1] - k):
            if img[r][c] == 0:
                temp = (region[(r-2*k):(r+1),(c-2*k):(c+1)])
                minimumCount += 1
                
                if np.all((temp == 0)):
                    count += 1
                    region[r-k][c-k] = count
                    checkRegion[r-k][c-k] = 255
                    
                else:
                    region[r-k][c-k] = np.max(temp) # assuming no different regional minima are connected together
                    check += 1

    return region, count


def findHeight(img, height, region, n):
    k = int((n-1) / 2)

    for r in range(k, img.shape[0] - k):
        for c in range(k, img.shape[1] - k):
            if region[r-k][c-k] != 0:
                temp = (img[(r-k):(r+k+1),(c-k):(c+k+1)])
                h = np.max(temp)
                height[r-k][c-k] = h

    return height

def findCeiling(region, height, numMin):
    # ceiling = np.copy(height)
    ceiling = np.zeros((region.shape[0],region.shape[1]),dtype=int)

    for i in range(1, 1+numMin):
        tempHeight = []
        position = []
        for r in range(region.shape[0]):
            for c in range(region.shape[1]):
                if region[r][c] == i:
                    tempHeight.append(height[r][c])
                    position.append([r,c])
        maxHeight = np.max(tempHeight)
        
        for pos in position:
            ceiling[pos[0]][pos[1]] = maxHeight
    
    return ceiling