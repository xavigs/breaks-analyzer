def printCollection(collection, level = 0, keysLength=0):
    if isinstance(collection, list):
        print("List")

        for i in range(0, level):
            print "    ",

            for j in range(0, keysLength):
                print " ",

            print "   ",

        print("[")

        for index, item in enumerate(collection):
            for i in range(0, level):
                print "    ",

                for j in range(0, keysLength):
                    print " ",

                print "   ",

            print "    [" + str(index) + "] => ",

            if not isinstance(item, list) and not isinstance(item, tuple) and not isinstance(item, dict):
                print(item)
            else:
                printCollection(item, level + 1, len(str(index)))

        for i in range(0, level):
            print "    ",

            for j in range(0, keysLength):
                print " ",

            print "   ",

        print("]")
    elif isinstance(collection, tuple):
        print("Tuple\n(")
        print(")")
    elif isinstance(collection, dict):
        print("Dict")

        for i in range(0, level):
            print "    ",

            for j in range(0, keysLength):
                print " ",

            print "   ",

        print("{")

        for key, value in collection.items():
            for i in range(0, level):
                print "    ",

                for j in range(0, keysLength):
                    print " ",

                print "   ",

            print "    [" + key + "] => ",

            if not isinstance(value, list) and not isinstance(value, tuple) and not isinstance(value, dict):
                print(value)
            else:
                printCollection(value, level + 1, len(str(index)))

        for i in range(0, level):
            print "    ",

            for j in range(0, keysLength):
                print " ",

            print "   ",

        print("}")

def lreplace(oldText, newText, subject):
    lastSubstringIndex = subject.rfind(oldText)
    newString = subject[:lastSubstringIndex] + subject[lastSubstringIndex+len(oldText):]
    return newString
