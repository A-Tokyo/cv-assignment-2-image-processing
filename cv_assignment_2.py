import cv2
import numpy as np
import time


# Define helper functions
def getHistogram(image):
    histogram = np.full((256), 0)
    for i in range (len(image)):
            for j in range (len(image[i])):
                value = image[i][j]
                histogram[value] += 1
    return histogram

def getCommHistogram(image):
    commHistogram = np.full((256), 0)
    histogram = getHistogram(image)
    commHistogram[0] = histogram[0]
    for i in range (1, 256):
        commHistogram[i] = histogram[i] + commHistogram[i - 1]
    return commHistogram

def printHistAndCommHist(inputPath, outputPath):
    # init basic vars
    image = cv2.imread(inputPath,0)
    imageHistogram = getHistogram(image)
    imageCommHistogram = getCommHistogram(image)

    # create new image
    imageNew = np.zeros((512,1024,3), np.uint8)
    maxHisHeightNorm = int(max(imageHistogram) / 512)
    maxCommHisHeightNorm = int(max(imageCommHistogram) / 512)

    for i,j in zip(range(0, 1024, 4), range(0, 256)):
        hisNormHeight = int(imageHistogram[j] / maxHisHeightNorm)
        comHisNormHeight = int(imageCommHistogram[j] / maxCommHisHeightNorm)
        cv2.line(imageNew, (i, 511), (i, 512 - comHisNormHeight), (140, 140, 140), 2)
        cv2.line(imageNew, (i, 511), (i, 512 - hisNormHeight), (80, 80, 80), 1)

    cv2.imwrite(outputPath, imageNew)


# Define question functions and their helpers
def histogramCalc():
    printHistAndCommHist("inputs/cameraman.png", "outputs/cameramanNewHisAndCommHis.png")
    printHistAndCommHist("inputs/bat.png", "outputs/batNewHisAndCommHis.png")
    printHistAndCommHist("inputs/fog.png", "outputs/fogNewHisAndCommHis.png")
    printHistAndCommHist("inputs/fognoise.png", "outputs/fognoiseNewHisAndCommHis.png")

def meanVsGaus():
    image = cv2.imread("inputs/cameraman.png",0)

    imageFilteredMean = cv2.blur(image,(5,5))
    cv2.imwrite("outputs/cameramanNewFilteredMean.png", imageFilteredMean)
    printHistAndCommHist("outputs/cameramanNewFilteredMean.png", "outputs/cameramanNewFilteredMeanHisAndCommHis.png")

    imageFilteredGaus = cv2.GaussianBlur(image,(5,5),0)
    cv2.imwrite("outputs/cameramanNewFilteredGaus.png", imageFilteredGaus)
    printHistAndCommHist("outputs/cameramanNewFilteredGaus.png", "outputs/cameramanNewFilteredGausHisAndCommHis.png")

def selectiveMedianFilter():
    image = cv2.imread("inputs/fognoise.png",0)
    newImage = np.zeros((len(image),len(image[0]),3), np.uint8)
    timeBeforeApplyingFilter = time.clock()

    for i in range (len(image)):
        for j in range (len(image[i])):
            value = image[i][j]
            pixelValues = []

            for fI in range (-2, 3):
                for fJ in range (-2, 3):
                    try:
                        pixelValues.append(image[i+fI][j+fJ])
                    except IndexError:
                        pass
            pixelValues.sort()
            newValue = pixelValues[int((len(pixelValues)-1)/2)]
            newImage[i][j] = newValue

    timeAfterApplyingFilter = time.clock()
    runtimeApplyingFilter = timeAfterApplyingFilter - timeBeforeApplyingFilter
    cv2.imwrite("outputs/fogNoiseNewSelectiveMedianFilterBasic.png", newImage)
    print("Runtime for applying selective median filter: " + str(runtimeApplyingFilter))


def contrastStrecthing():
    image = cv2.imread("inputs/frostfog.png",0)
    newImage = np.zeros((len(image),len(image[0]),3), np.uint8)
    a = 0
    b = 255
    c = min(image.flatten())
    d = max(image.flatten())
    scalingFactor = (b-a)/(d-c);

    for i in range (len(image)):
        for j in range (len(image[i])):
            value = image[i][j]
            newValue = ((value-c)*scalingFactor) + a
            newImage[i][j] = newValue

    cv2.imwrite("outputs/frostfogNewContrastStretching.png", newImage)
    printHistAndCommHist("outputs/frostfogNewContrastStretching.png", "outputs/frostfogNewContrastStretchingHisAndCommHis.png")

def histogramEqualization():
    image = cv2.imread("inputs/frostfog.png",0)
    newImage = np.zeros((len(image),len(image[0]),3), np.uint8)
    commHist = getCommHistogram(image)
    pixelCount = len(image)*len(image[0])

    for i in range (len(image)):
        for j in range (len(image[i])):
            value = image[i][j]
            f = commHist[value]
            newValue = f*(255/pixelCount)
            newImage[i][j] = newValue

    cv2.imwrite("outputs/frostfogNewHistogramEqualization.png", newImage)
    printHistAndCommHist("outputs/frostfogNewHistogramEqualization.png", "outputs/frostfogNewHistogramEqualizationHisAndCommHis.png")

def contrastStretchingAndHistogramVisualization():
    printHistAndCommHist("inputs/frostfog.png", "outputs/frostfogNewHisAndCommHis.png")
    contrastStrecthing()
    histogramEqualization()

def mystery():
    image = cv2.imread("inputs/tree.png",0)
    modifiedImage = cv2.imread("inputs/treeM.png",0)
    newImage = np.zeros((len(image),len(image[0]),3), np.uint8)


    for i in range (len(image)):
        for j in range (len(image[i])):
            value = modifiedImage[i][j] - image[i][j]
            newImage[i][j] = value

    cv2.imwrite("outputs/mysteryNew.png", newImage)

### END OF LOGIC

# Exec functions
# Q1
histogramCalc()

# Q2
meanVsGaus()

# Q3
selectiveMedianFilter()

# Q4
contrastStretchingAndHistogramVisualization()

# Q5 Bonus
mystery()

# END OF ASSIGNMENT