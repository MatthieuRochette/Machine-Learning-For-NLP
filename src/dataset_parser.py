from os import walk
from os.path import join, basename
from html.parser import HTMLParser
from random import random


class ReviewsHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reviews = []
        self.current_review = None
        self.use_data = False
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag == "review":
            self.current_review = {
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
        else:
            self.use_data = True
            self.current_tag = tag

    def handle_endtag(self, tag):
        # print("endtag", tag)
        if tag == "review":
            self.reviews.append(self.current_review)
        else:
            self.current_tag = None

    def handle_data(self, data):
        # print(data)
        if self.use_data:
            self.current_review[self.current_tag] = data.replace("\n", "")
            self.use_data = False

    def get_reviews(self):
        return self.reviews


def parse_reviews(path: str = "../original_data"):
    data = {}
    for root, dirnames, fnames in walk(path):
        parser = ReviewsHTMLParser()
        parsed_files = False
        for fname in fnames:
            if fname == "unlabeled.review":
                continue
            # print(root + "/" + fname)
            with open(join(root, fname), "r") as file:
                # file_content = file.read()
                # print(file_content)
                parser.feed(file.read())
            parsed_files = True
        if parsed_files:
            data[basename(root)] = parser.get_reviews()
    return data


def write_in_file(data_set: [], file):
    sep = "|"
    inc = 0
    for key in data_set[0].keys():
        file.write(key)
        inc += 1
        if inc < len(data_set[0].keys()):
            file.write(sep)
    file.write('\n')
    for it in data_set:
        inc = 0
        for key in data_set[0].keys():
            file.write(it[key].rstrip("\n"))
            inc += 1
            if inc < len(data_set[0].keys()):
                file.write(sep)

        file.write('\n')


def split_data_set(data_source: []):
    training_set = []
    testing_set = []
    for k, v in data_source.items():
        train = v[:int((len(v) + 1) * 0.80)]
        test = v[int((len(v) + 1) * 0.80):]
        print(k, ":", len(v), type(v), v[0], end="\n\n")
        for i in train:
            training_set.append(i)
        for i in test:
            testing_set.append(i)

    training_file = open("../training_review.csv", 'w', encoding='utf-8-sig')
    testing_file = open("../testing_review.csv", 'w', encoding='utf-8-sig')

    write_in_file(training_set, training_file)
    write_in_file(testing_set, testing_file)

    training_file.close()
    testing_file.close()


data = parse_reviews()
print(len(data))
print(data.keys())
split_data_set(data)
