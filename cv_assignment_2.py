import cv2
import numpy as np

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
    cameraman = cv2.imread(inputPath,0)
    cameramanHistogram = getHistogram(cameraman)
    cameramanCommHistogram = getCommHistogram(cameraman)

    # create new image
    cameramanNew = np.zeros((512,1024,3), np.uint8)
    maxHisHeightNorm = int(max(cameramanHistogram) / 512)
    maxCommHisHeightNorm = int(max(cameramanCommHistogram) / 512)

    for i,j in zip(range(0, 1024, 4), range(0, 256)):
        hisNormHeight = int(cameramanHistogram[j] / maxHisHeightNorm)
        comHisNormHeight = int(cameramanCommHistogram[j] / maxCommHisHeightNorm)
        cv2.line(cameramanNew, (i, 511), (i, 512 - comHisNormHeight), (140, 140, 140), 2)
        cv2.line(cameramanNew, (i, 511), (i, 512 - hisNormHeight), (80, 80, 80), 1)

    cv2.imwrite(outputPath, cameramanNew)

def cameraManMean():
    cameraman = cv2.imread("inputs/cameraman.png",0)

    cameramanFilteredMean = cv2.blur(cameraman,(5,5))
    cv2.imwrite("outputs/cameramanNewFilteredMean.png", cameramanFilteredMean)
    printHistAndCommHist("outputs/cameramanNewFilteredMean.png", "outputs/cameramanNewFilteredMeanHisAndCommHis.png")

    cameramanFilteredGaus = cv2.GaussianBlur(cameraman,(5,5),0)
    cv2.imwrite("outputs/cameramanNewFilteredGaus.png", cameramanFilteredGaus)
    printHistAndCommHist("outputs/cameramanNewFilteredGaus.png", "outputs/cameramanNewFilteredGausHisAndCommHis.png")


def mystery():
    originalImage = cv2.imread("inputs/tree.png",0)
    modifiedImage = cv2.imread("inputs/treeM.png",0)
    diffImage = np.zeros((len(originalImage),len(originalImage[0]),3), np.uint8)


    for i in range (len(originalImage)):
        for j in range (len(originalImage[i])):
            value = modifiedImage[i][j] - originalImage[i][j]
            diffImage[i][j] = value

    cv2.imwrite("outputs/mysteryNew.png", diffImage)

# Exec funcs
printHistAndCommHist("inputs/cameraman.png", "outputs/cameramanNewHisAndCommHis.png")
printHistAndCommHist("inputs/bat.png", "outputs/batNewHisAndCommHis.png")
printHistAndCommHist("inputs/fog.png", "outputs/fogNewHisAndCommHis.png")
printHistAndCommHist("inputs/fognoise.png", "outputs/fognoiseNewHisAndCommHis.png")

cameraManMean()

mystery()