import numpy as np
import math

# Funciones que reducen el número de clusteres, eliminando los que tengan un tamaño inferior a numero de pixeles dado
def reduce_clusters(mean_shift_result,grid,min_size=1):
    """ Elimina los clusters con un numero de elementos menor o igual a min_pixel,
        asignandolos al cluster que tengan alrededor"""

    def get_max_neighbor(i,results,puntos_originales,ventana=10):
        entorno = [[puntos_originales[i][0]+t[0],puntos_originales[i][1]+t[1]] for t in [(-ventana,-ventana),(-ventana,0),(-ventana,ventana),
                                                                      (0,-ventana),(0,ventana),(ventana,-ventana),
                                                                      (ventana,0),(ventana,ventana)]
                                                                      if [puntos_originales[i][0]+t[0],puntos_originales[i][1]+t[1]] in [list(x) for x in puntos_originales]]

        clusteres = [results[z] for z in [[list(x) for x in puntos_originales].index([i[0],i[1]]) for i in entorno]]
        return clusteres[np.argmax(np.array([clusteres.count(i) for i in clusteres]))]


    def get_small_clusters(results,min_size):
        results = list(results)
        return [c for c in results if results.count(c)<=min_size]

    small_clusters = get_small_clusters(mean_shift_result.cluster_ids,min_size)
    return np.array([get_max_neighbor(i,mean_shift_result.cluster_ids,mean_shift_result.original_points[:,:2],grid) if c in small_clusters else c for (i,c) in list(enumerate(mean_shift_result.cluster_ids))])


# Clase para el clasificador bayesiano
class BayesianClassifier():
    def __init__(self,mean_shift_result):
        self.base_data_clusters=mean_shift_result.cluster_ids
        self.base_data_points=mean_shift_result.original_points
        self.classifiers=np.unique(self.base_data_clusters)
        self.modelos = self._generate_models()
        self.n_classifiers=len(self.classifiers)

    def _generate_models(self):
        modelos={}
        for c in self.classifiers:
            cluster_points = np.array([self.base_data_points[i] for i in range(len(self.base_data_points)) if self.base_data_clusters[i]==c])
            modelos.update({c:(np.mean(cluster_points),np.cov(cluster_points,rowvar=False))})
        return modelos

    def cluster_data_points(self,X):
        y = np.zeros(len(X))
        for i in range(len(X)):
            y[i]=self.point_classifier(X[i])
        return y

    def point_classifier(self,x):
        return np.argmax([self.likelihood(x,self.modelos[w])*1/self.n_classifiers for w in self.modelos.keys()])

    def likelihood(self,x,model):
        return (1/((math.pi**(len(x)/2)) * (np.linalg.det(model[1])**(1/2))))*np.exp(-0.5*np.transpose(np.add(x,-model[0])).dot(model[1]).dot(np.add(x,-model[0])))

    def show_classifiers(self):
        print("{} clasificadores:".format(len(self.classifiers)))
        for c in self.classifiers:
            print("Clasificador número {}".format(c))
            print("Media: {}".format(self.modelos[c][0]))
            print("Matriz de covarianza: {}".format(self.modelos[c][1]))
            print("Determinante: {}".format(np.linalg.det(self.modelos[c][1])))
            print("---------------------------------------")
