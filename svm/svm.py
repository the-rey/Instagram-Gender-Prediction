#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html

import argparse
import json
import math
import random
import sys
import time

from progress import end_progress, progress, start_progress
from sklearn import svm
from sklearn.metrics import accuracy_score

from cache import cache

BLACKLIST_WORDS = []


def load_blacklist_words(filename):
    global BLACKLIST_WORDS
    with open(filename) as f:
        BLACKLIST_WORDS = f.readlines()
    BLACKLIST_WORDS = [x.strip() for x in BLACKLIST_WORDS]


def run_tests(data, label, size, split, kernel, gamma):
    print("\nRunning tests")
    print("=============")
    print("Kernel:", kernel)
    print("Gamma:", gamma)
    print("=============\n")
    avg_accuracy = 0

    for i in range(1, split + 1):
        test_set = data[round((i - 1) * size / split):round((i) * size / split)]
        label_test_set = label[round((i - 1) * size / split):round((i) * size / split)]

        training_set = data[0:round((i - 1) * size / split)]
        training_set.extend(data[round((i) * size / split):])

        label_training_set = label[0:round((i - 1) * size / split)]
        label_training_set.extend(label[round((i) * size / split):])

        print("Test-" + str(i))
        print("> Training model...")
        model = svm.SVC(C=10, kernel=kernel, gamma=gamma)
        model.fit(training_set, label_training_set)
        model.score(training_set, label_training_set)

        print("> Predicting test data...")
        label_predicted = model.predict(test_set)

        avg_accuracy += accuracy_score(label_test_set, label_predicted)
        print("> Accuracy: {0:.2f}%\n".format(accuracy_score(label_test_set, label_predicted) * 100))

    print("=====================================")
    print("Avg. Accuracy: {0:.2f}%".format(avg_accuracy * 100 / split))


def main(args):
    start_time = time.time()
    print("Running SVM Classifier")

    print("Reading blacklist words file")
    load_blacklist_words("data/blacklist.txt")

    print("Reading raw gender-comment data")
    with open('data/male-comments.json', 'r') as f:
        male_comment = json.load(f)
    with open('data/female-comments.json', 'r') as f:
        female_comment = json.load(f)
    print("Loaded {} male and {} female comments".format(len(male_comment), len(female_comment)))

    if args.limit != -1:
        args.limit_per_gender = int(args.limit / 2)
        print("Limiting male and female comments to {} each ({} total)".format(args.limit_per_gender, args.limit))
        try:
            del male_comment[args.limit_per_gender:]
            del female_comment[args.limit_per_gender:]
        except:
            print("Not enough male/female comments data")
            sys.exit(1)

    if args.limit_per_gender > len(male_comment):
        print("Warning, limit per gender is higher than available male comments:", len(male_comment))
    if args.limit_per_gender > len(female_comment):
        print("Warning, limit per gender is higher than available female comments:", len(female_comment))

    gender_comment = []
    for idx, data in enumerate(male_comment):
        if idx >= args.limit_per_gender:
            print("Stored {} male comments".format(idx))
            break
        data[1] = data[1].lower()
        gender_comment.append(data)
    for idx, data in enumerate(female_comment):
        if idx >= args.limit_per_gender:
            print("Stored {} female comments".format(idx))
            break
        data[1] = data[1].lower()
        gender_comment.append(data)
    random.shuffle(gender_comment)

    list_of_words = set()
    for data in gender_comment:
        words = list(filter(lambda x: x not in BLACKLIST_WORDS, data[1].split(' ')))
        list_of_words.update(words)
    list_of_words = list(list_of_words)
    word_count = len(list_of_words)

    print("Total of {} words found".format(word_count))

    data = []
    label = []
    total = len(gender_comment)
    start_progress("Processing {} raw gender-comment data".format(total))
    for i, j in enumerate(gender_comment):
        if j[0] == 'female':  # Label for female = 0, and male = 1
            label.append(0)
        else:
            label.append(1)

        wc = {}
        for word in j[1].split():
            if word in wc:
                wc[word] += 1
            else:
                wc[word] = 1

        d = []
        for idx in range(word_count):
            count = 0
            if list_of_words[idx] in wc:
                count = wc[list_of_words[idx]]
            d.append(count)
        data.append(d)

        progress(i / total * 100)
        if i == total:
            break
    end_progress()

    if args.cache:
        cache(data, label, word_count)

    run_tests(data, label, total, 8, args.kernel, args.gamma)

    print("Elapsed time: {0:.2f}s".format(time.time() - start_time))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-l",
        "--limit",
        action="store",
        dest="limit",
        default=-1,
        type=int,
        help="Limit processed data, equal male and female comments")

    parser.add_argument(
        "-e",
        "--limit-per-gender",
        action="store",
        dest="limit_per_gender",
        default=math.inf,
        type=int,
        help="Limit per gender")

    parser.add_argument(
        "-c",
        "--cache",
        action="store_true",
        dest="cache",
        default=False,
        help="Cache processed raw data")

    # Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’.
    parser.add_argument(
        "-g",
        "--gamma",
        action="store",
        dest="gamma",
        default=1,
        type=int,
        help="Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’")

    # Specifies the kernel type to be used in the algorithm
    # Must be one of ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’ or a
    # callable. If none is given, ‘rbf’ will be used
    parser.add_argument(
        "-k",
        "--kernel",
        action="store",
        dest="kernel",
        default="rbf",
        help="Specifies the kernel type to be used in the algorithm")

    args = parser.parse_args()
    main(args)
