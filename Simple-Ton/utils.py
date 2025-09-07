# utils.py
# Utilities script/module for Simple-Ton
# New: 7/27/25
#
import os
import networkx as nx
import pymongo
import subprocess
import pickle
from nltk.corpus import wordnet as wn
from config import nnAll, vbAll, jjAll, rbAll, prpAll

sDictionary = '/home/gary/src/Simple-Ton/processedData/sDictionary.p'


def connectMongo():
    # Connect to local copy of MongoDB
    c = None

    try:
        c = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    # Make sure MongDB is running!
    # No matted what, I cannot catch:
    # pymongo.errors.ServerSelectionTimeoutError
    #
    #except ConnectionFailure as e:
    #    print(f"MongoDB connection failed: {e}")
    #except pymongo.errors.ServerSelectionTimeoutError as e:
    #    print(f"MongoDB connection timeout: {e}")
    except (ValueError, TypeError) as e:
        print(f"MongoDB error: {e}")
    return c


def getContraction(w):

    client = connectMongo()
    db = client['simp']
    collection = db['contractions']

    if w[0] == "I" and w[1] =="'": # Seperate I for is
        doc = collection.find_one({'contraction': w})
    else:
        doc = collection.find_one({'contraction': w.lower()})

    print("doc:")
    print(doc)

    if doc:
        expForm = doc['expandedForm']
        print('expForm: ', expForm)
    else:
        expForm = None
        print('expForm not found for w: ', w.lower())

    return expForm


def getRoot(G):
    for node, indegree in G.in_degree():
        if indegree == 0:
            # if you'r graph is a tree you only have one root so you don't need to check every node, once you find it it's done
            return node
    return None


def searchKG(G, inputSentObj):

    for word in inputSentObj.taggedSent:
        if word[1] in ['NN', 'NNP']:
            try:
                ancestorsFound = nx.ancestors(G, word[0])
            except nx.NetworkXError as e:
                #print(f"NetworkX Exception caught: {e} ")
                #print("Just assume the error is not in graph: ", word)
                #
                inputSentObj.data.append({"Unknown": word})
                
            else:
                #print("Ancestors: ")
                #print(ancestorsFound)
                # ancestorsFound does not contain current node (word), but
                # shortest_path does...
                # Sorted
                a = nx.shortest_path(G, source=getRoot(G), target=word[0])
                k = {"Known": word, "Ancestors": a}
                #print("Childern:")
                c = nx.descendants(G, word[0])
                if len(c) > 0:
                    #print(c)
                    k["Children"] = c
                inputSentObj.data.append(k)

    return inputSentObj


def searchMongoWiki(u):
    client = connectMongo()
    db = client['simp']
    collection = db['wikiData']
    
    doc = collection.find_one({"title": u}) 

    #print(doc)

    client.close()
    return doc


def addNaiveG(s):
    x = None
    print('addNaiveG...')
    client = connectMongo()
    db = client['simp']
    collection = db['naiveGrammar']

    x = collection.insert_one(s)
    print(f"Inserted ID: {x.inserted_id}")

    if x == None:
        return None

    return s['taggedSent']


def checkNaiveG(inputS):
    x = None
    print('checkNaiveG...')
    client = connectMongo()
    db = client['simp']
    collection = db['naiveGrammar']

    x = collection.find_one({'rawSent': inputS})

    return x   


def naiveGrammar(inputS, s1, s2):
    x = None

    print('---------- naiveGrammar')
    print('inputS: ')
    print(inputS)
    
    x = checkNaiveG(inputS)

#    print('checkNaiveG returned (x): ', x)
    if x:
        print(x['taggedSent'])
        return x['taggedSent']
    
    print('s1:')
    print(s1)
    print('s2:')
    print(s2)
    ans = input('Enter sentnce number with best grammar <1/2>: ')
    #print(type(ans))
    #print(ans)
    if ans not in ['1', '2']:
        return None

    if ans == '1':
        # Add s1 to naiveGrammar DB
        s = {'rawSent': inputS, 'taggedSent': s1}
        #s = {inputS: s1}
        #print(ans, s)
        x = addNaiveG(s)
    elif ans == '2':
        # Add s2 to naiveGrammar DB
        s = {'rawSent': inputS, 'taggedSent': s2}
        #s = {inputS: s2}
        #print(ans, s)
        x = addNaiveG(s)

    #print("x: ", x)

    return x


def checkPickleDictionary(inputSentObj):

    wordDef = {}
    rawDict = []
    lineCnt = 0
    wordFound = False

    if os.path.exists(sDictionary):
        sDict = pickle.load(open(sDictionary, 'rb'))
        print(f'Read {len(sDict)} Lines From {sDictionary} Pickle File.')
    else:
        print(f'{sDictionary} Not Found')

    
    print('now to check the sentence...')
    inputSentObj.printAll()
    print('-----------')

    wordCount = 1
    for word in inputSentObj.taggedSent:
        print("word:  ", word)
        print('   ', word[0].capitalize())
        print('      ', word[0][0].capitalize())
        print('.........')
        for i in sDict:
            print("i[0]: ", i[0])
            if i[0] == word[0][0].capitalize(): # 1st of word to match dictionary section
                print("==i[0]: ", i[0])
                print("  type i: ", type(i))
                print('  ---')
                for j in i[1]: # Grid through dictionary section for the word
                    #print('j: ', j)
                    
                    if j[0] == word[0].capitalize(): # Word matches dictionary entry(ies)
                        print('...')
                        print("j[0]: ", j[0])
                        print("j[1]: ", j[1])
                        print("type j: ", type(j))
    
    return wordDef


