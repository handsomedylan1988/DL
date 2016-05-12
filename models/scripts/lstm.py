from __future__ import print_function
import numpy as np
import sPickle
from tools import CatSeqFeature, SeqStr2Vector
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from keras.layers.recurrent import LSTM
from keras.preprocessing.sequence import pad_sequences
import sys
sys.path.append("../Pre/scripts/")
from config import INPUT_DIM, OUTPUT_DIM


batch_size = 16
nb_epoch = 60

# construct model
model = Sequential()

model.add(LSTM(32, input_dim= 64))

#model.add(LSTM(output_dim=OUTPUT_DIM, input_dim=INPUT_DIM))
model.summary()

#model.compile(loss='mse', optimizer=RMSprop())


# load the dictionary
input = open('../Pre/featdict.pkl', 'rb')
featnamearray, feattypedict, featdict = sPickle.load(input)
input.close()

# load the input features
input = open('../Pre/sequence.pkl', 'rb')
X_train_N = sPickle.load(input)
X_train_V = sPickle.load(input)
X_test_N = sPickle.load(input)
X_test_V = sPickle.load(input)
Y_train = sPickle.load(input)
Y_test = sPickle.load(input)
input.close()

assert(len(X_train_V) == len(Y_train))
assert(len(X_test_V) == len(Y_test))
X_test_V = SeqStr2Vector(featnamearray, feattypedict, featdict, X_test_V)
X_test = CatSeqFeature(X_test_V, X_test_N)
X_test = pad_sequences(X_test)
Y_test = pad_sequences(Y_test)
X_test = np.array(X_test)
print (X_test.shape, Y_test.shape)
raw_input()

"""
feed batch to model manually cause vector features can be very large
"""
for i in xrange(nb_epoch):
    print ("epoch:%d" % i)
    batch_number = len(X_train_N) / batch_size
    print(batch_number)
    eidx = 0
    loss = 0
    for n in xrange(batch_number):
        if (n+1) * batch_size < len(X_train_N):
            eidx = (n+1) * batch_size
        else:
            eidx = len(X_train_N)
        X_batch_N = X_train_N[n * batch_size: eidx]
        X_batch_V = X_train_V[n * batch_size: eidx]
        X_batch_V = SeqStr2Vector(
                featnamearray, feattypedict, featdict, X_batch_V)
        X_batch = CatSeqFeature(X_batch_V, X_batch_N)
        Y_batch = Y_train[n * batch_size: eidx]
        X_batch = pad_sequences(X_batch)
        Y_batch = pad_sequences(Y_batch)
        print (X_batch.shape, Y_batch.shape)
        lscalar = model.train_on_batch(X_batch, Y_batch)
        loss = loss + lscalar
        if (n+1) % 100 == 0:
            print ("batch: %d loss: %f " % (n+1, loss / 100))
            loss = 0
    score = model.evaluate(X_test, Y_test, verbose=0)
    print('Test score:', score)

json_string = model.to_json()
open('mlp_architecture.json', 'w').write(json_string)
model.save_weights('mlp_weights.h5', overwrite=True)
