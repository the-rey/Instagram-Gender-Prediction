#!/usr/bin/env python3

import time

"""
Cache format

[data] is a file where each line is of the form:

    [M] [term_1]:[count] [term_2]:[count] ...  [term_N]:[count]

where [M] is the number of unique terms in the document, and the [count]
associated with each term is how many times that term appeared in the document.

[label] is a file where each line is the corresponding label for [data].
The labels must be 0, 1, ..., C-1, if we have C classes.
"""

TIMESTAMP = time.strftime("%H%M%S")


def cache_data(data, term_count, filename):
    filename = filename + "-" + TIMESTAMP + ".dat"

    with open(filename, "w") as f:
        for doc in data:
            f.write(str(term_count))
            for idx, count in enumerate(doc):
                f.write(" " + str(idx) + ":" + str(count))
            f.write("\n")


def cache_label(label, filename):
    filename = filename + "-" + TIMESTAMP + ".dat"

    with open(filename, "w") as f:
        for l in label:
            f.write(str(l) + "\n")


def cache(data, label, word_count):
    print("Caching data... [suffix: {}]".format(TIMESTAMP))
    cache_label(label, "label")
    cache_data(data, word_count, "data")
