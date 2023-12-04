import json
import string
import os
import sys
import time
from constants import STOP_WORDS

# TODOS
#  i think i should minimize docIDs by generating my own, so that it will decrease the
#  size , will implement it later
class Hashing:
    def HasherFunction(self, string1):
        sum = 0
        for x,l in enumerate(string1):
            sum = sum + (x+1)*ord(l)
        return (sum)%200
    
class ForwardIndex:

    def convertToWords(self, content):
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
    def listOfWordsHits(self, words):
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
        return wordsObject


    def createForwardIndex(self, docList):
        """
        INPUT: I will take full list of converted json objs from jsonFile (e.g, news369),
        then it will return a forwardIndex
        """
        start_time =  time.time()
        forwardIndex = []
        for docsList in docList:
            for doc in docsList:
                docObj = {}
                metaDataObj = {}
                for key in doc:
                    if(key == 'content'):
                        # docObj[key] = doc[key]
                        words = self.convertToWords(doc[key])
                        # docObj['words'] = words

                        # docObj['words'] = listOfWordsHits(words, doc['id'])

                        wordsObj = self.listOfWordsHits(words)
                        docObj['words'] = wordsObj
                    else:
                        metaDataObj[key] = doc[key]
                    docObj["metaData"] = metaDataObj
                forwardIndex.append(docObj)
        print("Execution Time (Forward): " + str(time.time()-start_time))
        return forwardIndex
    
    def documentList(self ,directoryName):
        files = os.listdir(directoryName)
        files = [(directoryName+"/"+f) for f in files if os.path.isfile(directoryName+'/'+f)] #Filtering only the files
        listDr = []
        for file in files:
            with open(file) as f:
                listDr.append(json.load(f))
        return listDr


    def forwardIndexGenerator(self, directoryName):
        """The function takes a fileName and generates the
        corresponding forward index for that file"""

        docsList = self.documentList(directoryName)
        forwardIndex = self.createForwardIndex(docsList)    
        self.writeForwardIndexToFile(forwardIndex)

    def writeForwardIndexToFile(self, forwardIndex):
        """
        INPUT: it will take forwardIndex,
        and write it to a file after converting it to json obj
        """
        file_path = "Forward_Index.json"
        with open(file_path, 'w') as json_file:
            json.dump(forwardIndex, json_file)

class InvertedIndex:
    
    def generateInvertedIndex(self):
        hashObj = Hashing()
        start_time =  time.time()
        with open("Forward_Index.json", "r") as forwardIndexFile:
            forwardIndex = json.load(forwardIndexFile)
        invertedIndex = {}
        # invertedIndex will look like this : { "barrelName" : { "word1": [{docId: val, freq: val, pos : [list of pos]}, ....], "word2": [{...}, "{.....}, {...} ], "barrelName": .....  }
        # barrelName is calculated using hashFileName function ---> for example "musfir" = m6 barrelName
        for articleData in forwardIndex:
            # articleData is  = { "metaData" : {metadata object}, "words": { "word1": {freq: "val", pos : [list of pos]}}}
            words = articleData["words"].keys()
            for word in words:
                barrelName = hashObj.HasherFunction(word)
                barrelWordsObj = {}
                # wordObjInfo contains {id: val, freq: val, pos: [values]}
                wordObjInfo = articleData["words"][word]
                idOfArticle = articleData["metaData"]["id"]
                wordObjInfo["id"] = idOfArticle
                if invertedIndex.get(barrelName):
                    # invertedIndex[barrelName]
                    if invertedIndex[barrelName].get(word):
                        invertedIndex[barrelName][word].append(wordObjInfo)
                    else:       
                        invertedIndex[barrelName][word] = [wordObjInfo]
                        # invertedIndex[barrelName][word].append(wordObjInfo)
                    # pass
                else:
                    invertedIndex[barrelName] = {}
                    # wordObjInfo contains {id: val, freq: val, pos: [values]}
                    invertedIndex[barrelName][word] = [wordObjInfo]
            barrelNames = invertedIndex.keys()
            # i am also dealing with numbers here like "888" is also searchable, any number is searchable if exists in docs
            # for now, but in future i will think about it

        forwardIndex = []
        for barrelName in barrelNames:
            os.makedirs("Inverted_Index", exist_ok=True)
            barrelFilePath = "Inverted_Index/" + "barrel" + str(barrelName) + ".json"
            with open(barrelFilePath, mode="w") as barrel:
                json.dump(invertedIndex[barrelName], barrel)
        print("Execution Time (Inverted): " + str(time.time()-start_time))

class IndexGenerator:

    def runGenerator(self, directoryName):
        fIndex = ForwardIndex()
        iIndex = InvertedIndex()
        fIndex.forwardIndexGenerator(directoryName)
        iIndex.generateInvertedIndex()



#  usage: python IndexGen.py <directory>
def __main__():
    directoryName = sys.argv[1]
    indexGenerator = IndexGenerator()
    indexGenerator.runGenerator(directoryName)

__main__()
