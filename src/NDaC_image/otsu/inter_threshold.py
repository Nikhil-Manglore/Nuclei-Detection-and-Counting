import numpy as np

# Get the probabilities of each grayscale value from 0 to 255
#
# variables:
#   arr_hist = array of numbers of pixel of each grayscale value from 0 to 255
#   arrGray = array that stores the grayscale value of the image
def getProb(arr_hist, arrGray):
    p = [] # array that stores the probabilites of each grayscale value
    for i in range(256):
        p.append(arr_hist[i] / np.size(arrGray))
    return p

# Get the sum of probabiliteis that are under and greater or equal to the theshold value
#
# variables:
# p = array that stores the probabiliteis of each grayscale value
# k = threshold value
def getProb_inter(p,k):
    p1 = 0 # the probabilities that is below the theshold value
    p2 = 0 # the probabilities that is greater or equal to the theshold value

    for i in range(256):
        if i <= (k-1):
            p1 += p[i]
        else: 
            p2 += p[i]
    return p1, p2

# Get the mean values that are below threshold and greater or equal to thoreshold value
#
# variables:
# p = array that stores the probabiliteis of each grayscale value
# p1 = the probabilities that is below the theshold value
# p2 = the probabilities that is greater or equal to the theshold value
# k = threshold value
def getMean_inter(p,p1,p2,k):
    m1 = 0 # mean value below threshold value
    m2 = 0 # mean value greater or equal to threshold value
    temp = [] # array that keeps the values of i*p[i] for further calculations

    for i in range(256):
        temp.append(i * p[i])
    
    for i in range(256):
        if i <= (k-1):
            m1 += temp[i]
        else:
            m2 += temp[i]
        
    if p1 == 0: # if p1 == 0, m1 / p1 will not be available
        m1 = 0
    else:
        m1 = m1 / p1
    if p2 == 0: # if p2 == 0, m2 / p2 will not be available
        m2 = 0
    else:
        m2 = m2 / p2

    return m1, m2

# Get the variance values that are below threshold and greater or equal to the threshold value
#
# variables:
# p = array that stores the probabiliteis of each grayscale value
# p1 = the probabilities that is below the theshold value
# p2 = the probabilities that is greater or equal to the theshold value
# m1 = mean value below threshold
# m2 = mean value greater or equal to threshold value
# k = threshold value
def getVariance_inter(p, p1, p2, m1, m2, k):
    var1 = 0 # variance value below threshold value
    var2 = 0 # variance value greater or equal to threshold value

    for i in range(256):
        if (p1 == 0) or (p2 == 0):
            continue
        if i <= (k-1):
            var1 += ((i - m1) ** 2) * p[i] / p1
        else:
            var2 += ((i - m2) ** 2) * p[i] / p2

    return var1, var2

# Get the intra cluster variance value of threshold k
#
# variables:
# p1 = the probabilities that is below the theshold value
# p2 = the probabilities that is greater or equal to the theshold value
# var1 = variance value below threshold
# var2 = varaince value greater or equal to threshold value
def getIntra_var(p1, p2, var1, var2):
    intraVar = 0 # the intra cluster vairance value of threshold k

    intraVar = p1 * var1 + p2 * var2

    return intraVar


# Get the thredhold value of intra cluster variance
# 
# variables:
#   img = grayscale

# Switched getThreshold_inter to get_threshold_inter - standard nomenclature.
# Tikhon Pachin - 10/12/2021
def get_threshold_inter(img):
    k = 256 # the threshold value, set to 256 because thredhold value is between 0 and 255
    tempVar = 10000 # temporary value that stores the minimum varaince

    # get the histogram array of the grayscale image
    arr_hist = getGrayHist(img)

    # Values needed to calculate the threshold value
    for i in range(256):
        p = getProb(arr_hist,img)
        p1, p2 = getProb_inter(p,i)
        m1, m2 = getMean_inter(p,p1,p2,i)
        var1, var2 = getVariance_inter(p,p1,p2,m1,m2,i)
        intraVar = getIntra_var(p1,p2,var1,var2)

        if (var1 == 0) or (var2 == 0):
            continue
        # Comparison between the inra-cluster variance (intraVar) calculates with the value i and the 
        # tempVar. The smaller variance value gets store in the tempVar because we are finding minimum 
        # in this function. k value with smaller variance will also be stored.
        if intraVar < tempVar:
            tempVar = intraVar
            k = i

    return k

# Get the numbers of pixels in different grayscale values from 0 to 255
#
# Variable:
# arrGray = the array that stores the grayscale value of the image
def getGrayHist(img):
    arrGray = np.array(img)
    arr_flat = arrGray.flatten()
    arr_hist = np.histogram(arr_flat,bins = 256, range=[0,255]) # array of the histogram of the grayscaled array
    arr_hist = arr_hist[0] 
    return arr_hist

# Change all the pixels that are below the threshold value to 0 and the pixels that are greater or equal
# the threshold value to 255.
#
# variables:
#   arrGray = array that stores the grayscale value of the image
#   result = threshold value 
def imageChange(arrGray, result):
    for i in range(len(arrGray)):
        for j in range(len(arrGray[0])):
            if arrGray[i][j] <= result:
                arrGray[i][j] = 0
            else:
                arrGray[i][j] = 255
    return arrGray

# # Testing functions ----------- (uncomment to test) ---------------

# # read and show image
# img = cv2.imread("4.png")
# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# plt.show()

# # conver image to grayscale image
# B, G, Ｒ = img[:,:,0], img[:,:,1], img[:,:,2]
# arrGray = []
# for i in range(len(B)):
#     arrGray.append(0.2126 * R[i] + 0.7125 * G[i] + 0.0722 * B[i])
# plt.imshow(arrGray,cmap="gray")
# plt.show()

# # Use functions
# result = getThreshold_inter(arrGray)
# arrGray = imageChange(arrGray,result)
# plt.imshow(arrGray,cmap="gray")
# plt.show()
