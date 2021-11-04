import pandas as pd
from os.path import join


class DataSet:
    def __init__(self, path: str, csv_sep: str = "\|\|") -> None:
        self.csv_sep = csv_sep

        self.training: pd.DataFrame = pd.read_csv(
            join(path, "training_review.csv"), sep=self.csv_sep, engine="python"
        ).rename({"product_type": "domain"}, axis=1)
        self.training = DataSet.transform_new_set(self.training)
        self.training_by_domain = DataSet.get_by_domain(self.training)

        self.testing: pd.DataFrame = pd.read_csv(
            join(path, "testing_review.csv"), sep=self.csv_sep, engine="python"
        ).rename({"product_type": "domain"}, axis=1)
        self.testing = DataSet.transform_new_set(self.testing)
        self.testing_by_domain = DataSet.get_by_domain(self.testing)

    @staticmethod
    def transform_new_set(df: pd.DataFrame) -> pd.DataFrame:
        def add_polarity_col(row):
            if row["rating"] < 3:
                row["polarity"] = "negative"
            else:
                row["polarity"] = "positive"
            return row

        df = df.apply(add_polarity_col, axis=1)
        df["rating_str"] = df["rating"].astype("object")
        return df

    @staticmethod
    def get_by_domain(df: pd.DataFrame) -> dict[str : pd.DataFrame]:
        types = df["domain"].unique()
        ret_obj = {k: None for k in types}
        for type_ in types:
            ret_obj[type_] = df[df["domain"] == type_].drop("domain", axis=1)
        return ret_obj


if __name__ == "__main__":
    ds = DataSet("./parsed_data/")
    print(ds.testing.dtypes)
    print(ds.testing)
