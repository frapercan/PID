import math
import numpy as np


def euclidean_dist(pointA, pointB):
    if(len(pointA) != len(pointB)):
        raise Exception("expected point dimensionality to match")
    total = float(0)
    for dimension in range(0, len(pointA)):
        total += (pointA[dimension] - pointB[dimension])**2
    return math.sqrt(total)


def gaussian_kernel(distance, bandwidth, e=1):
    euclidean_distance = np.sqrt(((distance)**2).sum(axis=1))
    val = (1/(bandwidth*math.sqrt(2*math.pi))) * np.exp(-0.5*((euclidean_distance / bandwidth))**2)
    return val


def multivariate_gaussian_kernel(distances, bandwidths, e=1):

    # Number of dimensions of the multivariate gaussian
    dim = len(bandwidths)

    # Covariance matrix
    cov = np.multiply(np.power(bandwidths, 2), np.eye(dim))

    # Compute Multivariate gaussian (vectorized implementation)
    exponent = -0.5 * np.sum(np.multiply(np.dot(distances, np.linalg.inv(cov)), distances), axis=1)
    val = (1 / np.power((2 * math.pi), (dim/2)) * np.power(np.linalg.det(cov), 0.5)) * np.exp(exponent)

    return val

def epanechnikov_kernel(distance,bw,e=1):
    distance_s = distance[:,:2]/bw[0]
    distance_r = distance[:,2:5]/bw[1]

    ek_s = epanechnikov_profile(np.power(np.array([np.linalg.norm(distance_s[i]) for i in range(len(distance_s)) ]),2))
    ek_r = epanechnikov_profile(np.power(np.array([np.linalg.norm(distance_r[i]) for i in range(len(distance_r)) ]),2))

    #print(np.array([np.linalg.norm(distance_s[i]) for i in range(len(distance_s)) ]))
    #print(np.array([np.linalg.norm(distance_r[i]) for i in range(len(distance_r)) ]))

    val = (e/(bw[0]**2)*(bw[1]**2))*ek_s*ek_r

    return val

def epanechnikov_profile(values):
    return np.array([1-x if np.linalg.norm(x)<=1 else 0 for x in values])
