#!/usr/bin/env python3

# Module for performing clustering, classification etc. for the ColourApp
from scipy import misc
from scipy.cluster.vq import whiten

from sklearn import cluster as clstr
from sklearn.cluster import AffinityPropagation
from sklearn import metrics

from skimage.transform import resize

import numpy as np

# Takes a ndarray and a k value as paramter.

def cluster(im, k, intervall = False):

    # Resizes the image to a more manageble size for clustering.
    # Timeconsumption for clustering drastically reduses.
    imDim = np.array(im.shape[0:2])
    resizedImage = resize(im, (imDim[:2] / imDim.max() * 100).astype(int))

    # To show the picture sent to the function to verify that there actually is an image.
    #import matplotlib.pyplot as plt    #plt.imshow(im)    #plt.show()

    # Reshapes the resized image to a (width*height)*RGB  matrix.
    dimensions = resizedImage.shape
    picReshape = resizedImage.reshape((dimensions[0] * dimensions[1], dimensions[2]))

    numb_of_pxl = dimensions[0] * dimensions[1]

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

    # if k=0 we need to estimate a good value for K.
    #    finds the best K(closes to 1)

    if (intervall):
        s_scores = np.ones(k)
        s_scores[0] = -1
        s_scores[1] = -1
        for i in range(2, k):
            #WHITEND 3(N*M) originale datapunkter
            #n_samples, number of centroids
            #label, 3xK matrise

            kmeansData = clstr.KMeans(i).fit(whitened)
            s_scores[i] = metrics.silhouette_score(whitened, kmeansData.labels_)
            print(i, s_scores[i])

        # Print scores for testing purposes.
        k_val = np.amax(s_scores)
        k = np.argmax(s_scores)

        # Used for testing?
        # print(19 * '*')
        # print('|', k, k_val, '|')
        # print(19 * '*')

    else:
        kmeansData = clstr.KMeans(k).fit(whitened)

    # Clusters the images whiten data and recreates the actual centroid values.
    kArr = (kmeansData.cluster_centers_ * stdDev)

    # Reshapes the original picture to a (width*height)*RGB  matrix.
    # This is necessary for kmeans to predict the corresponding color for each pixel
    # in regards to the resized image is has been trained on.
    orgPicDim = im.shape
    orgPicReshape = im.reshape((orgPicDim[0] * orgPicDim[1], orgPicDim[2]))

    # Uses the learned data from the resized image to predict cluster for each pixel
    # on the original picture.
    tmp = np.array((kmeansData.labels_).reshape((dimensions[0], dimensions[1])))
    #print(tmp)
    #print("space")

    test = whiten(orgPicReshape)
    labels = kmeansData.predict(test)

    # Reshapes the label list back to the size of the origial image matrix,
    centroidMatrix = np.array(labels).reshape((orgPicDim[0], orgPicDim[1]))
    #print(centroidMatrix)
    # Returns a centroidmatrix representing the image with clustervalues instead of actual colors.
    return centroidMatrix, kArr

#cluster(misc.face(), 4, False)
#cluster(misc.imread("images/asdfghjk.jpg"), 4)
