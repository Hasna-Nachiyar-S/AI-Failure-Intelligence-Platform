from typing import Dict
import pandas as pd


class Analytics:

    @staticmethod
    def dataset_info(df: pd.DataFrame) -> Dict:
        return {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "missing_values": int(df.isnull().sum().sum()),
            "duplicates": int(df.duplicated().sum())
        }

    @staticmethod
    def missing_values(df: pd.DataFrame):
        return df.isnull().sum()

    @staticmethod
    def duplicate_rows(df: pd.DataFrame):
        return df.duplicated().sum()

    @staticmethod
    def summary(df: pd.DataFrame):
        return df.describe(include="all")

    @staticmethod
    def value_count(df: pd.DataFrame, column: str):
        return df[column].value_counts()

    @staticmethod
    def numeric_statistics(df: pd.DataFrame):
        return df.describe()

    @staticmethod
    def correlation(df: pd.DataFrame):
        numeric = df.select_dtypes(include="number")
        return numeric.corr()

    @staticmethod
    def top_values(df: pd.DataFrame, column: str, n: int = 10):
        return df[column].value_counts().head(n)