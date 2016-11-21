"""
CSE 575 Group Project: Predicting Objects in Missing Images

Parser for Visual Genome image data by Elan Markov

This parser extracts object and phrase data for all images from
JSON files and saves as text files for the next step in the parsing
process. This version is adapted from the API but does not query the
API directly.

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

def createObject(objData, objFile):
	print "WARNING: Reading JSON file will take a while, machine may perform slowly in meantime."
	dataFile = open(objData, 'r')
	data = json.loads(dataFile.read())
	outFile = open(objFile, 'w')
	print "JSON File read, now processing images."
	numImg = 0
	for image in data:
		numImg = numImg + 1
		outFile.write("%d\n" % image['image_id'])
		objects = image['objects']
		outFile.write("%d\n" % len(objects))
		for obj in objects:
			outFile.write("%d %d %d %d " % (obj['x'], obj['y'], obj['w'], obj['h']))
			name = unidecode(obj['names'][0]).rstrip() #use only the first name listed
			outFile.write(name) 
			outFile.write('\n')
		if(numImg % 100 == 0):
			print "%d of %d images completed" % (numImg, len(data))
	dataFile.close()
	outFile.close()

def createPhrase(phraseData, phraseFile):
	print "WARNING: Reading JSON file will take a while, machine may perform slowly in meantime."
	dataFile = open(phraseData, 'r')
	data = json.loads(dataFile.read())
	print "JSON File read, now processing images."
	outFile = open(phraseFile, 'w')
	numImg = 0
	for image in data:
		numImg = numImg + 1
		regions = image['regions']
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
	dataFile.close()
	outFile.close()

print "Working on objects..."
createObject("objects.json", "allObjects.txt")
print "All objects created and saved!"

print "Working on phrases..."
createPhrase("region_descriptions.json", "allPhrases.txt")
print "All phrases created and saved!"
