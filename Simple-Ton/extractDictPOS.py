# extractDictPOS.py
#
# Extract all PoS abbreviations from dictionary
#

from utils import connectMongo
import json

testOutFile = "dictPOS.txt"
dictOutFile = "newDict.txt"



if __name__ == "__main__":

    client = connectMongo()
    db = client['simp']
    collection = db['dictionary']
    wordCount = 0
    posSet = set()
    posDictList = []
    newDict = []

    all_documents = list(collection.find({}))

    # Extract PoS
    for document in all_documents:
        wordCount += 1
        docWord = document['word']
        docDef = document['definition']

        index = docDef.find(')')
        docPOS = docDef[0:index + 1]

        posSet.add(docPOS)

        # Rebuild dictionary
        tmpDict = {"WORD": docWord, "POS": docPOS, "DEF":docDef[index + 1:]}
        newDict.append(tmpDict)
        

        #print(f'{wordCount}: {docWord}: {docPOS}')

    print('-----')
    
    pCnt = 0
    with open(testOutFile, 'w') as f:
        for p in posSet:
            pCnt += 1
            #print(f'{pCnt}: {d}')
            posWordDict = {"POS": p, "WORDS": []}
            posDictList.append(posWordDict)

            f.write(p + '\n')

    f.close()

    # Write newDict to json for later processing
    with open('data.json', 'w') as f:
        #for d in newDict:
        json.dump(newDict, f)
            
    f.close()

    
    

    
    pCnt = 0
#    for key, value in posWordDict.items():
#        pCnt += 1
#        print(f'{pCnt}: {key}: {value}')

    for d in posDictList:
        pCnt += 1
        print(f'{pCnt}: {d}')

        for document in all_documents:

            docWord = document['word']
            docDef = document['definition']

            index = docDef.find(')')
            docPOS = docDef[0:index + 1]
        
            if d['POS'] == docPOS:
                if docWord not in d['WORDS']:
                    d['WORDS'].append(docWord)
        
                    
    pCnt = 0
    for d in posDictList:
        pCnt += 1
        print(f'{pCnt}: {d["POS"]}')
        print(f'{pCnt}: {d["WORDS"]}')
