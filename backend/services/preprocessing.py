import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler


class Preprocessor:

    def __init__(self):
        self.encoders = {}
        self.scaler = StandardScaler()

    def clean(self, df: pd.DataFrame):

        df = df.copy()

        # Remove duplicate rows
        df.drop_duplicates(inplace=True)

        # Remove completely empty rows
        df.dropna(how="all", inplace=True)

        for col in df.columns:

            if pd.api.types.is_numeric_dtype(df[col]):

                df[col] = df[col].fillna(df[col].median())

            else:

                df[col] = df[col].fillna("Unknown")

        return df

    def encode(self, df: pd.DataFrame):

        df = df.copy()

        for col in df.columns:

            if not pd.api.types.is_numeric_dtype(df[col]):

                encoder = LabelEncoder()

                df[col] = encoder.fit_transform(df[col].astype(str))

                self.encoders[col] = encoder

        return df

    def scale(self, df: pd.DataFrame):

        df = df.copy()

        # Don't scale the target column
        feature_columns = [col for col in df.columns if col != "Failure_Type"]

        df[feature_columns] = self.scaler.fit_transform(
            df[feature_columns]
        )

        return df

    def preprocess(self, df: pd.DataFrame):

        df = self.clean(df)

        df = self.encode(df)

        df = self.scale(df)

        return df