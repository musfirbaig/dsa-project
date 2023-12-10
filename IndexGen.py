import json
import os
import sys
import time
from nltk.stem import SnowballStemmer
from constants import STOP_WORDS
import ujson
import shutil

STOP_WORDS_SET = set(STOP_WORDS)
stemmer = SnowballStemmer("english")
# this hashing function was written by me specifically for nela-gt-2022 dataset,
# it sufficiently (uniformaly) distributes words in the search engine barrels 
class Hashing:
    def HasherFunction(self, inputString):
        sum = 0
        for index, element in enumerate(inputString):
            sum = sum + ((len(inputString) - index) * ord(element))
        return (sum)%500
    
# class written to generate forward index 
class ForwardIndex:

    def convertToWords(self, content):
        """
        INPUT: article content
        OUTPUT: list of words for case insensitivity (lowercase)
        """
        words = content.lower().split(' ')
        words = [stemmer.stem(word).encode("ascii", errors="ignore").decode().strip('\',._+/\\!@#$?^()[]}{"').strip() for word in words if word not in STOP_WORDS_SET]
        words = [word for word in words if len(word) != 0]
        return words


    def dictWordToPositionAndFrequency(self, words):
        """
        INPUT: list of words and docID,
        OUTPUT: Hash Map of objects containing word-> freq and docID-> docID
        """
        wordsObject = {}
        for index, word in enumerate(words):
            if word in wordsObject:
                wordsObject[word]["freq"] += 1
                wordsObject[word]["pos"].append(index)
            else:
                wordsObject[word] = {
                    "freq" : 1,
                    "pos" : [index]
                }
        return wordsObject


    def createForwardIndex(self, documentList):
        """
        INPUT: A list of .json files in a directory
        OUTPUT: The Corresponding Forward Index
        """


        os.system("cls")
        print("generating forward index....")
        start_time = time.time()
        forwardIndex = []
        keysOfArticle = list(documentList[0][0].keys())
        keysOfArticle.remove("content")
        for jsonDocument in documentList:
            for article in jsonDocument:
                articleObject = {"metaData": {}}
                words = self.convertToWords(article["content"])
                wordsObject = self.dictWordToPositionAndFrequency(words)
                articleObject["words"] = wordsObject
                for key in keysOfArticle:
                    articleObject["metaData"][key] = article[key]
                forwardIndex.append(articleObject)
                if sys.getsizeof(forwardIndex) >= 50000:
                    self.writeForwardIndexToFile(forwardIndex)
                    forwardIndex = []
        if len(forwardIndex):
            self.writeForwardIndexToFile(forwardIndex)
        os.system("cls")
        print("Execution Time (Forward Index): " + str(time.time()-start_time))
        time.sleep(2)
    
    def documentList(self, directoryName):
        """
        INPUT: Directory to operate on
        OUTPUT: List of files in directory
        """
        files = os.listdir(directoryName)
        files = [(directoryName+"/"+f) for f in files if os.path.isfile(directoryName+'/'+f)]
        self.__fileCounter = 0
        listDr = []
        for file in files:
            with open(file) as f:
                listDr.append(ujson.load(f))
        return listDr


    def forwardIndexGenerator(self, directoryName):
        """
        INPUT: Directory to operate on
        OUTPUT: Corresponding Forward Index
        """
        documentList = self.documentList(directoryName)
        self.createForwardIndex(documentList)    

    def writeForwardIndexToFile(self, forwardIndex):
        """
        INPUT: Forward Index
        SIDE EFFECTS: Dumping Forward Index to File
        """
        
        os.makedirs("Forward_Index", exist_ok=True)
        file_path = "Forward_index/" + "stemmedIndex" + str(self.__fileCounter) + ".json"
        print("writing(): " + file_path)
        self.__fileCounter += 1
        with open(file_path, 'w') as json_file:
            ujson.dump(forwardIndex, json_file)

    def getNoFiles(self):
        return self.__fileCounter
# class operates on the ForwardIndex generated by the previous class and generates
# barrel based inverted index
class InvertedIndex:

    def writeAndIfUpdateBarrel(self, barrel: dict, barrelName: str):
        
        path = f"Inverted_Index/barrel{barrelName}.json"
        temp = {}
        
        if os.path.exists(path):
            with open(path, mode="r") as alreadyBarrel:
                temp = ujson.load(alreadyBarrel)
        if len(temp) == 0:
            print("updating(): " + path)
        else:
            print("writing(): " + path)
        with open(path, mode="w") as writeFile:
            for word, info in barrel.items():
                if word in temp:
                    # Update existing information if article IDs match
                    temp[word].append(info)
                else:
                    # Add completely new word information
                    temp[word] = info
            ujson.dump(temp, writeFile)
        
                
    def generateInvertedIndex(self, noFiles):
        """
        SIDE EFFECTS: generates a inverted index for the
        forward index present in the directory
        """
        if os.path.exists("Inverted_Index"):
            shutil.rmtree("Inverted_Index")
        os.system("cls")
        print("generating inverted index....")
        os.makedirs("Inverted_Index", exist_ok=True)
        hashingObject = Hashing()
        startTime = time.time()
        invertedIndex = {}
        for indexNo in range(noFiles):
            with open("Forward_Index/stemmedIndex"+str(indexNo)+".json", "r") as forwardIndexFile:
                forwardIndex = ujson.load(forwardIndexFile)
            for articleData in forwardIndex:
                words = articleData["words"].keys()
                for word in words:
                    barrelName = hashingObject.HasherFunction(word)
                    wordObjectInfo = articleData["words"][word]
                    articleId = articleData["metaData"]["id"]
                    wordObjectInfo["id"] = articleId
                    if barrelName in invertedIndex:
                        if word in invertedIndex[barrelName]:
                            invertedIndex[barrelName][word].append(wordObjectInfo)
                        else:
                            invertedIndex[barrelName][word] = [wordObjectInfo]
                    else:
                        invertedIndex[barrelName] = {word: [wordObjectInfo]}
                    if sys.getsizeof(invertedIndex[barrelName]) > 7000:
                        self.writeAndIfUpdateBarrel(invertedIndex[barrelName], barrelName)
                        invertedIndex[barrelName] = {}
                
        barrelNames = invertedIndex.keys()
        forwardIndex = []
        for barrelName in barrelNames:
            self.writeAndIfUpdateBarrel(invertedIndex[barrelName], barrelName)
        os.system("cls")
        print("Execution Time (Inverted Index): " + str(time.time() - startTime))


# class demonstrating the generation of forward index as well as
# the inverted index
class IndexGenerator:

    def runGenerator(self, directoryName):
        """
        SIDE EFFECT: Creation of forward and inverted indexes
        """
        fIndex = ForwardIndex()
        iIndex = InvertedIndex()
        fIndex.forwardIndexGenerator(directoryName)
        iIndex.generateInvertedIndex(fIndex.getNoFiles())


def main():
    #  usage: python IndexGen.py <directory>
    if (len(sys.argv) != 2):
        print("Correct Usage: \"python IndexGen.py <directory>\"")
        sys.exit()
    directoryName = sys.argv[1]
    indexGenerator = IndexGenerator()
    indexGenerator.runGenerator(directoryName)

main()