#!/usr/bin/python
from gensim import models
from copy import deepcopy
from utilities import *

window_size = 3

def train(domain, shouldTrain, setNumber):
    '''
    The function trains a model on training data and then tests the models accuracy on the testing data.
    Since training is time consuming, we save the model and load it later for further testing
    '''
    print "\n=== Set : %s ===\n" % str(setNumber)

    if shouldTrain == True:
        sentences = models.word2vec.LineSentence(domain+'/train'+str(setNumber)+'.txt')
        model = models.Word2Vec(sentences=sentences, min_count=1, workers=4, hs=1, window=window_size, iter=1000)
        model.save(domain+'/model'+str(setNumber)+'.txt')
    else:
        # OR load a mode
        model = models.Word2Vec.load(domain+'/model'+str(setNumber)+'.txt')

    print "Training : COMPLETE!"

    # Evaluate model on test data
    plans = open(domain+'/test'+str(setNumber)+'.txt').read().split("\n")
    list_of_objects = [[unicode(actn, "utf-8") for actn in plan_i.split()] for plan_i in plans]
    objects = model.vocab.keys()
    #print "#objects = {0}".format( len(objects) )
    return [x for x in list_of_objects if len(x) > window_size*2], objects, model

def train_and_test(domain, shouldTrain, setNumber):

    list_of_objects, objects, model = train(domain, shouldTrain, setNumber)

    correct = 0
    total = 0
    #print list_of_objects, objects
    print "Testing : RUNNING . . ."
    for itr in xrange(len(list_of_objects)):

        img = list_of_objects[itr]

        incomplete_img, missing_idx = remove_random_objects(img)
        total += 1
        object_set, tentative_imgs = permuteOverMissingActions(objects, missing_idx, incomplete_img)
        correct += predictAndVerify(model, missing_idx, tentative_imgs, object_set, img, window_size)

        # Print progress at certain time intervals
        if (itr*100)/len(list_of_objects) % 10 == 0:
            sys.stdout.write( "\rProgress: %s %%" % str( (itr*100)/len(list_of_objects) ) )
            sys.stdout.flush()

    sys.stdout.write( "\r\rTesting : COMPLETE!\n")
    sys.stdout.flush()
    print "\nUnknown actions: %s; Correct predictions: %s" % (str(total), str(correct))
    print "Set Accuracy: %s\n" % str( float(correct*100)/total )
    return total, correct
