def printCollectionContent(openings, level, levelIdentation, identation, key, value):
    print "{}{}[{}] =>".format(levelIdentation, identation, key),

    if type(value).__name__ not in openings:
        print(str(value))
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
    otherKeywords = {'alcaraz-carlos': 'alcaraz-garfia-carlos',
                    'kwon-soonwoo': 'kwon-soon-woo'
    }
    keyword = text.replace(" ", "-").lower()

    if keyword in otherKeywords:
        return otherKeywords[keyword]
    else:
        return keyword