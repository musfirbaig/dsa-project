
# hashing a file using a word, that is also hashed in createMetaDataFiles
def hashFileName(word):
    metaFileName = ''
    for char in word:
        if char.isalnum():
            metaFileName = char
            break
    if metaFileName == '':
        metaFileName = 'dump'
    return metaFileName