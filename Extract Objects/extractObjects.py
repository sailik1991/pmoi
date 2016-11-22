"""
readFile: read in the phrases from the text file
extractNouns: extract objects from the phrases using nltk
"""

from nltk.corpus import wordnet as wn
from nltk import pos_tag, word_tokenize

def readFile(filename):
    f = open(filename)
    lines = f.read().strip().split("\n")
    imagePhrases = []
    
    i = 0
    
    while i < len(lines):
        try:
            print lines[i]
            #img = str(lines[i+1])
            size = int(lines[i+1])
            phrases = []
            counter = 0
        
            for j in range(size):
                parts = lines[i+2+j].split()

                if len(parts) <= 4:
                    counter += 1
                    continue

                info = []
    
                for m in range(0, 4):
                    info.append(int(parts[m]))

                phrase = ''.join([k for k in str(lines[i+2+j]) if not k.isdigit(    )]).strip()
                phrases.append([info, phrase])
            
            #i += 1
            imagePhrases.append(phrases)
            i += 2 + size

        except:
            i += 2 + size
    f.close()
    return imagePhrases

def overlappingRectangles(oldTL, oldBR, TL, BR):
    
    if(oldTL[0] > BR[0] or TL[0] > oldBR[0]):
        return False

    if(oldTL[1] < BR[1] or TL[1] < oldBR[1]):
        return False

    return True

def extractNouns(imagePhrases):

    imageObjects = []
    for i in range(0, len(imagePhrases)):
        phrases = imagePhrases[i]
        objects = []
        phraseInfo = []
        for j in range(0, len(phrases)):
            [info, phrase] = phrases[j]
            tags = pos_tag(word_tokenize(phrase))
            nouns = [t for t in tags if 'NN' in t]
            nouns = [row[0].lower() for row in nouns]
            nouns = [n for n in nouns if n not in objects]
            
            #newObjects = []

            objectNouns = []
            for n in nouns:
                if len(wn.synsets(n)) is not 0:
                    synonyms = wn.synsets(n)[0].lemma_names() 
                    intersectionSet = set(objects).intersection(synonyms)
                    if len(intersectionSet) > 0:
                        continue
                #newObjects.append(n) 
                objectNouns.append(n)
                
            """for n in newObjects:
                if n not in objects:
                    objectNouns.append(n)
                else:
                    oldInfo = []
                    oldInfoFlag = False
                    for p in range(0, len(phraseInfo)):
                        if n in phraseInfo[p][1]:
                            oldInfo = phraseInfo[p][0]
                            oldInfoFlag = True
                            break
                    
                    if oldInfoFlag is True:
                        oldTL = [oldInfo[0], oldInfo[1]]
                        oldBR = [oldInfo[0]+oldInfo[2], oldInfo[1]+oldInfo[3]]

                        TL = [info[0], info[1]]
                        BR = [info[0] + info[2], info[1]+ info[3]]
                    
                        flag = overlappingRectangles(oldTL, oldBR, TL, BR)

                        if flag is False:
                            objectNouns.append(n)
                
            phraseInfo.append([info, objectNouns])   
            """
            
            objects += objectNouns

        imageObjects.append(objects)

    return imageObjects

if __name__ == "__main__":
    imagePhrases = readFile('allPhrases-2.txt')
    #print imagePhrases
    imageObjects = extractNouns(imagePhrases)
    
    f = file('objects.lst', 'w')

    for i in range(len(imageObjects)):
        print i
        for x in imageObjects[i]:
            f.write(x+" ")
        f.write('\n')
