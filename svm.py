#!/usr/bin/env python

import sys
import json
from sklearn import svm
from sklearn.metrics import accuracy_score

LIMIT = 1000

with open('gender-comment.json', 'r') as f:
    gender_comment = json.load(f)

with open('list-of-words.json', 'r') as f:
    list_of_words = json.load(f)

list_of_words   = list(set(list_of_words)) # Remove duplicate words
word_count      = len(list_of_words) # Get total word count
dict_of_words   = {} # Mapping word to index

for idx, word in enumerate(list_of_words):
    dict_of_words[word] = idx

data = []
label = []
# gender_comment.sort()
for i, v in enumerate(gender_comment):

    # Label for female = 0, and male = 1
    if v[0] == 'female':
        label.append(0)
    else:
        label.append(1)

    wc = {}
    for word in v[1].split():
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

    print(i)
    if i == 197:
        print(gender_comment[i][0], gender_comment[i][1])
    if i == LIMIT:
        break


size = LIMIT

average_accuracy = 0

for i in range(1,9):

        test_set = data[round((i-1)*size/8):round((i)*size/8)]
        label_test_set = label[round((i-1)*size/8):round((i)*size/8)]
        
        training_set = data[0:round((i-1)*size/8)]
        training_set.extend(data[round((i)*size/8):])

        label_training_set = label[0:round((i-1)*size/8)]
        label_training_set.extend(label[round((i)*size/8):])

        print("starting test ke " + str(i))

        model = svm.SVC(kernel='linear', C=10, gamma=100)
        model.fit(training_set, label_training_set)
        model.score(training_set, label_training_set)

        label_predicted = model.predict(test_set)

        average_accuracy += accuracy_score(label_test_set, label_predicted)
        print(str(accuracy_score(label_test_set, label_predicted)))

print("{0:.2%}".format(average_accuracy/8))