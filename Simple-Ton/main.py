# main.py
# Single-pass main script for Simple-Ton 2.0
# New: 7/25/25; Mod: 11/27/25
#

import sys
from simpletonKG import loadKG
from simpletonKG import plotG
from processInput import processUserInput
from utils import checkWordNet, checkMongoDictionary, searchKG, searchMongoWiki


def getUnknowns(inputSentObj):
    unknowns = []
    for d in inputSentObj.data:
        if "Unknown" in d:
            unknowns.append(d["Unknown"])         
    
    return unknowns

if __name__ == "__main__":

    docs = []

    
    # Build/load KG
    kgTuple = loadKG()

    #plotG(LTG)
    #plotG(nLTG)

    # Get input from user, expand contractions, and POS tag
    inputSentObj = processUserInput()
    
    if inputSentObj != None:
        print('---- inputSentObj:')
        inputSentObj.printAll()

        #sys.exit("Debug Stop/exit...")
        
        print('---- checkMongoDictionary:')
        #mongoDefs = checkMongoDictionary(inputSentObj)
        checkMongoDictionary(inputSentObj)
        print('---- checkMongoDictionary returned:')
        #for d in mongoDefs:
        #    print("d: ")
        #    print(d)
        inputSentObj.printAll()

        print('---- checkWordNet:')
        print('---- inputSentObj:')
        inputSentObj.printAll()
        #synsets = checkWordNet(inputSentObj)
        checkWordNet(inputSentObj)
        print('---- checkWordNet returned:')
        #for synset in synsets:
        #    print('synset:')
        #    print(synset)
        inputSentObj.printAll()

        print('------------')
        print(inputSentObj.rawSent)
        #sys.exit("Debug Stop/exit...")
        
        print('---- start searchKB:')
        searchKG(kgTuple, inputSentObj)
        print('---- afer searchKB:')
        inputSentObj.printAll()
        
        #print('---- start getUnknowns:')
        #unk = getUnknowns(inputSentObj)
        #for u in unk:
        #    print("u: ", u)
        #    doc = searchMongoWiki(u[0])
        #    docs.append(doc)
        #    
        #for d in docs:
        #    print(d)
        
    print('------------')
    print(' main end')
    
