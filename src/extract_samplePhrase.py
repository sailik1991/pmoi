"""
CSE 575 Group Project: Predicting Objects in Missing Images

Parser for Visual Genome API image data by Elan Markov
Adapted from Visual Genome API Tutorial
This file will extract 100 image phrase descriptions from the
Visual Genome site.

Full version will extract from included JSON file directly due to large size.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import api as vg
from PIL import Image as PIL_Image
import requests
from StringIO import StringIO

def ImageDataExtract():
	#ids = vg.GetAllImageIds() # 108077 images total
	ids = vg.GetImageIdsInRange(startIndex=0, endIndex=99) #use for testing purposes, use the above command for full extraction
	imageDataList = []
	idNum = len(ids)
	print "total ids = %d" % len(ids)
	for i in range(0,len(ids)): 
		print "image %d of %d processing" % (i+1, idNum)
		image_id = ids[i]
		image = vg.GetImageData(id=image_id)
		url = image.url
		regions = vg.GetRegionDescriptionsOfImage(id=image_id)
		phraseList = []
		for j in range(0,len(regions)):
			phraseList.append((regions[j].x, regions[j].y, regions[j].width, regions[j].height, regions[j].phrase))
		imageDataList.append((image_id, url, phraseList))
	return imageDataList

def createText(filename):
	output = ImageDataExtract()
	outFile = open(filename, 'w')
	for i in range(0, len(output)):
		outputCurr = output[i]
		outFile.write("%d\n" % outputCurr[0])
		outFile.write(outputCurr[1] + '\n')

		phrases = outputCurr[2]
		outFile.write("%d\n" % len(phrases))
		for j in range(0, len(phrases)):
			phrase = phrases[j]
			outFile.write("%d %d %d %d " % (phrase[0], phrase[1], phrase[2], phrase[3]))
			outFile.write(phrase[4].rstrip() + '\n') #rstrip because some images end in a newline and mess up formatting

createText("100phrases.txt")
