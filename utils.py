# -*- coding: utf-8 -*-
from __future__ import print_function
import requests
from bs4 import BeautifulSoup
from random import randint
from time import sleep

def printCollectionContent(openings, level, levelIdentation, identation, key, value):
    print(u"{}{}[{}] =>".format(levelIdentation, identation, key), end=" ")

    if type(value).__name__ not in openings:
        print(u"{}".format(value).encode('utf-8'))
    else:
        printCollection(value, level + 1)

def printCollection(collection, level = 0):
    identation = "    "
    levelIdentation = level > 0 and identation * (level + 1) or ""
    openings = {'list': "[", 'tuple': "(", 'dict': "{"}
    endings = {'list': "]", 'tuple': ")", 'dict': "}"}
    collectionType = type(collection).__name__
    print(collectionType.capitalize())
    print("{}{}".format(levelIdentation, openings[collectionType]))

    if collectionType == "list" or collectionType == "tuple":
        for index, value in enumerate(collection):
            printCollectionContent(openings, level, levelIdentation, identation, index, value)
    elif collectionType == "dict":
        for key, value in collection.items():
            printCollectionContent(openings, level, levelIdentation, identation, key, value)

    print("{}{}".format(levelIdentation, endings[collectionType]))

def lreplace(oldText, newText, subject):
    lastSubstringIndex = subject.rfind(oldText)
    newString = subject[:lastSubstringIndex] + subject[lastSubstringIndex+len(oldText):]
    return newString

def getKeywordFromString(text):
    otherKeywords = {
        'alcaraz-carlos': 'alcaraz-garfia-carlos',
        'kwon-soonwoo': 'kwon-soon-woo',
        'svitolina-elina': 'monfils-elina',
        'mayar-sherif-ahmed-abdul-aziz': 'sherif-mayar',
        'meligeni-alves-felipe': 'meligeni-rodrigues-alves-felipe'
    }
    keyword = text.replace(" ", "-").lower()
    keyword = keyword.replace("'", "-")
    keyword = keyword.replace("(", "")
    keyword = keyword.replace(")", "")

    if keyword in otherKeywords:
        return otherKeywords[keyword]
    else:
        return keyword

def getStringFromKeyword(text):
    string = text.replace("-", " ").title()
    return string

def getSoup(url, headersSoup=None):
    if headersSoup is None:
        headersSoup = {"User-Agent" : "BreakSystem Scraper/1.0"}

    tried = 0

    while tried < 3:
        try:
            response = requests.get(url, headers=headersSoup)
            tried = 3
        except Exception as e:
            tried += 1
            sleep(randint(3, 5))

            if tried == 3:
                print("[ERROR] Connection error for the website {}: {}".format(url, e))
                exit()

    soup = BeautifulSoup(response.content, "lxml")
    return soup
