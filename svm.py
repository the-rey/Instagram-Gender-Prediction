import json
import argparse
import glob
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
            if word in word_tokenize(comment['text']):
                flag = False
                garbage = word
                break
        if flag:
            data.append((new_comment['gender'],comment['text']))

    shuffle(data)

def main(args):
    filenames = glob.glob("comments/*.json")
    
    for filename in filenames:
        readfile(filename)

    print("number of user: " + str(len(filenames)))
    print("number of comments: "+str(len(data)))
    svm_classify(svm())

def svm():

    index = 0

    

    for gender,comment in data:
        tempDictionaryPositive = {}
        tempDictionaryNegative = {}


        if gender not in listOfGender:
            listOfGender.append(gender)

        for word in word_tokenize(comment):
        
            tempDictionaryPositive[word]=True
            tempDictionaryNegative[word]=False
            listOfWords.append(word)

        for gen in listOfGender:
            if(gen==gender):
                trainDataGender.append((tempDictionaryPositive,gen))
            else:
                trainDataGender.append((tempDictionaryNegative,gen))


    genderClassifier = NaiveBayesClassifier.train(trainDataGender[1000:])
    print("{0:.2%}".format(classify.accuracy(genderClassifier,trainDataGender[:1000])))

    try:
        #HELPPPPPPP
        print(genderClassifier.show_most_informative_features(5))
    except:
        True

    saveFile = open('model/gender_classifier.p',"wb")
    pickle.dump(genderClassifier,saveFile)
    saveFile.close()
    
    
    return genderClassifier

def svm_classify(genderClassifier):
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
    
    