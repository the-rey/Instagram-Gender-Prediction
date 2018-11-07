#!/usr/bin/env python3

import sys
import json
import time
import argparse

from sklearn import svm
from sklearn.metrics import accuracy_score

def start_progress(title):
    global progress_x
    sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    sys.stdout.flush()
    progress_x = 0

def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("#" * (x - progress_x))
    sys.stdout.flush()
    progress_x = x

def end_progress():
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()

def run_tests(data, label, size, split):
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
        model = svm.SVC(C=10, kernel=args.kernel, gamma=args.gamma)
        model.fit(training_set, label_training_set)
        model.score(training_set, label_training_set)

        print("> Predicting test data...")
        label_predicted = model.predict(test_set)

        avg_accuracy += accuracy_score(label_test_set, label_predicted)
        print("> Accuracy: {0:.2f}%".format(accuracy_score(label_test_set, label_predicted) * 100))

    print("=====================================")
    print("Avg. Accuracy: {0:.2f}%".format(avg_accuracy * 100 / split))

def main(args):
    start_time = time.time()
    print("Running SVM Classifier")
    with open('data/gender-comment.json', 'r') as f:
        gender_comment = json.load(f)

    with open('data/list-of-words.json', 'r') as f:
        list_of_words = json.load(f)

    list_of_words   = list(set(list_of_words))  # Remove duplicates
    word_count      = len(list_of_words)        # Get total word count
    dict_of_words   = {}                        # Mapping word to index

    for idx, word in enumerate(list_of_words):
        dict_of_words[word] = idx

    data = []
    label = []
    start_progress("Reading data")
    total = len(gender_comment)
    if args.limit != -1:
        total = args.limit
    for i, j in enumerate(gender_comment):
        # Label for female = 0, and male = 1
        if j[0] == 'female':
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
        if i == args.limit:
            break
    end_progress()

    run_tests(data, label, total, 8)

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
        help="Limit processed data")

    parser.add_argument(
        "-g",
        "--gamma",
        action="store",
        dest="gamma",
        default=1,
        type=int,
        help="Gamma value")

    parser.add_argument(
        "-k",
        "--kernel",
        action="store",
        dest="kernel",
        default="linear",
        help="Kernel to use")

    args = parser.parse_args()
    main(args)