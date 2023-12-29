import os
import sys
import time
from nltk.stem import SnowballStemmer
from constants import STOP_WORDS
import ujson
import shutil
import numpy
import operator
from collections import OrderedDict
STOP_WORDS_SET = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
                       'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
                        'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
                        'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were',
                        'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
                        'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
                        'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
                        'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'her',
                        'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
                        'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's',
                        't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 
                        've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',
                        "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
                        "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren',
                        "weren't", 'won', "won't", 'wouldn', "wouldn't"])

stemmer = SnowballStemmer("english")
# this hashing function was written by me specifically for nela-gt-2022 dataset,
# it sufficiently (uniformaly) distributes words in the search engine barrels

class Hashing:

    def HasherFunction(self, inputString):
        sum = 0
        for index, element in enumerate(inputString):
            sum = sum + ((len(inputString) - index) * ord(element))
        return (sum)%500
    
    def rankingScore(self, freq, totalWords, posCoVar):
        return round((10000*(freq/totalWords))/(1 if posCoVar == 0 else posCoVar), 4)

class Search:

    def __init__(self, queueSize = 11):
        self.queueSize = queueSize
        self.queue = []
        self.files = {}
        self.hashing = Hashing()
        with open("metaDataURL.json") as f:
            self.meta = ujson.load(f)

    def addFileToQueue(self, barrelNo):
        with open (f"Inverted_Index/barrel{barrelNo}.json", "r") as f:
            self.queue.append(barrelNo)
            self.files[barrelNo] = ujson.load(f)
        print(self.queue)

        if (len(self.queue) > self.queueSize):
            self.files.pop(self.queue[0])
            self.queue.pop(0)

        
    def singleWordSearch(self, word):
        time1 = time.time()
        wordHash = self.hashing.HasherFunction(word)
        if wordHash not in self.files:
            self.addFileToQueue(wordHash)
        if word not in self.files[wordHash].keys():
            return []
        results = [self.meta[result]["url"] for result in self.files[wordHash][word].keys()]
        print((time.time()-time1)*1000)
        return results
        
    def multiWordSearch(self, words):
        time1 = time.time()
        barrels = []
        isNot = bool()
        results = []
        findTill = 0
        for i, word in enumerate(words):
            barrels.append(self.hashing.HasherFunction(word))
            if barrels[i] not in self.files:
                self.addFileToQueue(barrels[i])
        while words[findTill] not in self.files[barrels[findTill]]:
            findTill += 1
        for doc in self.files[barrels[findTill]][words[findTill]].keys():
            for i,  word in enumerate(words[findTill:]):
                if doc not in self.files[barrels[findTill+i]][word].keys():
                    isNot = True
                    break
            if not isNot:
                results.append(doc)
        return [self.meta[result]["url"] for result in results]

            
        
        print((time.time()-time1)*1000)
    def cleaningFunction(self, content):
        words = content.lower().split(' ')
        words = [stemmer.stem(word).encode("ascii", errors="ignore").decode().strip('\',._+/\\!@#$?^()[]}{"').strip() for word in words if word not in STOP_WORDS_SET]
        words = [word for word in words if len(word) != 0]
        return words
