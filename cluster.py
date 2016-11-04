#!/usr/bin/env python3

# Module for performing clustering, classification etc. for the ColourApp
from scipy import misc
from scipy.cluster.vq import kmeans2, whiten
import numpy as np

# Takes a ndarray and a k value as paramter.
def cluster(im, k=0):
    # Reads a image from a directory or use the generic "face"
    # face = misc.face()
    # face = misc.imread("images/asdfghjk.png")

    # Np array of length*width high and RGB wide, all zero
    dimensions = im.shape
    pictureArr = np.zeros(shape=(dimensions[0] * dimensions[1], dimensions[2]))

    # Iterates over the picture and stores the values in the numpy array.
    workaround = 0
    dim = [0,1,2]
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            pictureArr[workaround] = [im[i][j][dim[0]], im[i][j][dim[1]], im[i][j][dim[2]]]
            workaround += 1

    # For future develompent implement whiten for better clustering.
    # whitened = whiten(pictureArr)

    # Kmeans clustering
    kArr, label = kmeans2(pictureArr, k)

    # Creates a width*height array reprecenting the image which is filled with corresponding centroid value
    workaround = 0
    centroidPicArr = np.zeros(shape=(dimensions[0], dimensions[1]))
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            centroidPicArr[i][j] = label[workaround]
            workaround += 1

    return centroidPicArr,kArr

#cluster(misc.imread("images/asdfghjk.png"), 3)
