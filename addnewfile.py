import json
import os
import sys
import time
from nltk.stem import SnowballStemmer
from constants import STOP_WORDS
import ujson
import shutil
import math
from collections import defaultdict
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
class AddNewFile:
    def __init__(self):
        self.__fileCounter = 0
        self.existingArticleIds = set()
    
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
    def updateMetadataFile(self, new_data):
        """
        Update the metadata file with new entries from the processed documents.
        """
        metadata_filename = "metadata_urls.json"

        if not os.path.exists(metadata_filename):
            metadata = []
        else:
            with open(metadata_filename, 'r') as metadata_file:
                metadata = ujson.load(metadata_file)

        for document in new_data:
            metadata.append({
                'doc_id': document['metaData']['id'],
                'url': document['metaData']['url']
                })

        with open(metadata_filename, 'w') as metadata_file:
            ujson.dump(metadata, metadata_file, indent=4)
    def writeForwardIndexToFile(self, forwardIndex):
        os.makedirs("Forward_Index", exist_ok=True)
        file_path = "Forward_Index/stemmedIndex" + str(self.__fileCounter) + ".json"
        print("writing(): " + file_path)
        with open(file_path, 'w') as json_file:
            ujson.dump(forwardIndex, json_file)
        self.__fileCounter += 1

    def calculateTFIDF(self, freq, totalDocs, docsWithTerm):
        tf = freq / totalDocs
        idf = math.log(totalDocs / (1 + docsWithTerm))
        return tf * idf
    def addFileToForwardIndex(self, new_file_path):
        with open(new_file_path) as new_file:
            new_data = ujson.load(new_file)
        
        metadata_filename = "metadata_urls.json"
        if os.path.exists(metadata_filename):
            with open(metadata_filename, 'r') as metadata_file:
                metadata = ujson.load(metadata_file)
                self.existingArticleIds = {item['doc_id'] for item in metadata}

        additional_documents = []

        for document in new_data:
            article_id = document["id"]

            if article_id in self.existingArticleIds:
                print(f"Article with ID {article_id} already exists in the forward index.")
                continue
            else:
                print(f"Adding article with ID {article_id} to the forward index.")

            articleObject = {"metaData": {}}
            words = self.convertToWords(document["content"])
            wordsObject = self.dictWordToPositionAndFrequency(words)
            articleObject["words"] = wordsObject

            for key in document.keys():
                if key != "content":
                    articleObject["metaData"][key] = document[key]

            additional_documents.append(articleObject)
            self.existingArticleIds.add(article_id)

        # Write all documents to forward index and update metadata
        self.writeForwardIndexToFile(additional_documents)
        self.updateMetadataFile(additional_documents)
        self.updateInvertedIndexBarrels(additional_documents)
    def updateInvertedIndexBarrels(self, additional_documents):
        hashingObject = Hashing()
        invertedIndex = defaultdict(lambda: defaultdict(list))

        for document in additional_documents:
            wordsObject = document["words"]

            for word, info in wordsObject.items():
                barrelName = hashingObject.HasherFunction(word)
                docsWithTerm = len(invertedIndex[barrelName][word])
                rank = self.calculateTFIDF(info["freq"], self.getNoFiles(), docsWithTerm)
                info["rank"] = rank
                info["id"] = document["metaData"]["id"]

                if info not in invertedIndex[barrelName][word]:
                    invertedIndex[barrelName][word].append(info)

                # Check size and write to file if exceeds the limit
                if sys.getsizeof(invertedIndex[barrelName]) > 7000:
                    self.writeBarrelToFile(invertedIndex[barrelName], barrelName)
                    invertedIndex[barrelName] = defaultdict(list)

        # Write remaining barrels to files
        for barrelName, barrel in invertedIndex.items():
            self.writeBarrelToFile(barrel, barrelName)

    def writeBarrelToFile(self, barrel, barrelName):
        path = f"Inverted_Index/barrel{barrelName}.json"
        temp = {}

        if os.path.exists(path):
            with open(path, mode="r") as alreadyBarrel:
                temp = ujson.load(alreadyBarrel)

        for word, info in barrel.items():
            if word in temp:
                temp[word].extend(info)
            else:
                temp[word] = info
                
        os.makedirs("Inverted_Index", exist_ok=True)
        with open(path, mode="w") as writeFile:
            ujson.dump(temp, writeFile)

        print(f"Barrel {barrelName} data written to file")


    def getNoFiles(self):
        return self.__fileCounter
    
    def noProcessedArticles(self):
        return self.__noOfArticles
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

