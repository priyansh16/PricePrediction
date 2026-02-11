import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingRegressor


# -------------------------------------------------
# Custom Transformer: Municipality Target Encoding
# -------------------------------------------------

class MunicipalityEncoder(BaseEstimator, TransformerMixin):

    def fit(self, X, y):
        """
        Learn mean price per municipality
        """
        df = pd.DataFrame({
            "Municipality": X["Municipality"],
            "target": y
        })

        self.mapping = (
            df.groupby("Municipality")["target"]
            .mean()
            .to_dict()
        )

        self.global_mean = y.mean()
        return self

    def transform(self, X):
        """
        Apply learned mapping
        """
        X = X.copy()

        X["Municipality"] = X["Municipality"].map(self.mapping)
        X["Municipality"] = X["Municipality"].fillna(self.global_mean)

        return X


# -------------------------------------------------
# Pipeline Builder
# -------------------------------------------------

def build_pipeline():

    # Categorical features for OneHotEncoding
    categorical_cols = ["Built_on", "House_type", "Lift", "Balcony"]

    # ColumnTransformer handles OneHotEncoding
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_cols
            )
        ],
        remainder="passthrough"  # keep numeric columns
    )

    # Full pipeline
    pipeline = Pipeline(steps=[
        ("municipality_encoder", MunicipalityEncoder()),
        ("preprocessor", preprocessor),
        ("model", GradientBoostingRegressor())
    ])

    return pipeline