# class written to generate forward index 
class ForwardIndex:

    def __init__(self):
        self.__noOfArticles = 0
        self.__fileCounter = 0
        
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

    def __getMetaData(self):
        if os.path.exists("metaDataURL.json"):
            with open("metaDataURL.json", "r") as f:
                return ujson.load(f)
        return {}
    
    def createForwardIndex(self, documentList):
        """
        INPUT: A list of .json files in a directory
        OUTPUT: The Corresponding Forward Index
        """
        self.__fileCounter = 0
        self.__noOfArticles = 0
        os.system("cls")
        print("generating forward index....")
        start_time = time.time()
        forwardIndex = []
        keysOfArticle = list(documentList[0][0].keys())
        keysOfArticle.remove("content")
        metaDataURL = self.__getMetaData()
        for jsonDocument in documentList:
            for article in jsonDocument:
                if article["id"] not in metaDataURL:
                    metaDataURL[article["id"]] = {"url": article["url"], "title": article["title"]}
                else:
                    continue
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
                self.__noOfArticles += 1
        if bool(forwardIndex):
            self.writeForwardIndexToFile(forwardIndex)
        os.system("cls")
        with open("metaDataURL.json", "w") as f:
            ujson.dump(metaDataURL, f)
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
    
    def noProcessedArticles(self):
        return self.__noOfArticles
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
            print("writing(): " + path)
        else:
            print("updating(): " + path)
        with open(path, mode="w") as writeFile:
            for word in barrel:
                # barrel[word] = OrderedDict(sorted(barrel[word].items(), key=operator.itemgetter(1), reverse=True))
                if word in temp:
                    temp[word].update(barrel[word])
                    temp[word] = OrderedDict(sorted(temp[word].items(), key=operator.itemgetter(1), reverse=True))
                    continue
                temp[word] = OrderedDict(sorted(barrel[word].items(), key=operator.itemgetter(1), reverse=True))
            ujson.dump(temp, writeFile)
        
                
    def generateInvertedIndex(self, noFiles):
        """
        SIDE EFFECTS: generates a inverted index for the
        forward index present in the directory
        """
        os.system("cls")
        print("generating inverted index....")
        os.makedirs("Inverted_Index", exist_ok=True)
        hashingObject = Hashing()
        startTime = time.time()
        invertedIndex = {}
        coVar = 0
        mean = 0
        for indexNo in range(noFiles):
            with open("Forward_Index/stemmedIndex"+str(indexNo)+".json", "r") as forwardIndexFile:
                forwardIndex = ujson.load(forwardIndexFile)
            for articleData in forwardIndex:
                words = articleData["words"].keys()
                for word in words:
                    barrelName = hashingObject.HasherFunction(word)
                    coVar = numpy.std(numpy.array(articleData["words"][word]["pos"]))
                    mean = numpy.mean(numpy.array(articleData["words"][word]["pos"]))
                    coVar = coVar/(mean if mean != 0 else 1)
                    if barrelName in invertedIndex:
                        if word in invertedIndex[barrelName]:
                            invertedIndex[barrelName][word][articleData["metaData"]["id"]] = hashingObject.rankingScore(articleData["words"][word]["freq"], len(articleData["words"]), coVar)
                        else:
                            invertedIndex[barrelName][word] = {articleData["metaData"]["id"] : hashingObject.rankingScore(articleData["words"][word]["freq"], len(articleData["words"]), coVar)}
                    else:
                        invertedIndex[barrelName] = {}
                    if sys.getsizeof(invertedIndex[barrelName]) > 7000:
                        self.writeAndIfUpdateBarrel(invertedIndex[barrelName], barrelName)
                        invertedIndex[barrelName] = {}
                
        barrelNames = invertedIndex.keys()
        forwardIndex = []
        for barrelName in barrelNames:
            self.writeAndIfUpdateBarrel(invertedIndex[barrelName], barrelName)
        os.system("cls")
        print("Execution Time (Inverted Index): " + str(time.time() - startTime))
        time.sleep(2)


# class demonstrating the generation of forward index as well as
# the inverted index
class IndexGenerator:

    def __init__(self):
        self.fIndex = ForwardIndex()
        self.iIndex = InvertedIndex()

    def runGenerator(self, directoryName):
        """
        SIDE EFFECT: Creation of forward and inverted indexes
        """
        startTime = time.time()
        self.fIndex.forwardIndexGenerator(directoryName)
        self.iIndex.generateInvertedIndex(self.fIndex.getNoFiles())
        os.system("cls")
        print(f'Processed {self.fIndex.noProcessedArticles()} articles in {round(time.time() - startTime, 2)} seconds')

    def extendIndex(self, filePath):
        self.fIndex.__fileCounter = 0
        self.fIndex.__noOfArticles = 0
        with open(filePath, "r") as f:
            self.fIndex.createForwardIndex([ujson.load(f)])
        self.iIndex.generateInvertedIndex(self.fIndex.getNoFiles())

    


# def main():
#     #  usage: python IndexGen.py <directory>
#     if (len(sys.argv) != 2):
#         print("Correct Usage: \"python IndexGen.py <directory>\"")
#         sys.exit()
#     directoryName = sys.argv[1]
#     indexGenerator = IndexGenerator()
#     indexGenerator.runGenerator(directoryName)
    

# main()
