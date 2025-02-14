import pandas as pd
from geopy.distance import geodesic
from pandarallel import pandarallel
pandarallel.initialize()

import multiprocessing.pool

class NonDaemonProcess(multiprocessing.Process):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daemon = False

    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass

class MyPool(multiprocessing.pool.Pool):
    Process = NonDaemonProcess

# (Optional) Remove this patch if pandarallel already handles process creation.
# Locator.pool = MyPool  

def find_nearest_location(row, df_destination, destination_name):
    """Module-level function to compute the nearest destination."""
    origin = (row['latitude'], row['longitude'])
    distances = df_destination.apply(
        lambda x: geodesic(origin, (x['latitude'], x['longitude'])).kilometers, axis=1
    )
    nearest_index = distances.idxmin()
    nearest_distance = distances[nearest_index]
    nearest_location = df_destination.loc[nearest_index, destination_name]
    return pd.Series([nearest_distance, nearest_location])

class Locator:
    """
    Locator class that calculates the closest distance and location.
    """
    def __init__(self, origin_location, df_destination, destination_name):
        """
        Args:
            origin_location (DataFrame): DataFrame with origin points.
            df_destination (DataFrame): DataFrame with destination points.
            destination_name (str): Column name in df_destination holding the location's name.
        """
        self.origin_location = origin_location
        self.df_destination = df_destination
        self.destination_name = destination_name

        # Use parallel_apply with a module-level function.
        self.result = self.origin_location.parallel_apply(
            find_nearest_location, axis=1, args=(self.df_destination, self.destination_name)
        )