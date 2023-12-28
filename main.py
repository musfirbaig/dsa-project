import os
import sys
import time
from testersearchfunction import ForwardIndex, InvertedIndex, MetadataFile

class IndexGenerator:

    def runGenerator(self, directoryName):
        """
        SIDE EFFECT: Creation of forward and inverted indexes, and metadata file
        """
        fIndex = ForwardIndex()
        iIndex = InvertedIndex()
        metadataCreator = MetadataFile()  # Instantiate MetadataFile

        startTime = time.time()
        fIndex.forwardIndexGenerator(directoryName)
        iIndex.generateInvertedIndex(fIndex.getNoFiles())
        metadataCreator.createMetadataJSON(fIndex.documentList(directoryName))  # Generate metadata

        os.system("cls")
        print(f'Processed {fIndex.noProcessedArticles()} articles in {round(time.time() - startTime, 2)} seconds')

def main():
    #  usage: python IndexGen.py <directory>
    if (len(sys.argv) != 2):
        print("Correct Usage: \"python IndexGen.py <directory>\"")
        sys.exit()
    directoryName = sys.argv[1]
    indexGenerator = IndexGenerator()
    indexGenerator.runGenerator(directoryName)

main()