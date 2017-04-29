import logging

import json
import numpy as np
from sklearn.cluster import DBSCAN

logger = logging.getLogger(__name__)


def dbscan(items, distance_matrix, eps=0.1, min_samples=1):
    if len(items) == 1:
        return [items]

    db = DBSCAN(metric='precomputed',
                eps=eps,
                min_samples=min_samples,
                n_jobs=-1)
    labels = db.fit_predict(distance_matrix)

    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    np_items = np.array(items)
    np_clusters = [np_items[labels == i] for i in range(n_clusters_)]
    scalar_clusters = [
        [np.asscalar(i) for i in cluster]
        for cluster in np_clusters
    ]
    return scalar_clusters


def load_clusters(path):
    with open(path, 'r') as clusters_json:
        clusters = json.load(clusters_json)

    return clusters
