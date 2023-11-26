import json
import string
import os
from constants import STOP_WORDS

# TODOS
#  i think i should minimize docIDs by generating my own, so that it will decrease the
#  size , will implement it later

def convertToWords(content):
    # removing puntuation from the content string
    words = ''.join(char for char in content if char not in string.punctuation)
    # converting to lowerCase before spliting the content to the list of words
    words = content.lower().split(' ')
    words = [word for word in words if word not in STOP_WORDS]
    
    return words

def listOfWordsHits(words, docID):
    # this function will take simplified list of content (words), and docID
    # and will make listWords that contains objects of each word
    # with meta info of each word

    listWords = []

    for word in words:
        wordObj = {}
        
        
        freq = 0
        
        for curWord in words:
            if(curWord == word):
                freq += 1
                # by removing repeating words we will increase efficieny
                # because in this way it doesn't need to iterate over again on repeated words
                words.remove(curWord)
        
        # here I am assigning docID to each word of that doc
        # maybe it can be used later for inverted index

        wordObj[word] = freq
        wordObj['docID'] = docID

        listWords.append(wordObj)
    
    return listWords


def createForwardIndex(docsList):
    forwardIndex = []
    for doc in docsList:
        docObj = {}
        metaDataObj = {}
        for key in doc:
            if(key == 'content'):
                # docObj[key] = doc[key]
                words = convertToWords(doc[key])
                # docObj['words'] = words

                docObj['words'] = listOfWordsHits(words, doc['id'])
            else:
                metaDataObj[key] = doc[key]
            docObj["metaData"] = metaDataObj

        forwardIndex.append(docObj)
    

    return forwardIndex

def process_folder(folder_path):
    forward_indexes = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                docs_list = json.load(file)
                forward_index = createForwardIndex(docs_list)
                forward_indexes.extend(forward_index)

    return forward_indexes


forwardIndex = process_folder('newsdata')          

# print(docsList)

file_path = "./forward_index/output3.json"
# Write the list to a JSON file
with open(file_path, 'w') as json_file:
    json.dump(forwardIndex, json_file, indent=2) 

# print(forwardIndex)