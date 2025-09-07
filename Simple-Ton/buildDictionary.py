# buildDictionary.py
# Build dictionary from raw input.
# New: 8/3/25
# Rev: 8/24/25; Also create MongoDB
#
import os
import sys
#import csv
import string
import pickle
from utils import connectMongo, readDictionary

sDictionary = '/home/gary/src/Simple-Ton/processedData/sDictionary.p'


def getRawCorpus():
    # Read the raw corpus file(s)
    corpora = []
    corpusStr = ''
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

        bookName = inFile[: -4]
        #corpora.append((bookName, corpusStr))
        corpora.append((bookName, rows))
        corpusStr = ''

    return corpora


if __name__ == "__main__":
    
    c = getRawCorpus()

    print('----- c:')
    print(type(c))
    print(len(c))
    for i in c:
        print('i[0] (in c): ', i[0])

    print('----- c[0]:')
    print(type(c[0]))
    print(len(c[0]))
    
    print('-----len, type, c[0][0]:')
    print(len(c[0][1]))
    print(type(c[0][1]))
    print(c[0][0])
    
    print('----- len & type c[0][1]:')
    print(len(c[0][1]))
    print(type(c[0][1]))

    print('----- len & type c[0][1][0]:')
    print(len(c[0][1][0]))
    print(type(c[0][1][0]))
    print(c[0][1][0])
    """
    for i in c[0][1]:
        
        if i != '':
            print(len(i[1]))
            print(i)
    
    """

    print('Saving Dictionary data to pickle...')
    with open(sDictionary, "wb") as f:
        pickle.dump(c, f)

    testWord = "goat"

    wordDef = readDictionary(testWord)
    print(f'-------- {testWord}: wordDef:')
    print(wordDef)
    
