"""
CSE 575 Group Project: Predicting Objects in Missing Images

Parser for Visual Genome API image data by Elan Markov
Adapted from Visual Genome API Tutorial
This file will extract 100 image object descriptions from the
Visual Genome site.

Full version will extract from included JSON file directly due to large size.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import api as vg
from PIL import Image as PIL_Image
import requests
from StringIO import StringIO
import time

def ImageDataExtract():
	#ids = vg.GetAllImageIds() # 108077 images total
	ids = vg.GetImageIdsInRange(startIndex=0, endIndex=99) #use for testing purposes, use the above command for full extraction
	imageDataList = []
	idNum = len(ids)
	print "total ids = %d" % len(ids)
	for i in range(0,len(ids)): 
		print "image %d of %d processing" % (i+1, idNum)
		image_id = ids[i]
		graph = vg.GetSceneGraphOfImage(id=image_id)
		url = graph.image.url
		objects = graph.objects
		objList = []
		for j in range(0,len(objects)):
			objList.append((objects[j].x, objects[j].y, objects[j].width, objects[j].height, objects[j].names))
		imageDataList.append((image_id, url, objList))
	return imageDataList

def createText(filename):
	output = ImageDataExtract()
	outFile = open(filename, 'w')
	for i in range(0, len(output)):
		outputCurr = output[i]
		outFile.write("%d\n" % outputCurr[0])
		outFile.write(outputCurr[1] + '\n')

		objects = outputCurr[2]
		outFile.write("%d\n" % len(objects))
		for j in range(0, len(objects)):
			obj = objects[j]
			outFile.write("%d %d %d %d " % (obj[0], obj[1], obj[2], obj[3]))
			outFile.write(obj[4][0]) 
			outFile.write('\n')

t1 = time.time()
createText("100objects.txt")
t2 = time.time()-t1
print "%d" % t2
