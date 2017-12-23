import numpy as np

import mean_shift_utils_epanechnikov as ms_utils
import point_grouper as pg


#EN EL ARCHIVO ORIGNAL ESTABA COMO: MIN_DISTANCE = 0.000001
MIN_DISTANCE = 3

class MeanShift(object):
    def __init__(self, kernel=ms_utils.gaussian_kernel):
        """Inicializa el objeto meanshift, con un kernel"""
        if kernel == 'multivariate_gaussian':
            kernel = ms_utils.multivariate_gaussian_kernel
        elif kernel == 'epanechnikov_kernel':
            kernel = ms_utils.epanechnikov_kernel
        self.kernel = kernel

    def cluster(self, points, kernel_bandwidth, iteration_callback=None):
          
        """Recibe una lista de puntos, el tamaño de la distancia a tener en cuenta al utilizar el Kernel,
           y un parametro para sacar los estados a mitad del algoritmo(Debug).
        """
        if(iteration_callback):
            iteration_callback(points, 0)
        shift_points = np.array(points)
        max_min_dist = 10000000
        dist=0
        dist_after=1
        iteration_number = 0

        still_shifting = [True] * points.shape[0]
        while max_min_dist > MIN_DISTANCE:
            print(max_min_dist)
            max_min_dist = 0
            iteration_number += 1
            for i in range(0, len(shift_points)):
                if not still_shifting[i]:
                    continue
                print(i)
                p_new = shift_points[i]
                p_new_start = p_new
                p_new = self._shift_point(p_new, points, kernel_bandwidth)
                dist = 0 if dist==(ms_utils.euclidean_dist(p_new[:2], p_new_start[:2])+ms_utils.euclidean_dist(p_new[2:5], p_new_start[2:5])) else ms_utils.euclidean_dist(p_new[:2], p_new_start[:2])+ms_utils.euclidean_dist(p_new[2:5], p_new_start[2:5])
                if dist > max_min_dist:
                    max_min_dist = dist
                if dist < MIN_DISTANCE:
                    still_shifting[i] = False
                shift_points[i] = p_new
            if iteration_callback:
                iteration_callback(shift_points, iteration_number)
        point_grouper = pg.PointGrouper()
        group_assignments = point_grouper.group_points(shift_points.tolist())
        return MeanShiftResult(points, shift_points, group_assignments)
    
    def _shift_point(self, point, points, kernel_bandwidth):
        # from http://en.wikipedia.org/wiki/Mean-shift
        """Recibe un punto, una lista de puntos, y el ancho del kernel"""
        points = np.array(points)

        # numerator
        point_weights = self.kernel(point-points, kernel_bandwidth)
        tiled_weights = np.tile(point_weights, [len(point), 1])
        # denominator
        denominator = sum(point_weights)
        shifted_point = np.multiply(tiled_weights.transpose(), points).sum(axis=0) / denominator
        #print(point-points)
        #print(shifted_point==point)
        """recibe una lista  donde los puntos se han desplazado para formar un cluster"""
        return shifted_point

class MeanShiftResult:
    def __init__(self, original_points, shifted_points, cluster_ids):
        self.original_points = original_points
        self.shifted_points = shifted_points
        self.cluster_ids = cluster_ids

