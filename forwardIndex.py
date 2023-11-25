import json
import string

# TODOS
#  i think i should minimize docIDs by generating my own, so that it will decrease the
#  size , will implement it later

def convertToWords(content):
    # removing puntuation from the content string
    words = ''.join(char for char in content if char not in string.punctuation)
    # converting to lowerCase before spliting the content to the list of words
    words = content.lower().split(' ')
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
        for key in doc:
            if(key == 'content'):
                # docObj[key] = doc[key]
                words = convertToWords(doc[key])
                # docObj['words'] = words

                docObj['words'] = listOfWordsHits(words, doc['id'])
            else:
                docObj[key] = doc[key]
    
    forwardIndex.append(docObj)

    return forwardIndex




        

with open('./nela-gt-2022/newsdata/369news.json', 'r') as file:
    docsList = json.load(file)

    forwardIndex = createForwardIndex(docsList)

    

    # forwardIndex will look like this:
    # forwardIndex = [
    #     {
    #         id: docId,
    #         title: docTitle,
    #         date: docDate,
    #         url : links,
    #         ...,
    #         words: [
    #             {
    #                 word: docID,
    #                 freq : numberOftimesOccured 
    #              },
    #             {
    #               ...
    #             }
    #         ] 
    #     },
    #     {........}, 
    # ]
            

            

# print(docsList)
print(forwardIndex)