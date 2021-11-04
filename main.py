from src.dataset import DataSet
from src.dataset_parser import parse_data_to_csv

raw_path = "./original_data"
parsed_path = "./parsed_data"
parse_data_to_csv(raw_path, parsed_path)
ds = DataSet("./parsed_data/")
print(ds.training, ds.training.dtypes)
