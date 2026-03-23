"""
This module provides functionality for spatial clustering of real estate data based on
latitude and longitude. It utilizes the K-Means algorithm and evaluates multiple
statistical metrics (Elbow, Silhouette, Gap Statistic, Davies-Bouldin, and
Calinski-Harabasz) to determine the optimal number of clusters for geographical
segmentation.
"""

import numpy as np
import pandas as pd
import math

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.preprocessing import StandardScaler
from kneed import KneeLocator

def locationClustering(df, seed=42, lower=2, upper=15):
    """
    Performs K-Means clustering on latitude and longitude coordinates using multiple
    evaluation metrics to find optimal cluster counts.

    Args:
        df (pd.DataFrame): Input dataframe containing 'lat' and 'lon' columns.
        seed (int): Random seed for reproducibility.
        lower (int): Minimum number of clusters to test.
        upper (int): Maximum number of clusters to test.

    Returns:
        dict: A dictionary where keys are cluster counts and values are dataframes with one-hot encoded cluster labels.
        results = {
            2: df_k2,
            4: df_k4,
            6: df_k6,
    """
    coords = df[["lat", "lon"]].values
    scaled_coords = StandardScaler().fit_transform(coords)
    ellbow_vals, silhouette_vals, gap_vals, davies_vals, calinski_vals = findKMethod(scaled_coords, random_state=seed, lower_range=lower, upper_range=upper)

    candidates = [kneedleAlgorithm(ellbow_vals, lower, upper),
                  max(silhouette_vals, key=lambda k: k[0])[1],
                  max(gap_vals, key=lambda k: k[0])[1],
                  min(davies_vals, key=lambda k: k[0])[1],
                  max(calinski_vals, key=lambda k: k[0])[1]]
    candidates = list(set(candidates))
    candidates.sort()

    results = {}

    for c in candidates:
        df_temp = df.copy()
        labels = KMeans(n_clusters=c, random_state=random_state).fit_predict(scaled_coords)
        df_temp[f"cluster_{c}"] = labels
        df_temp = pd.get_dummies(df_temp, columns=[f"cluster_{c}"], prefix=f"loc_{c}")
        results[c] = df_temp

    return results


def findKMethod(coords, random_state, lower_range, upper_range):
    """
    Calculates various clustering metrics for a range of K values.

    Args:
        coords (np.ndarray): Scaled coordinate array.
        random_state (int): Random seed for reproducibility.
        lower_range (int): Minimum number of clusters to test.
        upper_range (int): Maximum number of clusters to test.

    Returns:
        tuple: Lists of scores for Elbow, Silhouette, Gap, Davies-Bouldin, and Calinski-Harabasz methods.
    """
    ellbow_vals = ellbow(coords, random_state, lower_range, upper_range)
    silhouette_vals = silhouette(coords, random_state, lower_range, upper_range)
    gap_vals = gapMethod(coords, random_state, lower_range, upper_range)
    davies_vals = daviesBouldin(coords, random_state, lower_range, upper_range)
    calinski_vals = calinskiHarabasz(coords, random_state, lower_range, upper_range)

    return ellbow_vals, silhouette_vals, gap_vals, davies_vals, calinski_vals


def ellbow(coords, random_state, lower, upper):
    """
    Calculates the sum of squared distances (inertia) for each K.

    Args:
        coords (np.ndarray): Scaled coordinate array.
        random_state (int): Random seed for reproducibility.
        lower (int): Start of K range.
        upper (int): End of K range.

    Returns:
        list: Inertia values for each K.
    """
    inertia = []
    for k in range(lower, upper):
        kmeans = KMeans(n_clusters=k, random_state=random_state)
        kmeans.fit(coords)
        inertia.append(kmeans.inertia_)
    return inertia


def kneedleAlgorithm(vals, lower, upper):
    """
    Identifies the 'knee' point in the elbow curve.

    Args:
        vals (list): Inertia values.
        lower (int): Start of K range.
        upper (int): End of K range.

    Returns:
        int: The optimal number of clusters according to the Kneedle algorithm.
    """
    kneedle = KneeLocator(
        x=range(lower, upper),
        y=vals,
        curve="convex",
        direction="decreasing"
    )
    x = kneedle.knee
    if x is None or (isinstance(x, float)) or math.isnan(x):
        diffs = np.diff(vals)
        x = lower + np.argmin(diffs)
    return x


def silhouette(coords, random_state, lower, upper):
    """
    Calculates Silhouette scores for each K.

    Args:
        coords (np.ndarray): Scaled coordinate array.
        random_state (int): Random seed for reproducibility.
        lower (int): Start of K range.
        upper (int): End of K range.

    Returns:
        list: Tuples of (silhouette_score, k).
    """
    scores = []
    for k in range(lower, upper):
        kmeans = KMeans(n_clusters=k, random_state=random_state)
        labels = kmeans.fit_predict(coords)
        scores.append((silhouette_score(coords, labels), k))
    return scores


def gapMethod(coords, random_state, lower, upper, n_refs=5):
    """
    Calculates the Gap Statistic for each K.

    Args:
        coords (np.ndarray): Scaled coordinate array.
        random_state (int): Random seed for reproducibility.
        lower (int): Start of K range.
        upper (int): End of K range.
        n_refs (int): Number of reference distributions to create.

    Returns:
        list: Tuples of (gap_value, k).
    """
    mins = coords.min(axis=0)
    maxs = coords.max(axis=0)
    gaps = []
    for k in range(lower, upper):
        kmeans = KMeans(n_clusters=k, random_state=random_state)
        kmeans.fit(coords)
        orig = kmeans.inertia_

        ref = []
        for _ in range(n_refs):
            rand = np.random.uniform(mins, maxs, size=coords.shape)
            kmeans_ref = KMeans(n_clusters=k, random_state=random_state)
            kmeans_ref.fit(rand)
            ref.append(kmeans_ref.inertia_)

        gap = np.log(np.mean(ref)) - np.log(orig)
        gaps.append((gap, k))
    return gaps


def daviesBouldin(coords, random_state, lower, upper):
    """
    Calculates Davies-Bouldin scores for each K.

    Args:
        coords (np.ndarray): Scaled coordinate array.
        random_state (int): Random seed for reproducibility.
        lower (int): Start of K range.
        upper (int): End of K range.

    Returns:
        list: Tuples of (davies_bouldin_score, k).
    """
    scores = []
    for k in range(lower, upper):
        labels = KMeans(n_clusters=k, random_state=random_state).fit_predict(coords)
        scores.append((davies_bouldin_score(coords, labels), k))
    return scores


def calinskiHarabasz(coords, random_state, lower, upper):
    """
    Calculates Calinski-Harabasz scores for each K.

    Args:
        coords (np.ndarray): Scaled coordinate array.
        random_state (int): Random seed for reproducibility.
        lower (int): Start of K range.
        upper (int): End of K range.

    Returns:
        list: Tuples of (calinski_harabasz_score, k).
    """
    scores = []
    for k in range(lower, upper):
        labels = KMeans(n_clusters=k, random_state=random_state).fit_predict(coords)
        scores.append((calinski_harabasz_score(coords, labels), k))
    return scores
