# pmoi
The module tries to Predict Missing Objects in Images.

## Workflow

+ Generate object sequences from object data obtained from visual genome database
```bash
cd ./src/data/
python object_sequence_generator.py allObjects.txt
```

+ Move the generated list and divide data for k-fold cross validation
```bash
cp vg.lst ../word2vec/imgs_as_objs/
cd ../word2vec/
python k_fold_generator.py imgs_as_objs/vg.lst
```

+ Run word2vec and compute the accuracy
```bash
python runner.py imgs_as_objs/
```

Sample output for a run looks like this (prediction set size = 5%):
```
=== Set : 0 ===

Training : COMPLETE!
Testing : RUNNING . . .
Testing : COMPLETE!

Unknown actions: 9917; Correct predictions: 475
Set Accuracy: 4.78975496622


=== Set : 1 ===

Training : COMPLETE!
Testing : RUNNING . . .
Testing : COMPLETE!

Unknown actions: 10369; Correct predictions: 572
Set Accuracy: 5.51644324429


=== Set : 2 ===

Training : COMPLETE!
Testing : RUNNING . . .
Testing : COMPLETE!

Unknown actions: 9615; Correct predictions: 434
Set Accuracy: 4.51378055122


=== Set : 3 ===

Training : COMPLETE!
Testing : RUNNING . . .
Testing : COMPLETE!

Unknown actions: 9924; Correct predictions: 485
Set Accuracy: 4.88714228134


=== Set : 4 ===

Training : COMPLETE!
Testing : RUNNING . . .
Testing : COMPLETE!

Unknown actions: 10563; Correct predictions: 520
Set Accuracy: 4.92284388905


=== Set : 5 ===

Training : COMPLETE!
Testing : RUNNING . . .
Testing : COMPLETE!

Unknown actions: 10654; Correct predictions: 481
Set Accuracy: 4.5147362493


=== Set : 6 ===

Training : COMPLETE!
Testing : RUNNING . . .
Testing : COMPLETE!

Unknown actions: 10654; Correct predictions: 576
Set Accuracy: 5.4064201239


=== Set : 7 ===

Training : COMPLETE!
Testing : RUNNING . . .
Testing : COMPLETE!

Unknown actions: 10286; Correct predictions: 521
Set Accuracy: 5.06513707953


=== Set : 8 ===

Training : COMPLETE!
Testing : RUNNING . . .
Testing : COMPLETE!

Unknown actions: 10386; Correct predictions: 421
Set Accuracy: 4.05353360293


=== Set : 9 ===

Training : COMPLETE!
Testing : RUNNING . . .
Testing : COMPLETE!

Unknown actions: 10545; Correct predictions: 497
Set Accuracy: 4.71313418682


==== FINAL STATISTICS ====

Total missing objects: 102913; Total correct predictions: 4982
ACCURACY: 4.84098218884
```
