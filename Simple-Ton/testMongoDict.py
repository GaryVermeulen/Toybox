from utils import connectMongo

word = 'dog'
wordDef = []
client = connectMongo()
db = client['simp']
collection = db['dictionary']



print('.----------')
print('word: ', word)
capWord = word.capitalize()
print('capWord: ', capWord)


docs = collection.find({'word': capWord})

for doc in docs:
    print(doc)

print(docs)
