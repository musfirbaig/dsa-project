import json
import string

from constants import STOP_WORDS

# TODOS
#  i think i should minimize docIDs by generating my own, so that it will decrease the
#  size , will implement it later

def convertToWords(content):
    """
    this function will take a string of large content as input
    and return list of lowercase words (it will exclude stop words)
    """

    # removing puntuation from the content string
    words = ''.join(char for char in content if char not in string.punctuation)
    # converting to lowerCase before spliting the content to the list of words
    words = content.lower().split(' ')
    words = [word for word in words if word not in STOP_WORDS]

    return words

# def listOfWordsHits(words, docID):
def listOfWordsHits(words):
    """
    INPUT: list of words and docID,
    it will map each word with its freq & docID and return
    return list of Objects containing word: freq and docID: docID
    """
    # this function will take simplified list of content (words), and docID
    # and will make listWords that contains objects of each word
    # with meta info of each word

    # listWords = []

    wordsObject = {}

    for index, word in enumerate(words):
        # whole structure is redefining as below
        # wordsObject = {"word" : {freq: "freq", pos: [list of positions in word list]}, "word2": ..... }

        if wordsObject.get(word) is not None:
            wordObject = wordsObject[word]
            wordObject["freq"] += 1

            # as pos is storing set of positions as its value
            # cannot use set as json have difficulty in parsing 
            # wordObject["pos"].add(index)

            wordObject["pos"].append(index)

        else:

            # if the word doesnt exist as a key , then it will create a new key in wordsObject
            wordsObject[word] = {
                "freq" : 1,
                "pos" : [index]
            }









        # -----------------------------------------------------
        # OLD CODE 
        # wordObj = {}
        # listOfPos = []

        # freq = 0

        # for i ,curWord in enumerate(words):
            # if(curWord == word):
                # freq += 1

                # finding positions of a word in a list of words , and push it in the list

                # listOfPos.append(i)

                # by removing repeating words we will increase efficieny
                # because in this way it doesn't need to iterate over again on repeated words

                # words.remove(curWord)

        # here I am assigning docID to each word of that doc
        # maybe it can be used later for inverted index

        # wordObj[word] = freq

        # entering word with its list of positions in a article

        # wordObj['pos'] = listOfPos
        # wordObj['docID'] = docID

        # listWords.append(wordObj)
        # ----------------------------------------------------------
    return wordsObject


def createForwardIndex(docsList):
    """
    INPUT: I will take full list of converted json objs from jsonFile (e.g, news369),
    then it will return a forwardIndex
    """
    forwardIndex = []
    for doc in docsList:
        docObj = {}
        metaDataObj = {}
        for key in doc:
            if(key == 'content'):
                # docObj[key] = doc[key]
                words = convertToWords(doc[key])
                # docObj['words'] = words

                # docObj['words'] = listOfWordsHits(words, doc['id'])

                wordsObj = listOfWordsHits(words)
                docObj['words'] = wordsObj
            else:
                metaDataObj[key] = doc[key]
            docObj["metaData"] = metaDataObj

        forwardIndex.append(docObj)


    return forwardIndex

def writeForwardIndexToFile(forwardIndex):
    """
    INPUT: it will take forwardIndex,
    and write it to a file after converting it to json obj
    """
    file_path = "./forward_index/output5.json"

    # print(forwardIndex)

    # Write the list to a JSON file

    with open(file_path, 'w') as json_file:

        # json.dump(forwardIndex, json_file, indent=2)

        # json.dump(forwardIndex, json_file, indent=2)
        json.dump(forwardIndex, json_file)





# with open('./nela-gt-2022/newsdata/369news.json', 'r') as file:
# with open('./nela-gt-2022/newsdata/weareanonymous.json', 'r') as file:
with open('./nela-gt-2022/newsdata/mcclatchydc.json', 'r') as file:
# with open('./nela-gt-2022/newsdata/abcnews.json', 'r') as file:
    docsList = json.load(file)

    forwardIndex = createForwardIndex(docsList)



    # forwardIndex will look like this:
    # forwardIndex = [
    #     {
    #     metaData: {
    #         id: docId,
    #         title: docTitle,
    #         date: docDate,
    #         url : links,
    #         ...,}
    #         words: [
    #             {
    #                 word: freq,
    #                 docID : numberOftimesOccured 
    #              }]
    #      },
    #             {
    #               ...
    #             }
    # 
    #     },
    #     {........}, 
    # ]

    writeForwardIndexToFile(forwardIndex)



# print(docsList)



# print(forwardIndex)