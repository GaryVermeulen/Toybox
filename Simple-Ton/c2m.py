# c2m.py
# Read contractions.txt and make MongoDB
#
import pymongo
from utils import connectMongo

inputFile = '/home/gary/src/Simple-Ton/inputData/contractions.txt'

def makeContractions():

    cnt = 0
    mdb = connectMongo()
    simpDB = mdb["simp"]
    c = simpDB["contractions"]

    c.drop() # Clean start
    

    try:
        with open(inputFile, 'r') as file:
            for line in file:
                l = line.strip()
                if l[0] != '#':
                    lLst = l.split(':')
                    
                    c.insert_one({'contraction': lLst[0], 'expandedForm': lLst[1]})
                    cnt += 1
        file.close()
                    
                    
    except FileNotFoundError:
        print(f"File {inputFile} not found error.")
    except Exception as e:
        print(f"Exception {e} caught.")


    return cnt

if __name__ == "__main__":


    cnt = makeContractions()

    print(f'{cnt} Contractions read into MongoDB')
