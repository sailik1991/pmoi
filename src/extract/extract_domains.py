"""
CSE 575 Group Project: Predicting Objects in Missing Images

Parser for Visual Genome image data by Elan Markov

This parser extracts object and phrase data for all images within a domain
JSON files and saves as text files for the next step in the parsing
process. This version is adapted from the API but does not query the
API directly.

Here, the "ski" and "racket" domains will be extracted.

This skips the Retrieve Data step that requires querying the VG server,
which significantly cuts down on the runtime.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image as PIL_Image
import requests
from StringIO import StringIO
import simplejson as json #fast JSON reader
from unidecode import unidecode #convert unicode symbols to closest ASCII equivalent
import re #for regular expressions

def createObject(objData, objFile, codeWords):
	print "WARNING: Reading JSON file will take a while, machine may perform slowly in meantime."
	dataFile = open(objData, 'r')
	data = json.loads(dataFile.read())
	outFile = open(objFile, 'w')
	print "JSON File read, now processing images."
	numImg = 0
	numInDomain = 0
	for image in data:
		numImg = numImg + 1
		objects = image['objects']
		if(matchObjects(objects, codeWords)): #only print matches
			numInDomain = numInDomain + 1
			outFile.write("%d\n" % image['image_id'])
			outFile.write("%d\n" % len(objects))
			for obj in objects:
				outFile.write("%d %d %d %d " % (obj['x'], obj['y'], obj['w'], obj['h']))
				name = unidecode(obj['names'][0]).rstrip() #use only the first name listed
				outFile.write(name) 
				outFile.write('\n')
		if(numImg % 100 == 0):
			print "%d of %d images completed" % (numImg, len(data))
	print "Images in this domain: %d\n" % numInDomain
	dataFile.close()
	outFile.close()

def createPhrase(phraseData, phraseFile, codeWords):
	print "WARNING: Reading JSON file will take a while, machine may perform slowly in meantime."
	dataFile = open(phraseData, 'r')
	data = json.loads(dataFile.read())
	print "JSON File read, now processing images."
	outFile = open(phraseFile, 'w')
	numImg = 0
	numInDomain = 0
	for image in data:
		numImg = numImg + 1
		regions = image['regions']
		if(matchPhrases(regions,codeWords)):
			numInDomain = numInDomain + 1
			imgID = regions[0]['image_id']
			outFile.write("%d\n" % imgID)
			outFile.write("%d\n" % len(regions))
			for reg in regions:
				outFile.write("%d %d %d %d " % (reg['x'], reg['y'], reg['width'], reg['height']))
				name = unidecode(reg['phrase'])
				name = name.strip()
				name = name.replace('\n', ' ')
				outFile.write(name)
				outFile.write('\n')
		if(numImg % 100 == 0):
			print "%d of %d images completed" % (numImg, len(data))
	print "Images in this domain: %d\n" % numInDomain	
	dataFile.close()
	outFile.close()

def matchObjects(objects, codeWords): #print if one object name matches a keyword
	for obj in objects:
		for name in obj['names']:
			for code in codeWords:
				if name == code:
					return True
	return False

def matchPhrases(regions, codeWords): #print if any word in any phrase matches a keyword
	for reg in regions:
		name = unidecode(reg['phrase'])
		for code in codeWords:
			if findWholeWord(code)(name) != None:
				return True
	return False

def findWholeWord(w): #obtained from http://stackoverflow.com/questions/5319922/python-check-if-word-is-in-a-string
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

print "Working on ski objects..."
createObject("objects.json", "skiObjects.txt", ["ski"])
print "Working on racket objects..."
createObject("objects.json", "racketObjects.txt", ["racket", "racquet"])
print "All objects created and saved!"

print "Working on ski phrases..."
createPhrase("region_descriptions.json", "skiPhrases.txt", ["ski"])
print "Working on racket phrases..."
createPhrase("region_descriptions.json", "racketPhrases.txt", ["racket", "racquet"])
print "All phrases created and saved!"

