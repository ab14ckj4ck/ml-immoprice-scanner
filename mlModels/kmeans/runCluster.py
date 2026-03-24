from mlModels.kmeans.locationClustering import trainLocationModel, addLocationFeature
from mlModels.kmeans.data.data import getData
import logging


logging.basicConfig(filename='app.log', level=logging.INFO, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def runCluster():
    df = getData()
    logging.info("Starting K-Means Clustering locations")
    scaler, kmeans = trainLocationModel(df)
    location_features = addLocationFeature(df, scaler, kmeans)
    logging.info("Finished K-Means Clustering locations")

    return location_features