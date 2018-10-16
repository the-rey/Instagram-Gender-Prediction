#!/usr/bin/env python
# -*- coding: utf-8 -*-
import statistics as statistics

data = {}

def addGenderAndAge(username, gender, age):
    if(not (username in data)):
        data[username] = {}
        data[username]['gender'] = []
        data[username]['age'] = []

    data[username]['gender'].append(gender)
    data[username]['age'].append(int(age))

def getAge(username):
    if(not (username in data)):
        return False

    try:
        return statistics.mode(data[username]['age'])
    except:
        try:
            return statistics.median(data[username]['age'])
        except: 
            try:
                return statistics.median_grouped(data[username]['age'])
            except:
                return False

def getGender(username):
    if(not (username in data)):
        return False

    try:
        return statistics.mode(data[username]['gender'])
    except:
        return False