# utils.py
# Utilities script/module for Simple-Ton
# New: 7/27/25; Mod: 11/28/25
#
import os
import networkx as nx
import pymongo
import subprocess
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from config import nnAll, vbAll, jjAll, rbAll, prpAll



def connectMongo():
    # Connect to local copy of MongoDB
    c = None

    try:
        c = pymongo.MongoClient("mongodb://10.0.0.30:27017")
    #    c = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    # Make sure MongDB is running!
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


def searchKG(kgTuple, inputSentObj):

    for word in inputSentObj.taggedSent:
        
        if word[1] in ['NN', 'NNP']:
            for kg in kgTuple:
                try:
                    ancestorsFound = nx.ancestors(kg, word[0])
                except nx.NetworkXError as e:
                    #print(f"NetworkX Exception caught: {e} ")
                    #print("Just assume the error is not in graph: ", word)
                    #
                    inputSentObj.kgData.append({"Unknown": word, "UnknownIn": kg.name})
                
                else:
                    #print("Ancestors: ")
                    #print(ancestorsFound)
                    # ancestorsFound does not contain current node (word), but
                    # shortest_path does...
                    # Sorted
                    a = nx.shortest_path(kg, source=getRoot(kg), target=word[0])
                    k = {"Known": word, "KnownIn": kg.name, "Ancestors": a}
                    #print("Childern:")
                    c = nx.descendants(kg, word[0])
                    if len(c) > 0:
                        #print(c)
                        k["Children"] = c
                    inputSentObj.kgData.append(k)
                    
    return inputSentObj

"""
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
"""

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


def readMongoDictionary(word):

    wordDef = []
    client = connectMongo()
    db = client['simp']
    collection = db['dictionary']
    docCount = 0
    docMatchCount = 0


    print('---------- readMongoDictionary start')
    print('word: ', word)
    
    #capWord = word[0].capitalize()
    #print('capWord: ', capWord)

    upWord = word[0].upper()

    #query = {"word": capWord}
    query = {"word": upWord}


    docs = collection.find(query)

    #print("type docs: ", type(docs))

    for doc in docs:
        docCount += 1
        #print('doc: ')
        #print('doc["wordList"]: ', doc['wordList'])
        #print('doc["word"]: ', doc['word'])
        #print('doc["pos"]: ', doc['pos'])
        #print('doc["line2"]: ', doc['line2'])
        #print('doc["definition"]: ', doc["definition"])

        # Does doc[pos] match word[1]?
        docPOSMatch = checkDocPOS(doc['pos'], word)
        if docPOSMatch:
            docMatchCount += 1
            #print("MATCH")
            wordDef.append(doc)
        
    print(f"Found {docCount} documents and {docMatchCount} possible matches")
    print('---------- readMongoDictionary end')
    return wordDef


def checkMongoDictionary(sentObj):

    wordDef = []
    sentWordDefs = []

    print(">>>>   checkMongoDictionary--start: ")
    #print("   taggedSent: ", sentObj.taggedSent)

    for word in sentObj.taggedSent:

        #print("   word: ", word)
        #print("   word[0]: ", word[0])

        wordDef = readMongoDictionary(word)
        #print("wordDef: ", wordDef)
        sentWordDefs.append((word, wordDef))

        #print(f"   Found {len(wordDef)} possibe definitions for {word}")

    #print(">>>> sentWordDefs:")
    #print(sentWordDefs)
    sentObj.dictionaryData = sentWordDefs
    print(">>>>   checkMongoDictionary--end: ")
    #return sentWordDefs
    return sentObj


def checkWordNet(sentObj):

    wordDefs = []
    synsetsFound = []
    wordMatch = False
    lemma = ''

    #print("     checkWordNet--start: ")
    #print("     taggedSent: ", sentObj.taggedSent)
    
    for w in sentObj.taggedSent:
        wordMatch = False
        synsetsFound = []
        #print('=' * 20)
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
            #print('s: ', s)
    
        # Second reduce by eliminating synset word(s) that do match w
        for s0 in s:
            #print('s0:')
            #print(s0)

            #print('s0.name():')
            #print(s0.name())

            #nameList = s0.name().split('.')
            
            #print("nameList: ", nameList)

            #if nameList[0] == w[0]:
            if s0.pos == w[0]:
                #wordDefs.append((w, s0))
                synsetsFound.append(s0)
                wordMatch = True
            #else:
            #    print(f"NO MATCH: {nameList} and {w}")

        if not wordMatch:
            #print("LOOKING FOR LEMMA")
            lemmatizer = WordNetLemmatizer()
            if w[1] in nnAll:
                lemma = lemmatizer.lemmatize(w[0], pos=wn.NOUN)
                #print(f"The lemma of {w[0]} is: {lemma}")
                s = wn.synsets(lemma, pos=wn.NOUN)
                synsetsFound.append(s)
            elif w[1] in vbAll:
                lemma = lemmatizer.lemmatize(w[0], pos=wn.VERB)
                #print(f"The lemma of {w[0]} is: {lemma}")
                s = wn.synsets(lemma, pos=wn.VERB)
                synsetsFound.append(s)
            elif w[1] in jjAll:
                lemma = lemmatizer.lemmatize(w[0], pos=wn.ADJ)
                #print(f"The lemma of {w[0]} is: {lemma}")
                s = wn.synsets(lemma, pos=wn.ADJ)
                synsetsFound.append(s)
            elif w[1] in rbAll:
                lemma = lemmatizer.lemmatize(w[0], pos=wn.ADV)
                #print(f"The lemma of {w[0]} is: {lemma}")
                s = wn.synsets(lemma, pos=wn.ADV)
                synsetsFound.append(s)
            else:
                print(f"{w[1]} of {w} not defined.")
                s = wn.synsets(w[0])
                #print('Could not reduce synset for: ', w)
            """
            for s0 in s:
                nameList = s0.name().split('.')
            
                print("nameList: ", nameList)

                if nameList[0] == w[0]:
                    #wordDefs.append((w, s0))
                    synsetsFound.append(s0)
                else:
                    print(f"NO LEMMA FOUND: {nameList} and {w}")
            """
        print('First synset def of: ', w)
        print(synsetsFound)
        print('---')
        if len(synsetsFound) > 0:
            if len(synsetsFound[0]) > 0:
                print(synsetsFound[0][0].definition())
                wordDefs.append((w, synsetsFound, synsetsFound[0][0].definition()))
        else:
            wordDefs.append((w, synsetsFound, 'UNK?'))

        

                
    #print('wordDefs:')
    #print(wordDefs)
    sentObj.synsets = wordDefs
    print("     checkWordNet--end: ")
    #return wordDefs
    return sentObj


