#!/usr/bin/env python3

import argparse
import glob
import io
import json
from random import shuffle

import nltk
import numpy as np
import parameter as param
from nltk import (NaiveBayesClassifier, WordNetLemmatizer, classify,
                  word_tokenize)
from nltk.corpus import stopwords
from nltk.probability import FreqDist

import _pickle as pickle

data = []
list_of_gender = []
list_of_words = []
train_data_gender = []


def read_file(filename):
    new_comment = json.load(open(filename, "r", encoding="utf-8"))

    if str(new_comment["gender"]) == "False":  # Invalid gender
        return

    for _, comment in enumerate(new_comment["comments"]):
        words_in_comment = word_tokenize(comment["text"].lower())

        valid = True
        for word in param.garbage_words:
            if word.lower() in words_in_comment:
                valid = False
                break

        if valid:
            data.append((new_comment["gender"], comment["text"]))

    shuffle(data)


def main(args):
    filenames = glob.glob("comments/*.json")
    for index, filename in enumerate(filenames):
        print(str(index) + " " + filename)
        read_file(filename)

    print("Number of user: " + str(len(filenames)))
    print("Number of comments: " + str(len(data)))

    naive_bayes_classify(naive_bayes())


def naive_bayes():
    print("Running Naive-Bayes Classifier")

    for gender, comment in data:
        word_exist = {}
        word_not_exist = {}

        if gender not in list_of_gender:
            list_of_gender.append(gender)

        for word in word_tokenize(comment):
            word_exist[word] = True
            word_not_exist[word] = False

            if word not in list_of_words:
                list_of_words.append(word)

        for gen in list_of_gender:
            if gen == gender:
                train_data_gender.append((word_exist, gen))
            else:
                train_data_gender.append((word_not_exist, gen))

    average_accuracy = 0
    size = len(train_data_gender)

    for i in range(1, 9):
        test_set = train_data_gender[round((i - 1) * size / 8): round((i) * size / 8)]
        training_set = train_data_gender[0: round((i - 1) * size / 8)]
        training_set.extend(train_data_gender[round((i) * size / 8):])

        gender_classifier = NaiveBayesClassifier.train(training_set)

        print("{0:.2%}".format(classify.accuracy(gender_classifier, test_set)))
        average_accuracy += classify.accuracy(gender_classifier, test_set)
    average_accuracy /= 8

    print("Average accuracy: " + "{0:.2%}".format(average_accuracy))

    try:
        text = gender_classifier.show_most_informative_features(5).encode('windows-1252')
        print(text)
    except:
        print("Exception...")
        True

    save_file = open("model/gender_classifier.p", "wb")
    pickle.dump(gender_classifier, save_file)
    save_file.close()

    return gender_classifier


def naive_bayes_classify(gender_classifier):
    print("Classifying using trained Naive-Bayes model")

    while True:
        text = input("Insert phrase >> ")
        if text.lower() == "exit":
            break

        text_dict = {}
        for word in word_tokenize(text):
            text_dict[word.lower()] = True

        print("Phrase = ", text)
        print("Gender  = ", gender_classifier.classify(text_dict))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    main(args)
