from os import walk
from os.path import join, basename
from html.parser import HTMLParser


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
            self.current_review[self.current_tag] = data
            self.use_data = False

    def get_reviews(self):
        return self.reviews


def parse_reviews(path: str = "./original_data"):
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


data = parse_reviews()
print(len(data))
print(data.keys())
for k, v in data.items():
    print(k, ":", len(v), type(v), v[0], end="\n\n")
