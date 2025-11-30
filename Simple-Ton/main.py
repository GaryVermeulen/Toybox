# main.py
# Single-pass main script for Simple-Ton 2.0
# New: 7/25/25; Mod: 11/27/25
#

import sys
from simpletonKG import loadKG, plotG
from processInput import processUserInput
from utils import checkWordNet, check4TaggingErrors, checkMongoDictionary, searchKG #, searchMongoWiki


def collectData(inputSentObj):

    print('---- inputSentObj:')
    inputSentObj.printAll()

    print('---- check4TaggingErrors:')
    check4TaggingErrors(inputSentObj)
    print('---- check4TaggingErrors returned:')            
    inputSentObj.printAll()

    print('---- start searchKB:')
    searchKG(kgTuple, inputSentObj)
    print('---- searchKB returned:')
    inputSentObj.printAll()

    print('---- checkWordNet:')
    checkWordNet(inputSentObj)
    print('---- checkWordNet returned:')
    inputSentObj.printAll()
        
    print('---- checkMongoDictionary:')
    checkMongoDictionary(inputSentObj)
    print('---- checkMongoDictionary returned:')
    inputSentObj.printAll()

    return inputSentObj


if __name__ == "__main__":
    
    # Build/load KG
    kgTuple = loadKG()

    for kg in kgTuple:
        plotG(kg)

    # Get input from user, expand contractions, and POS tag
    inputSentObj = processUserInput()
    
    if inputSentObj != None:

        collectData(inputSentObj)
        
        print('---------------- Full Results:')
        inputSentObj.printFull()
    else:
        print("No input.")
    print('----------------')
    print(' main end')
    
