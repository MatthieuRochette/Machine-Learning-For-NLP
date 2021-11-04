import re
from os import walk
from os.path import join, basename
from html.parser import HTMLParser
from random import Random

random_seed = 912
rand = Random(random_seed)

sep = "||"  # CSV separator for saving parsed data


class ReviewsHTMLParser(HTMLParser):
    CLEANR = re.compile("<.*?>")

    def __init__(self, tags_to_ignore: list = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags_to_ignore = tags_to_ignore or list()
        self.reviews = []
        self.current_review = None
        self.use_data = False
        self.current_tag = None
        self.empty_review = {
            "unique_id": None,
            "asin": None,
            "product_name": None,
            "product_type": None,
            "helpful": None,
            "rating": None,
            "title": None,
            "date": None,
            "reviewer": None,
            "reviewer_location": None,
            "review_text": None,
        }
        for k in self.tags_to_ignore:
            self.empty_review.pop(k)

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag == "review":
            self.current_review = self.empty_review.copy()
        elif tag in self.tags_to_ignore:
            return
        else:
            self.use_data = True
            self.current_tag = tag
            # print("start tag:", tag, "-> use_data =", self.use_data)

    def handle_endtag(self, tag):
        # print("endtag", tag)
        if tag == "review":
            self.reviews.append(self.current_review)
        else:
            self.current_tag = None
            self.use_data = False

    def handle_data(self, data):
        # print(data)
        if self.use_data:
            # print("Handling data in tag:", self.current_tag)
            data = re.sub(self.CLEANR, "", data)
            data = data.replace(sep, "/")  # to avoid errors when saving in CSV later
            # this is a one occurence in the electronics dataset
            data.replace("computer & video games", "electronics")
            self.current_review[self.current_tag] = data.replace("\n", "")
            self.use_data = False


def parse_reviews(path: str = "./original_data"):
    data = {}
    for root, _, fnames in walk(path):
        parser = ReviewsHTMLParser(
            tags_to_ignore=[
                "unique_id",
                "asin",
                "reviewer",
                "reviewer_location",
                "product_name",
                "helpful",
                "date",
                "title",
            ]
        )
        parsed_files = False
        for fname in fnames:
            if fname == "unlabeled.review":
                continue
            with open(join(root, fname), "r") as file:
                parser.feed(file.read())
            parsed_files = True
        if parsed_files:
            data[basename(root)] = parser.reviews
    return data


def convert_to_csv(data_set: list, file):
    inc = 0
    for key in data_set[0].keys():
        file.write(key)
        inc += 1
        if inc < len(data_set[0].keys()):
            file.write(sep)
    file.write("\n")
    for it in data_set:
        inc = 0
        for key in data_set[0].keys():
            file.write(it[key].rstrip("\n"))
            inc += 1
            if inc < len(data_set[0].keys()):
                file.write(sep)
        file.write("\n")


def split_data_set(data_source: list, save_path: str):
    training_set = []
    testing_set = []
    for _, v in data_source.items():
        # repeat-safe (in the short term) because rand is seeded and data_source is always
        # read in the same order by dict.items()
        rand.shuffle(v)
        train = v[: int((len(v) + 1) * 0.80)]
        test = v[int((len(v) + 1) * 0.80) :]
        # print(_, ":", len(v), type(v), v[0], end="\n\n")
        for i in train:
            training_set.append(i)
        for i in test:
            testing_set.append(i)

    training_file = open(
        join(save_path, "training_review.csv"), "w", encoding="utf-8-sig"
    )
    testing_file = open(
        join(save_path, "testing_review.csv"), "w", encoding="utf-8-sig"
    )

    convert_to_csv(training_set, training_file)
    convert_to_csv(testing_set, testing_file)

    training_file.close()
    testing_file.close()


def parse_data_to_csv(read_path: str = "./", save_path: str = "./"):
    split_data_set(parse_reviews(read_path), save_path)
    print(f"Parsed data to {save_path} CSV successfully.")


if __name__ == "__main__":
    parse_data_to_csv("./original_data", "./parsed_data")
