from mlModels.kmeans.locationClustering import locationClustering
from mlModels.kmeans.data.data import getData
import logging


logging.basicConfig(filename='app.log', level=logging.INFO, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def runCluster():
    df = getData()
    logging.info("Starting K-Means Clustering locations")
    print("-------Starting K-Means Clustering locations-------")
    kmeans_label_results = locationClustering(df)

    return kmeans_label_results