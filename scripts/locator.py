import pandas as pd
from geopy.distance import geodesic


class Locator:
    """
        Locatorclass
    """
    def __init__(self, origin_location, df_destination, destination_name):
        """_summary_

        Args:
            origin_location (_type_): DataFrame from where to calculate
            df_destination (_type_): DataFrame with destinatin
            destination_name (_type_): location name for closest point

        Returns:
            _type_: returns nearest distance and nearest location in series
        """
        self.df_destination = df_destination
        self.destination_name = destination_name
        self.origin_location = origin_location
        self.result = self.origin_location.apply(lambda row: self._find_nearest_location(row), axis=1)

    def _find_nearest_location(self, row):
        self.origin_location = (row['latitude'], row['longitude'])
        # Calculate distance from the town to every airport
        distances = self.df_destination.apply(lambda x: geodesic(self.origin_location, (x['latitude'], x['longitude'])).kilometers, axis=1)
        # Find the index of the airport with the smallest distance
        nearest_index = distances.idxmin()
        # Retrieve the minimum distance and corresponding airport ID
        nearest_distance = distances[nearest_index]
        nearest_location = self.df_destination.loc[nearest_index, self.destination_name]
        return pd.Series([nearest_distance, nearest_location])