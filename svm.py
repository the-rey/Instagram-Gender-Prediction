#!/usr/bin/env python

import sys
import json
from sklearn import svm
from sklearn.metrics import accuracy_score

LIMIT = 100

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

model = svm.SVC(kernel='linear', C=1, gamma=100)
model.fit(data, label)
model.score(data, label)
label_predicted = model.predict(data)

print(accuracy_score(label, label_predicted))