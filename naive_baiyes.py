import json
import argparse
import glob
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer
from nltk import NaiveBayesClassifier
from nltk import classify
from random import shuffle
import io
import parameter as param
from nltk.probability import FreqDist
import _pickle as pickle
import numpy as np

data = []
listOfGender = []
listOfWords = []
trainDataGender = []


def readfile(filename):
    new_comment = json.load(open(filename, 'r',encoding="utf-8"))
    
    if str(new_comment['gender']) == 'False':
        return

    for index, comment in enumerate(new_comment['comments']):
        flag = True
        garbage = ""
        for word in param.garbageWords:
            if word.lower() in word_tokenize(comment['text'].lower()):
                flag = False
                garbage = word
                print(word)
                break
        if flag:
            data.append((new_comment['gender'],comment['text']))

    shuffle(data)

def main(args):
    filenames = glob.glob("comments/*.json")
    
    for index, filename in enumerate(filenames):
        print(index)
        readfile(filename)

    print("number of user: " + str(len(filenames)))
    print("number of comments: "+str(len(data)))
    nb_classify(nb())

def nb():

    index = 0
    
    print("training")

    for gender,comment in data:
        tempDictionaryPositive = {}
        tempDictionaryNegative = {}


        if gender not in listOfGender:
            listOfGender.append(gender)

        for word in word_tokenize(comment):
        
            tempDictionaryPositive[word]=True
            tempDictionaryNegative[word]=False
            
            if word not in listOfWords:
                listOfWords.append(word)

        for gen in listOfGender:
            if(gen==gender):
                trainDataGender.append((tempDictionaryPositive,gen))
            else:
                trainDataGender.append((tempDictionaryNegative,gen))


    average_accuracy = 0
    size = len(trainDataGender)

    for i in range(1,9):

        test_set = trainDataGender[round((i-1)*size/8):round((i)*size/8)]
        training_set = trainDataGender[0:round((i-1)*size/8)]
        training_set.extend(trainDataGender[round((i)*size/8):])

        genderClassifier = NaiveBayesClassifier.train(training_set)
        print("{0:.2%}".format(classify.accuracy(genderClassifier,test_set)))
        average_accuracy += classify.accuracy(genderClassifier,test_set)

    average_accuracy /= 8
    print("average accuracy: " + "{0:.2%}".format(average_accuracy))

    try:
        #HELPPPPPPP
        print(genderClassifier.show_most_informative_features(5))
    except:
        True

    saveFile = open('model/gender_classifier.p',"wb")
    pickle.dump(genderClassifier,saveFile)
    saveFile.close()
    
    
    return genderClassifier

def nb_classify(genderClassifier):
    print("classifying")
    text=""
    while True:
        text = input("insert phrase >> ")
        if text == 'exit':
            break

        textDict = {}

        for word in word_tokenize(text):
            word = word.lower()
            textDict[word]=True

        print("Phrase = ",text)
        print("gender  = ",genderClassifier.classify(textDict))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    main(args)
    
    