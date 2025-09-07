# buildSimpDict.py
#
# Build a dictionary for Simple-Ton w/UPenn Treebank POS tags
#

import sys
from utils import connectMongo
import json

dictOutFile = "simpDict.txt"

killSwitch = 1

def loadMongoDict():
    # Load existing Mongo dictionary
    client = connectMongo()
    db = client['simp']
    collection = db['dictionary']
    wordCount = 0
    posSet = set()
    posDictList = []
    newDict = []

    all_documents = list(collection.find({}))

    return all_documents


def buildSimpDict(docs):

    newDictList = []

    for doc in docs:
    # Extract out the pieces
        docWord = doc['word']
        docDef = doc['definition']

        index = docDef.find(')')
        docPOS = docDef[0:index + 1]

        docTags = pos2Tags(docPOS)

        if "UNK" in docTags or "LT4" in docTags: # Retain only known tags
            continue

        tmpDict = {"WORD": docWord, "POS": docPOS, "TAG": docTags, "DEF": docDef[index + 1:]}

        newDictList.append(tmpDict)

    return newDictList


def pos2Tags(pos):
    # There are 304 dictionary unique PoS definitions
    # within the 187665 entries, see dictPOS.txt
    # This is a work-in-process
    docTags = []


    
    #print(len(pos), pos)
    # For now simple mapping
    if len(pos) == 4: # Assuming (n.)
        #print(pos[1], pos[2])
        if (pos[1] == 'n') and (pos[2] == '.'):
            docTags.append("NN")
        elif (pos[1] == 'v') and (pos[2] == '.'):
            docTags.append("VB")
        elif (pos[1] == 'a') and (pos[2] == '.'):
            docTags.append("JJ")
            
        else:
            docTags.append("UNK")
    else:
        docTags.append("LT4")
    
    return docTags


if __name__ == "__main__":

    cnt = 0
    docs = loadMongoDict()

    print(len(docs))

    for d in docs:
        cnt +=1
        print(d)
        if cnt >= 100:
            break
            #sys.exit("TEMP STOP")

    newDictList = buildSimpDict(docs)
    
    # Write new dict to json for later processing
    with open('data.json', 'w') as f:
        #for d in newDict:
        json.dump(newDictList, f)
            
    f.close()
    
