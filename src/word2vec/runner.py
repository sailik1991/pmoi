import bf
import dup
import sys

def main(argv):
    #print argv
    domain = argv[0]
    train = True if len(argv)==2 and argv[1]=='t' else False
    #K is used for k-fold cross validation
    k = 10

    missing = 0
    correct = 0
    for i in range(k):
        m, c = bf.train_and_test( domain, train, i )
        missing += m
        correct += c

    print "\n==== FINAL STATISTICS ===="
    print "\nTotal missing objects: %s; Total correct predictions: %s" % (str(missing), str(correct))
    print "ACCURACY: %s\n" % str( float(correct*100)/missing )

if __name__ == "__main__":
    main(sys.argv[1:])
