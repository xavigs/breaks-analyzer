def printCollection(collection, level = 0, keysLength=0):
    if isinstance(collection, list):
        print("List")

        for i in range(0, level):
            print("    ", end="")

            for j in range(0, keysLength):
                print(" ", end="")

            print("   ", end="")

        print("[")

        for index, item in enumerate(collection):
            for i in range(0, level):
                print("    ", end="")

                for j in range(0, keysLength):
                    print(" ", end="")

                print("   ", end="")

            print("    [" + str(index) + "] => ", end="")

            if not isinstance(item, list) and not isinstance(item, tuple) and not isinstance(item, dict):
                print(item)
            else:
                printCollection(item, level + 1, len(str(index)))

        for i in range(0, level):
            print("    ", end="")

            for j in range(0, keysLength):
                print(" ", end="")

            print("   ", end="")

        print("]")
    elif isinstance(collection, tuple):
        print("Tuple\n(")
        print(")")
    elif isinstance(collection, dict):
        print("Dict")

        for i in range(0, level):
            print("    ", end="")

            for j in range(0, keysLength):
                print(" ", end="")

            print("   ", end="")

        print("{")

        for key, value in collection.items():
            for i in range(0, level):
                print("    ", end="")

                for j in range(0, keysLength):
                    print(" ", end="")

                print("   ", end="")

            print("    [" + key + "] => ", end="")

            if not isinstance(value, list) and not isinstance(value, tuple) and not isinstance(value, dict):
                print(value)
            else:
                printCollection(value, level + 1, len(str(index)))

        for i in range(0, level):
            print("    ", end="")

            for j in range(0, keysLength):
                print(" ", end="")

            print("   ", end="")

        print("}")

def lreplace(oldText, newText, subject):
    lastSubstringIndex = subject.rfind(oldText)
    newString = subject[:lastSubstringIndex] + subject[lastSubstringIndex+len(oldText):]
    return newString
