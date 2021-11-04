import pandas as pd
from os.path import join


class DataSet:
    def __init__(self, path: str, csv_sep: str = "\|\|") -> None:
        self.csv_sep = csv_sep
        self.training: pd.DataFrame = pd.read_csv(
            join(path, "training_review.csv"), sep=self.csv_sep, engine="python"
        )
        self.testing: pd.DataFrame = pd.read_csv(
            join(path, "testing_review.csv"), sep=self.csv_sep, engine="python"
        )

    def get_by_product_type(self, set: pd.DataFrame) -> dict[list]:
        types = set["product_type"].unique()
        ret_obj = {k: None for k in types}
        for type_ in types:
            ret_obj[type_] = set[set["product_type"] == type_].drop(
                "product_type", axis=1
            )
        return ret_obj

    def get_training_by_product_type(self):
        return self.get_by_product_type(self.training)

    def get_testing_by_product_type(self):
        return self.get_by_product_type(self.testing)


if __name__ == "__main__":
    ds = DataSet("./parsed_data/")
    print(ds.get_testing_by_product_type().keys())
    print(ds.get_training_by_product_type().keys())
