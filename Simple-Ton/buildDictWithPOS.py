# buildDictWithPOS.py
#
# Build a dictionary with POS tags using NTLK
#

import sys
import nltk
from nltk.tokenize import word_tokenize
from utils import connectMongo

testOutFile = "dictPOS.txt"



if __name__ == "__main__":

    client = connectMongo()
    db = client['simp']
    collection = db['dictionary']
    wordCount = 0
    simpDict = {}
    dictList = []

    all_documents = list(collection.find({}))

    # Build simple dictionary 
    for document in all_documents:
        wordCount += 1
        docWord = document['word']
        docDef = document['definition']

        # Strip off org pos
        index = docDef.find(')')
        docDef = docDef[index + 1:]

        simpDict[docWord] = docDef

    pos_tagged_dictionary = {}
    for word, definition in simpDict.items():
        word_tokens = word_tokenize(word)
        # Apply POS tagging
        tagged_word = nltk.pos_tag(word_tokens)
        # Store the tagged word (e.g., just the word and its main tag)
        if tagged_word:
            #pos_tagged_dictionary[word] = tagged_word[0][1] # Get the tag of the first token
            #pos_tagged_dictionary['Definition'] = definition
            tmpDict = {"WORD": word, "TAG": tagged_word[0][1], "DEF": definition}
            dictList.append(tmpDict)

    # Dump what we have
    wordCount = 0
    #for key, value in simpDict.items():
    #for key, value in pos_tagged_dictionary.items():
    #    wordCount += 1
    #    print(f'{wordCount}: {key}: {value}')
    #
    for i in dictList:
        wordCount += 1
        print(i)
        if wordCount >= 100:
            sys.exit("STOP NOW")

