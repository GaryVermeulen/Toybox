# buildDictionary.py
# Build dictionary from raw input.
# 
# New: 8/24/25
#
import os
import sys
import string
from utils import connectMongo, readDictionary


def getRawCorpus():
    # Read the raw corpus file(s)
    dictionary = []
    #corpusStr = ''
    #progPath = os.getcwd()
    #dataPath = progPath + '/inputCorpora'
    dataPath = '/home/gary/data/csvDictionary'
    dirList = os.listdir(dataPath)

    translator = str.maketrans('', '', string.punctuation)

    print('Reading input file(s)...')

    # Read corpus input
    # Debug stop
    ##dStop = 0
    for inFile in dirList:
        print('inFile: ', inFile)
        
        rows = []
        with open(dataPath + '/' + inFile, 'r', encoding="latin-1") as f:
            while (line := f.readline()):
                if len(line) > 1:
                    word, sep, definition = line.partition('(')
                    # Clean word
                    word = word.strip()
                    word = word.translate(translator)
                    # Build word/definition tuple
                    #   Glue back on (
                    #   Strip last " and \n char's
                    definition = sep + definition
                    definition = definition[:-2]
                    rows.append((word, definition))
                    """
                    dStop += 1
                    if dStop > 5:
                        sys.exit("dStop reached.")
                    """
        f.close()

        #bookName = inFile[: -4]
        #corpora.append((bookName, corpusStr))
        #corpusStr = ''
        #
        #corpora.append((bookName, rows))
        #
        for r in rows:
            dictionary.append(r)
        

    return dictionary


def buildMongoCollection(dictionary):
    client = connectMongo()
    db = client['simp']
    collection = db['dictionary']
    collection.drop() # Start fresh

    for line in dictionary:
        word = line[0]
        definition = line[1]

        wordDef = {'word': line[0], 'definition': line[1]}

        x = collection.insert_one(wordDef)


    return "FIN"


if __name__ == "__main__":
    cnt = 1
    dictionary = getRawCorpus()
    d = buildMongoCollection(dictionary)

    """
    print('----- c:')
    print(type(c))
    print(len(c))
    for line in c:
        print(f'{cnt}: >{line}<')
        cnt += 1

        if cnt >= 100:
            sys.exit("Limit reached.")

    """
    
