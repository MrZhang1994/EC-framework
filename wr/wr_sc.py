import numpy as np
from sklearn.cluster import SpectralClustering
from sklearn import metrics
import warnings
import time


def warn_disable(*args, **kwargs):
    pass


def cal_sum(Graph, data):
    cut_sum = 0
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            if data[i] != data[j]:
                cut_sum += Graph[i][j]

    return cut_sum


def check_iso(Graph, iso, iso_threshold, sc_data):
    cluster_data = {}
    for i, val in enumerate(sc_data):
        if val not in cluster_data:
            cluster_data[val] = set()
        cluster_data[val].add(i)

    for i in cluster_data:
        iso_sum = 0
        cluster = list(cluster_data[i])
        for ii in range(len(cluster)):
            for jj in range(ii+1, len(cluster)):
                iso_sum += iso[cluster[ii]][cluster[jj]]

        if iso_sum > iso_threshold:
            # print(cluster_data,iso_sum)
            return False

    return True


def sc(Graph, isolation, isolation_threshold, time_measure, times_for_each_sc_num=5):
    Graph = list(Graph) + np.transpose(Graph)
    isolation = list(isolation) + np.transpose(isolation)
    warnings.warn = warn_disable

    best_cluster, best_cut_sum = [], -1

    for cluster_num in range(1, len(Graph)):
        for i_for_each_sc_num in range(1, times_for_each_sc_num):
            sc_start = time.time()
            sc = SpectralClustering(n_clusters=cluster_num,
                                    affinity='precomputed')
            sc.fit(Graph)
            sc_end = time.time()
            time_measure[0]+=sc_end-sc_start

            if not check_iso(Graph, isolation, isolation_threshold, sc.labels_):
                continue

            cut_sum = cal_sum(Graph, sc.labels_)

            if best_cut_sum < 0 or cut_sum < best_cut_sum:
                best_cut_sum = cut_sum
                best_cluster = list(sc.labels_)

    cluster_data = {}
    for i, val in enumerate(best_cluster):
        if val not in cluster_data:
            cluster_data[val] = set()
        cluster_data[val].add(i)

    cluster_num_result = max(cluster_data)+1

    return cluster_data, best_cut_sum
