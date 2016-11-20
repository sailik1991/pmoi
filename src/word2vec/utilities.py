#!/usr/bin/python
from gensim import models
from copy import deepcopy
from math import ceil,floor
from itertools import permutations
import random
import sys, getopt
import random

pediction_set_size = 70

""" NEEDED FOR TRAINING """
def remove_random_objects(image):
    missing_index = random.randrange(0, len(image))
    incomplete_image = deepcopy(image)
    incomplete_image[ missing_index ] = ''
    return incomplete_image, missing_index

""" NEEDED FOR DUP """
def getActionsForBlanks(T):
    index = []
    for i in xrange(len(T)):
        v = max(T[i])
        index.append( random.choice([j for j in xrange(len(T[i])) if T[i][j] == v]) )
    return index

def verify(T, indices, actions, plan):
    correct = 0.0
    for i in xrange(len(T)):
        acts = sorted( range(len(T[i])), key=lambda x:T[i][x] )[-1*pediction_set_size:]
        if plan[indices[i]] in acts:
            correct += 1.0
    return correct

""" NEEDED FOR BRUTE FORCE """
def getTentativeImage(o, ii, idx):
    ii[idx] = o
    return ii

def permuteOverMissingActions(objects, missing_idx, incomplete_img):
    object_set = []
    tentative_imgs = []
    for o in permutations(objects, 1):
        object_set.append(o)
        tentative_imgs.append(getTentativeImage(o, incomplete_img, missing_idx))
    return object_set, tentative_imgs

def predictAndVerify(model, missing_idx, tentative_imgs, object_set, img, window_size):
    correct = 0
    window_subimg = []
    for ti in tentative_imgs:
	window_subimg.append( ti[max(0,missing_idx-window_size):min(len(ti),missing_idx+window_size+1)] )
    scores = model.score( window_subimg )
    best_indices = scores.argsort()[-1*pediction_set_size:][::-1]
    for j in best_indices:
        #print object_set[j][0]
        #print img[missing_idx]
	    if object_set[j][0] == img[missing_idx]:
	        correct += 1
	        break;
    
    return correct
