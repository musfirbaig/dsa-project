
# hashing a file using a word, that is also hashed in createMetaDataFiles

# old code for hashfunction

def hashFileName(word):
    metaFileName = ''
    for char in word:
        if char.isalnum():
            metaFileName = char
            break
    if metaFileName == '':
        metaFileName = 'dump'
    return metaFileName


def hashFileName(word):
    #  I am assuming that the word that is inputed is always lowercase
    metaFileName = ''
    for char in word:
        if char.isalnum():
            wordLength = len(word)
            if(wordLength>=3 and wordLength <= 12):
                # if wordleng is between 3 and 12, then a3, a5 etc filename, its for creating barrels with its name
                metaFileName = char + str(len(word))
                break
            elif wordLength < 3:
                metaFileName = char + 's'
                break
            else:
                metaFileName = char + 'l'
                break
    if metaFileName == '':
        metaFileName = 'dump'
    return metaFileName

# print(hashFileName("musfirbaig"))