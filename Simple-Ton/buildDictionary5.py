# buildDictionary4.py
# Build dictionary from raw input.
# 
# New: 8/24/25
# Mod: 11/16/25
#
import os
import sys
import string
from utils import connectMongo
from config import posAbbreviations


def getRawCorpus():
    dataFile = '/home/gary/src/data/rawD.txt'

#    print('Reading input file...')
        
    rows = []
    with open(dataFile, 'r', encoding="latin-1") as f:
        rowCnt = 0
        while (row := f.readline()):
            rowCnt += 1
            rows.append(row)
            
    f.close()
    
    return rows


def preProcessRows(rows):
    newRows = []
    
    for i in range(len(rows)):
        if rows[i].isupper():
            # Option 1
            #if rows[i - 1].isupper():
            #    print('same as above: ', rows[i].strip())
            #else:
            #    words.append('BREAK') # Breaking up lines into word groups
            #    sectionCnt = 1
            
            # Option 2
            newRows.append('BREAK') # Breaking up lines into word groups

        if len(rows[i].rstrip()) > 0:        
            newRows.append(rows[i].rstrip())
        
    return newRows


def buildWordBlocks(newRows):

    wordDefs = []
    tmpWordDef = []

    rowCnt = 0

    for row in newRows:
        rowCnt += 1
        
        if row == 'BREAK':
            if rowCnt > 1:
                wordDefs.append(tmpWordDef)
                tmpWordDef = []
        else:
            tmpWordDef.append(row)


        if rowCnt > 300:
            return wordDefs

    return wordDefs


def buildMongoCollection(wordDefBlocks):
    
    client = connectMongo()
    db = client['simp']
    collection = db['dictionary']
    collection.drop() # Start fresh

    word = ''
    line2 = ''
    posFound = []
    
    Etym = 'Etym'
    unknownWords = []

    totalLineCnt = 1

    for wordDefBlock in wordDefBlocks:
 #       print('----------')
 #       print('totalLineCnt: ', totalLineCnt)
        lineCnt = 0
        defBlock = []
        punctPOS_cont = False
        
        for line in wordDefBlock:
            lineCnt += 1
            if lineCnt == 1:
                word = line
                wordList = line.split(';')
            elif lineCnt == 2:
                
                print('lineCnt == 2: line:')
                print(line)

                if "[" in line:
                    punctPOS_cont = True

                

                """

                # Save original line 2
                line2 = line
                
                index = line.find(Etym)
                if index == -1:
                    print('No Etym:')
                    pLst = line.split(',')
                    p2Lst = pLst[-1].split()
                    if len(p2Lst) > 0:
                        pos2Chk = p2Lst[0].strip()
                    else: # Just pass garbage
                        pos2Chk = line
                    # Attempt to reduce garabge
                    pos2Chk = pos2Chk.replace(";", "").strip()
                else:
                    print('Found Etym:')
                    pLst = line[:index].split(',')                    
                    pos2Chk = pLst[-1].strip()
                    idx = pos2Chk.find(';')
                    if idx != -1:
                        pos2ChkLst = pos2Chk.split()
                        pos2Chk = pos2ChkLst[0].replace(";", "").strip()
                        
                if pos2Chk in wordList:
                    pos2Chk = ''

                print('pos2Chk: ', pos2Chk)

                # Treebank POS does not have a transitive verb tag, so...
                if pos2Chk == 'v.t.':
                    pos2Chk = 'v.'
                    print('Modified pos2Chk for v.t. to v.: ', pos2Chk) 

                try:
                    pos = posAbbreviations[pos2Chk]
                except KeyError:
                    pos = "Unknown"
                    unknownWords.append(wordDefBlock)
                print('pos: ', pos)

                posFound = []
                posFound.append(pos2Chk)
                posFound.append(pos)

                print(posFound)
                """
            else:                    
                defBlock.append(line)
#
#                
#        print('...')        
        pos = posFound
        wordDef = {'wordList': wordList, 'word': word, 'pos': pos, 'line2': line2, 'definition': defBlock}
        x = collection.insert_one(wordDef)
        totalLineCnt += 1        
        
    return unknownWords


if __name__ == "__main__":
    cnt = 1
    rawRows = getRawCorpus()
    newRows = preProcessRows(rawRows)
    wordBlocks = buildWordBlocks(newRows)
#    unknowns = buildMongoCollection(wordDefBlocks)
    print('---------------')
    for i in wordBlocks:
        print(i)
    print("Len wordBlocks: ", len(wordBlocks))
    #print("Len unknowns: ", len(unknowns))
    print("Coda.")

    
    
