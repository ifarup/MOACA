#!/usr/bin/env python3

# Module for performing clustering, classification etc. for the ColourApp
from scipy import misc
from scipy.cluster.vq import whiten

from sklearn import cluster as clstr
from sklearn.cluster import AffinityPropagation
from sklearn import metrics

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

    numb_of_pxl = dimensions[0] * dimensions[1]

    im.reshape((numb_of_pxl, -1))

    # The image is Int which Kmeans does not support (only Float and Double), and for
    # this reason it must be changed.
    pictureMatrix = picReshape.astype(float)

    # Used for better results of the clustering.
    whitened = whiten(pictureMatrix)

    # Calculates the standard deviation. Used for the inverse whiten operation on the
    # centroid array returned by kmeans. This is needed to calculate the inverse operation
    # of whiten. Whiten basically returns pictureMatrix devided by its standard deviation.
    # https://github.com/scipy/scipy/blob/master/scipy/cluster/vq.py
    stdDev = np.std(pictureMatrix, axis=0)
    zeroStdMask = stdDev == 0
    if zeroStdMask.any():
        # For each value having a standard deviation of zero.
        stdDev[zeroStdMask] = 1.0

    # if k=0 we need to estimate a good K(KK)

        # Kmeans clustering on whiten data.
        # if k=0 we need to estimate a good K(KK)
#    if (k == 0):

#        s_scores = np.ones(10)
#        s_scores[0] = -1
#        s_scores[1] = -1
#        for i in range(2, 10):
            #WHITEND 3(N*M) originale datapunkter
            #n_samples, number of centroids
            #label, 3xK matrise

            kArr, label = kmeans2(im, i)
            s_scores[i] = metrics.silhouette_score(im, label)
            print(i, s_scores[i])
    else:
        kArr, label = kmeans2(whitened, k)

    #finds the best K(closes to 1)
#    k_val = np.amax(s_scores)
#    k = np.argmax(s_scores)
#    print(19 * '*')
#    print('|',k, k_val,'|')
#    print(19 * '*')

    # Clusters the images whiten data and recreates the actual centroid values.
    kmeansData = clstr.KMeans(k).fit(whitened)
    kArr = (kmeansData.cluster_centers_ * stdDev)

    # Reshapes the label list back to the size of the origial image matrix,
    centroidMatrix = np.array(kmeansData.labels_).reshape((dimensions[0], dimensions[1]))

    # Returns a centroidmatrix representing the image with clustervalues instead of actual colors.
    return centroidMatrix, kArr

#cluster(misc.face(), 4)
#cluster(misc.imread("images/asdfghjk.png"), 4)
