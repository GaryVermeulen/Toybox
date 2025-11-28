# testWordNet.py
# Quick and dirty WordNet word test
#
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from config import nnAll, vbAll, jjAll, rbAll, prpAll

lemmatizer = WordNetLemmatizer()
word = ('ran', 'VBD')

print("START: testWordNet: word: ", word)

if word[1] in nnAll:
    s = wn.synsets(word[0], pos=wn.NOUN)
elif word[1] in vbAll:
    s = wn.synsets(word[0], pos=wn.VERB)
elif word[1] in jjAll:
    s = wn.synsets(word[0], pos=wn.ADJ)
elif word[1] in rbAll:
    s = wn.synsets(word[0], pos=wn.ADV)
else:
    s = wn.synsets(word[0])
    print('Could not reduce synset for: ', word)
    print('s: ', s)

# Second reduce by eliminating synset word(s) that do match w
for s0 in s:
    #print('s0:')
    #print(s0)

    #print('s0.name():')
    #print(s0.name())

    nameList = s0.name().split('.')
    print("nameList:")
    print(nameList)

print("Word Tense Check:", word)

lemma = lemmatizer.lemmatize(word[0], pos=wn.VERB)
print(f"The lemma of {word[0]} is: {lemma}")



print("END: testWordNet.")
