import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from session_state_manager import initialize_session_state


class Pipelines:

    def __init__(self):
        pass

    def build(self, dataframe, categorical_features, numerical_features):
        # Build the pipeline for the categorical transformations
        pipeline = Pipeline(
            steps=[("ohe", OneHotEncoder(drop="first", sparse_output=False))]
        )

        # Create the column transformer using the pipelines defined above.
        fe_transformer = ColumnTransformer(
            transformers=[
                ("transf_cat", pipeline, categorical_features),
                ("scaled", StandardScaler(), numerical_features),
            ],
            remainder="drop",
        )

        # Fit the transformer to the dataframe
        fe_transformer.fit(dataframe)
        return (
            fe_transformer.get_feature_names_out(),
            pd.DataFrame(fe_transformer.transform(dataframe)),
        )
