"""
geo_utils.py
-------------
Small collection of geographic helper functions

Made simple so notebooks can import:
    from src.geo_utils import haversine_km
"""

import numpy as np


def haversine_km(lat1, lon1, lat2, lon2):
    """
    Compute the great-circle distance (in km) between two points.

    Parameters
    ----------
    lat1, lon1 : float
        Latitude & longitude of point A.
    lat2, lon2 : float
        Latitude & longitude of point B.

    Notes
    -----
    Uses the Haversine formula. Works well for general logistics planning.
    Not meant for high  precision geodesy hehe, but more than enough
    for hub/route simulations ;)

    Returns
    -------
    float
        Distance in kilometers.
    """

    R = 6371.0  # Earth's radius in km

    # convert to radians (avoid weird trig later)
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2)**2
        + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    )
    c = 2 * np.arctan2(a**0.5, (1 - a)**0.5)

    return R * c
