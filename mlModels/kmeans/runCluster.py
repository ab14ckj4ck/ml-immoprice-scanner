from mlModels.kmeans.locationClustering import trainLocationModel, addLocationFeature
from mlModels.kmeans.data.data import getClusterData
import logging


logging.basicConfig(filename='app.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def runCluster(n_clusters=14, seed=42):
    df = getClusterData()
    logging.info("Starting K-Means Clustering locations")
    kmeans = trainLocationModel(df, n_clusters=n_clusters, seed=seed)
    location_features = addLocationFeature(df, kmeans)
    logging.info("Finished K-Means Clustering locations")

    return location_features