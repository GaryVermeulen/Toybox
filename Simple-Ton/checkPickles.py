#
# checkPickles.py
#

import pickle


sDictionary = '/home/gary/src/Simple-Ton/processedData/sDictionary.p'


if __name__ == "__main__":

    
    # Dictionary
    #
    sDict = pickle.load(open(sDictionary, 'rb'))

    print('len sDict: ', len(sDict))
    print('type sDict: ', type(sDict))

    for k in sDict:
        print(k[0])
        print(len(k[1]))

    print(sDict[0][1][0])
        