def readPickleDictionary(word):

    wordDef = []

    print('.----------')
    print('word: ', word)
    capWord = word.capitalize()
    print('capWord: ', capWord)
    
    if os.path.exists(sDictionary):
        sDictList = pickle.load(open(sDictionary, 'rb'))
        print(f'Read {len(sDictList)} Lines From {sDictionary} Pickle File.')
    else:
        print(f'{sDictionary} Not Found')

    firstLetter = word[0].capitalize()
    print("firstLetter: ", firstLetter)

    for section in sDictList:
        if section[0] == firstLetter:
            print(section[0], firstLetter)
            #print(section)
            
            for secWord in section[1]:
                #print('words: ', words)
                if secWord[0] == capWord:
                    print(secWord[0], capWord)
                    print(secWord[1])
                    print('...')
                    wordDef.append((secWord[0], secWord[1]))
            
    
    print('----------.')
    return wordDef


def readMongoDictionary(word):

    wordDef = []
    client = connectMongo()
    db = client['simp']
    collection = db['dictionary']
    docCount = 0
    docMatchCount = 0


    #print('---------- readMongoDictionary start')
    #print('word: ', word)
    
    capWord = word[0].capitalize()
    #print('capWord: ', capWord)

    query = {"word": capWord}


    docs = collection.find(query)

    #print("type docs: ", type(docs))

    for doc in docs:
        docCount += 1
        #print('doc: ')
        #print('doc["word"]: ', doc['word'])
        #print('doc["pos"]: ', doc['pos'])
        #print('doc["definition"]: ', doc["definition"])

        # Does doc[pos] match word[1]?
        docPOSMatch = checkDocPOS(doc['pos'], word[1])
        if docPOSMatch:
            docMatchCount += 1
            #print("MATCH")
            wordDef.append(doc)
        
    #print(f"Found {docCount} documents and {docMatchCount} possible matches")
    #print('---------- readMongoDictionary end')
    return wordDef

def checkMongoDictionary(sentObj):

    wordDef = []
    sentWordDefs = []

    print("   checkMongoDictionary--start: ")
    #print("   taggedSent: ", sentObj.taggedSent)

    for word in sentObj.taggedSent:

        #print("   word: ", word)
        #print("   word[0]: ", word[0])

        wordDef = readMongoDictionary(word)
        sentWordDefs.append((word, wordDef))

        print(f"   Found {len(wordDef)} possibe definitions for {word}")

    print("   checkMongoDictionary--end: ")
    return sentWordDefs


def checkWordNet(sentObj):

    wordDefs = []

    #print("     checkWordNet--start: ")
    #print("     taggedSent: ", sentObj.taggedSent)
    
    for w in sentObj.taggedSent:
        #print('w: ', w)
        #s = wn.synsets(w[0])
        #print('s: ', s)

        # Try to reduce synsets by matching with POS tag
        # First map POS to wordnet POS
        if w[1] in nnAll:
            s = wn.synsets(w[0], pos=wn.NOUN)
        elif w[1] in vbAll:
            s = wn.synsets(w[0], pos=wn.VERB)
        elif w[1] in jjAll:
            s = wn.synsets(w[0], pos=wn.ADJ)
        elif w[1] in rbAll:
            s = wn.synsets(w[0], pos=wn.ADV)
        else:
            s = wn.synsets(w[0])
            print('Could not reduce synset for: ', w)
            print('s: ', s)

        # Second reduce by eliminating synset word(s) that do match w
        for s0 in s:
            #print('s0:')
            #print(s0)

            #print('s0.name():')
            #print(s0.name())

            nameList = s0.name().split('.')
            #print(nameList[0])

            if nameList[0] == w[0]:
                wordDefs.append((w, s0))
    
    print("     checkWordNet--end: ")
    return wordDefs


def checkDocPOS(doc, word):

    docMatch = ''

    #print('  checkDocPOS start')

    #print('  doc:    ', doc)
    #print('  word:   ', word)

    doc = doc.replace('(', '')
    doc = doc.replace(')', '')

    doc = doc.replace('/', '')
    doc = doc.replace('&', '')
    doc = doc.replace(',', '')

    docList = doc.split('.')
    #print('  docList: ', docList)

    # Just simple mapping for now
    if docList[0] == 'n' and word in nnAll:
        return True
    elif docList[0] == 'v' and word in vbAll:
        return True
    elif (docList[0] == 'a' or docList[0] == 'adj') and word in jjAll:
        return True
    elif docList[0] == 'superl' and word in jjAll:
        return True
    elif docList[0] == 'adv' and word in rbAll:
        return True
    elif docList[0] == 'definite article' and word == 'DT':
        return True
    elif docList[0] == 'prep' and word == 'IN':
        return True
    elif docList[0] == 'pron' and word in prpAll:
        return True

    #print('  checkDocPOS end')
    return False


