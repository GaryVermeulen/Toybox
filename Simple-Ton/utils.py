# utils.py
# Utilities script/module for Simple-Ton
# New: 7/27/25
#
import os
import networkx as nx
import pymongo
import subprocess
import pickle

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

    print(doc)

    client.close()
    return doc


def checkDictionary(inputSentObj):

    wordDef = {}
    rawDict = []
    lineCnt = 0

    if os.path.exists(sDictionary):
        sDict = pickle.load(open(sDictionary, 'rb'))
        print(f'Read {len(sDict)} Lines From {sDictionary} Pickle File.')
    else:
        print(f'{sDictionary} Not Found')

    
    print('now to check the sentence...')
    inputSentObj.printAll()

    wordCount = 1
    for word in inputSentObj.taggedSent:
        print(word)
        print(word[0].capitalize())
        print(word[0][0].capitalize())
        
        for i in sDict:
            #print("i: ", i[0])
            if i[0] == word[0][0].capitalize():
                print(i[0])
                print(type(i))
                for j in i[1]:
                    #print('j: ', j)
                    
                    if j[0] == word[0].capitalize():
                        print('...')
                        print(j[0])
                        print(j[1])
                        
            

    return wordDef



