#!/usr/bin/env python3

# Module for performing clustering, classification etc. for the ColourApp
from scipy import misc
from scipy.cluster.vq import kmeans, kmeans2, whiten
import numpy as np

# Takes a ndarray and a k value as paramter.
def cluster(im, k=0):

    # To show the picture sent to the function to verify that there actually is an image.
    #import matplotlib.pyplot as plt
    #plt.imshow(im)
    #plt.show()

    # Reshapes the image to a RGB * (width*height) matrix.
    dimensions = im.shape
    picReshape = im.reshape((dimensions[0]*dimensions[1], dimensions[2]))

    # Kmeans dos not support datatypes other than Float or Double, and for
    # this reason it must be changed. Nobody likes errors :)
    pictureArr = picReshape.astype(float)

    # For future develompent implement whiten for better clustering.
    # whitened = whiten(pictureArr)

    # Kmeans clustering
    kArr, label = kmeans2(pictureArr, k)

    # Reshapes the label list back to the size of the origial image matrix
    centroidMatrix = label.reshape((dimensions[0], dimensions[1]))

    return centroidMatrix,kArr

cluster(misc.face(), 4)