def check4TaggingErrors(sentObj):

    taggingErrors = []
    allSynsetPOS = []
    chkPOS = ''

    print("     check4TaggingErrors--start: ")
    print("     taggedSent: ", sentObj.taggedSent)

    for word in sentObj.taggedSent:
        #print('-----')
        #print('word: ', word)
        s = wn.synsets(word[0])
        allSynsetPOS = []
        #print(s)
        pTag = False
        for synset in s:
            #print('synset: ', synset)
            #print(type(synset))
            #print(synset.pos())
            allSynsetPOS.append(synset.pos())
            
            if synset.pos() == 'n':
                chkPOS = nnAll
                
            elif synset.pos() == 'v':
                chkPOS = vbAll
            elif synset.pos() == 'a':
                chkPOS = jjAll
            elif synset.pos() == 'r':
                chkPOS = rbAll
            elif synset.pos() == 's':
                chkPOS = jjAll
            else:
                chkPOS = 'UNKPOS'
                
            if word[1] in chkPOS:
                #print("Possible correct tag", word[1], chkPOS)
                pTag = True
                
        if not pTag:
            print("Possible tagging error with: ", word, allSynsetPOS)
            taggingErrors.append((word, allSynsetPOS))

    print("     check4TaggingErrors--end: ")
    
    sentObj.taggingErrors = taggingErrors
    
    return sentObj


def checkDocPOS(doc, word):

    docMatch = ''

    #print('  checkDocPOS start')

    #print('  doc:    ', doc)
    #print('  word:   ', word)

    
    # Old function
    #doc = doc.replace('(', '')
    #doc = doc.replace(')', '')
    #
    #doc = doc.replace('/', '')
    #doc = doc.replace('&', '')
    #doc = doc.replace(',', '')
    #
    #docList = doc.split('.')
    #print('  docList: ', docList)
    #
    # Just simple mapping for now
    #if docList[0] == 'n' and word in nnAll:
    #    return True
    #elif docList[0] == 'v' and word in vbAll:
    #    return True
    #elif (docList[0] == 'a' or docList[0] == 'adj.') and word in jjAll:
    #    return True
    #elif docList[0] == 'superl' and word in jjAll:
    #    return True
    #elif docList[0] == 'adv' and word in rbAll:
    #    return True
    #elif docList[0] == 'definite article' and word == 'DT':
    #    return True
    #elif docList[0] == 'prep' and word == 'IN':
    #    return True
    #elif docList[0] == 'pron' and word in prpAll:
    #    return True

    
    # Still, Just simple mapping for now...
    if doc[1] == word[1] and word[1] in nnAll:
        #print('  checkDocPOS end, n')
        return True
    elif doc[1] == word[1] and word[1] in vbAll:
        #print('  checkDocPOS end, v')
        return True
    
    #elif (dictPOS == 'a' or dictPOS == 'adj') and word in jjAll:
    #    print('  checkDocPOS end, a or adj')
    #    return True
    #elif dictPOS == 'superl' and word in jjAll:
    #    print('  checkDocPOS end, superl')
    #    return True
    #elif dictPOS == 'adv' and word in rbAll:
    #    print('  checkDocPOS end, adv')
    #    return True
    #elif dictPOS == 'definite article' and word == 'DT':
    #    print('  checkDocPOS end, definite article')
    #    return True
    #elif dictPOS == 'prep' and word == 'IN':
    #    print('  checkDocPOS end, prep')
    #    return True
    #elif dictPOS == 'pron' and word in prpAll:
    #    print('  checkDocPOS end, propn')
    #    return True


    #print('  checkDocPOS end, no match')
    return False


