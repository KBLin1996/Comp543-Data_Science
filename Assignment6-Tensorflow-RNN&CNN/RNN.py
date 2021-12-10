import numpy as np
import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

# the number of iterations to train for
numTrainingIters = 10000

# the number of hidden neurons that hold the state of the RNN
hiddenUnits = 500

# the number of classes that we are learning over
numClasses = 3

# the number of data points in a batch
batchSize = 100

# this function takes a dictionary (called data) which contains 
# of (dataPointID, (classNumber, matrix)) entries.  Each matrix
# is a sequence of vectors; each vector has a one-hot-encoding of
# an ascii character, and the sequence of vectors corresponds to
# one line of text.  classNumber indicates which file the line of
# text came from.  
# 
# The argument maxSeqLen is the maximum length of a line of text
# seen so far.  fileName is the name of a file whose contents
# we want to add to data.  classNum is an indicator of the class
# we are going to associate with text from that file.  linesToUse
# tells us how many lines to sample from the file.
#
# The return val is the new maxSeqLen, as well as the new data
# dictionary with the additional lines of text added


# (maxSeqLen, data) = addToData (maxSeqLen, data, "Holmes.txt", 0, 10000)
# (maxSeqLen, data) = addToData (maxSeqLen, data, "war.txt", 1, 10000)
# (maxSeqLen, data) = addToData (maxSeqLen, data, "william.txt", 2, 10000)


def addToData(maxSeqLen, data, fileName, classNum, linesToUse):
    # open the file and read it in
    with open(fileName) as f:
        content = f.readlines()

    # sample linesToUse numbers; these will tell us what lines
    # from the text file we will use
    myInts = np.random.choice(len(content) - 1, linesToUse, replace=False)

    # i is the key of the next line of text to add to the dictionary
    i = len(data)

    # loop thru and add the lines of text to the dictionary
    for whichLine in myInts.flat:
        # get the line and ignore it if it has nothing in it
        line = content[whichLine]
        if line.isspace () or len(line) == 0:
            continue;

        # take note if this is the longest line we've seen
        if len (line) > maxSeqLen:
            maxSeqLen = len (line)

        # create the matrix that will hold this line
        temp = np.zeros((len(line), 256))

        # j is the character we are on
        j = 0

        # loop thru the characters
        for ch in line:

            # ignore non-ascii
            if ord(ch) >= 256:
                continue

            # one hot!
            temp[j][ord(ch)] = 1

            # move onto the next character
            j = j + 1

        # remember the line of text
        data[i] = (classNum, temp)
 
        # move onto the next line
        i = i + 1
    # and return the dictionary with the new data
    return (maxSeqLen, data)


# this function takes as input a data set encoded as a dictionary
# (same encoding as the last function) and pre-pends every line of
# text with empty characters so that each line of text is exactly
# maxSeqLen characters in size
def pad (maxSeqLen, data):
   # loop thru every line of text
   for i in data:
        # access the matrix and the label
        temp = data[i][1]
        label = data[i][0]

        # get the number of chatacters in this line
        len = temp.shape[0]

        # and then pad so the line is the correct length
        padding = np.zeros((maxSeqLen - len, 256))
        data[i] = (label, np.transpose (np.concatenate ((padding, temp), axis = 0)))
   # return the new data set
   return data


# this generates a new batch of training data of size batchSize from the
# list of lines of text data. This version of generateData is useful for
# an RNN because the data set x is a NumPy array with dimensions
# [batchSize, 256, maxSeqLen]; it can be unstacked into a series of
# matrices containing one-hot character encodings for each data point
# using tf.unstack(inputX, axis=2)
# Task 2
def generateDataRNN(maxSeqLen, data):
    # randomly sample batchSize lines of text
    myInts = np.random.choice(len(data) - 1, batchSize, replace=False)

    # i is how many line there are in this text, which it the channels of the shape
    # stack all of the text into a matrix of one-hot characters
    x = np.stack(data[i][1] for i in myInts.flat)

    # and stack all of the labels into a vector of labels
    y = np.stack(np.array((data[i][0])) for i in myInts.flat)

    # return the pair
    return (x, y)


# this also generates a new batch of training data, but it represents
# the data as a NumPy array with dimensions [batchSize, 256 * maxSeqLen]
# where for each data point, all characters have been appended.  Useful
# for feed-forward network training
# Task 3
def generateDataFeedForward(maxSeqLen, data):
    # randomly sample batchSize lines of text
    myInts = np.random.choice(len(data) - 1, batchSize, replace=False)

    # stack all of the text into a matrix of one-hot characters
    x = np.stack(data[i][1].flatten() for i in myInts.flat)

    # and stack all of the labels into a vector of labels
    y = np.stack(np.array((data[i][0])) for i in myInts.flat)

    # return the pair
    return (x, y)


# Task 4
def generateTimeWrapping(maxSeqLen, data):
    # Randomly sample batchSize lines of text
    myInts = np.random.choice(len(data) - 1, batchSize, replace=False)

    x = np.zeros((batchSize, 2560, maxSeqLen-9))
    cnt = 0
    for i in myInts.flat:
        tempX = list()
        for k in range(maxSeqLen-9):
            tempX.append(data[i][1][:, k:k+10].flatten())
        tempX = np.array(tempX)
        tempX = np.transpose(tempX)

        x[cnt] = tempX
        cnt += 1

    # and stack all of the labels into a vector of labels
    y = np.stack(np.array((data[i][0])) for i in myInts.flat)

    # return the pair
    return (x, y)


# Task 1~4
def randomData(randomList, data, train, test):
    i = len(train)
    j = len(test)
    for idx in range(len(data)):
        if idx in randomList: 
            test[j] = data[idx]
            j += 1
        else:
            train[i] = data[idx]
            i += 1

    return train, test


# create the data dictionary
maxSeqLen = 0
data = dict()
train = dict()
test = dict()

# load up the three data sets
(maxSeqLen, data) = addToData(maxSeqLen, data, "Holmes.txt", 0, 11000)
randomList = np.random.choice(len(data), 1000, replace=False)
train, test = randomData(randomList, data, train, test)
#print(f"Stage1: Train=>{len(train)}, Test=>{len(test)}")

data.clear()
(maxSeqLen, data) = addToData(maxSeqLen, data, "war.txt", 1, 11000)
randomList = np.random.choice(len(data), 1000, replace=False)
train, test = randomData(randomList, data, train, test)
#print(f"Stage2: Train=>{len(train)}, Test=>{len(test)}")

data.clear()
(maxSeqLen, data) = addToData(maxSeqLen, data, "william.txt", 2, 11000)
randomList = np.random.choice(len(data), 1000, replace=False)
train, test = randomData(randomList, data, train, test)
#print(f"Stage3: Train=>{len(train)}, Test=>{len(test)}")


# pad each entry in the dictionary with empty characters as needed so
# that the sequences are all of the same length
train = pad(maxSeqLen, train)
test = pad(maxSeqLen, test)
        
# now we build the TensorFlow computation... there are two inputs, 
# a batch of text lines and a batch of labels
# Task 0~2
#inputX = tf.placeholder(tf.float32, [batchSize, 256, maxSeqLen])

# Task 3
#inputX = tf.placeholder(tf.float32, [batchSize, 256 * maxSeqLen])

# Task 4
inputX = tf.placeholder(tf.float32, [batchSize, 256 * 10, maxSeqLen-9])
inputY = tf.placeholder(tf.int32, [batchSize])

# this is the inital state of the RNN, before processing any data
initialState = tf.placeholder(tf.float32, [batchSize, hiddenUnits])

# the weight matrix that maps the inputs and hidden state to a set of values
W = tf.Variable(np.random.normal(0, 0.05, (hiddenUnits + 256, hiddenUnits)), dtype=tf.float32)


# Task 2
W_time_wrap = tf.Variable(np.random.normal(0, 0.05, (hiddenUnits + hiddenUnits + 256, hiddenUnits)), dtype=tf.float32)

# Task 3
W_feed_forward = tf.Variable(np.random.normal(0, 0.05, (hiddenUnits + 256 * maxSeqLen, hiddenUnits)), dtype=tf.float32)

# Task 4 (8 CNN filters)
CNNfilter = tf.Variable(np.random.uniform(0.01, 1, (256 * 10, 8)), dtype=tf.float32)
W_CNN = tf.Variable(np.random.normal(0, 0.05, (hiddenUnits + 8, hiddenUnits)), dtype=tf.float32)


# bias for the hidden values
b = tf.Variable(np.zeros((1, hiddenUnits)), dtype=tf.float32)

# weights and bias for the final classification
W2 = tf.Variable(np.random.normal(0, 0.05, (hiddenUnits, numClasses)),dtype=tf.float32)
b2 = tf.Variable(np.zeros((1, numClasses)), dtype=tf.float32)

# For RNN
# unpack the input sequences so that we have "a series of matrices",
# each of which has a one-hot encoding of the current character from
# every input sequence
# For Task 2 & 4
sequenceOfLetters = tf.unstack(inputX, axis=2)


'''
# Task 2

# Use a queue to store the output for 10 time ticks later in the future
queue = list()
currentState = initialState
tenStateBefore = initialState

# A single timeTick is a character with a shape (batchSize, 256)
for timeTick in sequenceOfLetters:
    if len(queue) >= 10:
        tenStateBefore = queue.pop(0)
    # Concatenate (based on column (axis=1)) the state with the input, then compute the next state
    inputPlusState = tf.concat([timeTick, currentState, tenStateBefore], 1)
    next_state = tf.tanh(tf.matmul(inputPlusState, W_time_wrap) + b)
    currentState = next_state
    queue.append(currentState)
'''

'''
# Task 3
inputPlusState = tf.concat([inputX, initialState], 1)
next_state = tf.tanh(tf.matmul(inputPlusState, W_feed_forward) + b)
currentState = next_state
'''

# Task 4
# now we implement the forward pass
currentState = initialState
for timeTick in sequenceOfLetters:
    eightVal = tf.matmul(timeTick, CNNfilter)
    inputPlusState = tf.concat([eightVal, currentState], 1)
    next_state = tf.tanh(tf.matmul(inputPlusState, W_CNN) + b)
    currentState = next_state


# compute the set of outputs
outputs = tf.matmul(currentState, W2) + b2

predictions = tf.nn.softmax(outputs)

# compute the loss
losses = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=outputs, labels=inputY)
totalLoss = tf.reduce_mean(losses)

# use gradient descent to train
#trainingAlg = tf.train.GradientDescentOptimizer(0.02).minimize(totalLoss)
trainingAlg = tf.train.AdagradOptimizer(0.02).minimize(totalLoss)
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333)

# and train!!
with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
    # initialize everything
    sess.run(tf.global_variables_initializer())

    _finalState = np.zeros((batchSize, hiddenUnits))
    # and run the training iters
    for epoch in range(numTrainingIters):
        # get some data
        # Task 2
        #x, y = generateDataRNN(maxSeqLen, train)
        # Task 3
        #x, y = generateDataFeedForward(maxSeqLen, train)
        # Task 4
        x, y = generateTimeWrapping(maxSeqLen, train)

        # do the training epoch
        _currentState = np.zeros((batchSize, hiddenUnits))
        _totalLoss, _trainingAlg, _currentState, _predictions, _outputs = sess.run(
                [totalLoss, trainingAlg, currentState, predictions, outputs],
                feed_dict={
                    inputX:x,
                    inputY:y,
                    initialState:_currentState
                })

        if epoch == numTrainingIters - 1:
            _finalState = _currentState
        # just FYI, compute the number of correct predictions
        numCorrect = 0
        for i in range (len(y)):
           maxPos = -1
           maxVal = 0.0
           for j in range (numClasses):
               if maxVal < _predictions[i][j]:
                   maxVal = _predictions[i][j]
                   maxPos = j
           if maxPos == y[i]:
               numCorrect = numCorrect + 1
        # print out to the screen
        print("Step", epoch, "Loss", _totalLoss, "Correct", numCorrect, "out of", batchSize)


    # Testing
    numCorrect = 0
    avgTestLoss = 0.0

    predictIter = int(len(test) / batchSize)
    for epoch in range(predictIter):
        # Testing Data
        # Task 2
        #testX, testY = generateDataRNN(maxSeqLen, test)
        # Task 3
        #testX, testY = generateDataFeedForward(maxSeqLen, test)
        # Task 4
        testX, testY = generateTimeWrapping(maxSeqLen, test)

        # Do the testing
        _currentState = np.zeros((batchSize, hiddenUnits))
        _totalLoss, _trainingAlg, _currentState, _predictions, _outputs = sess.run(
                [totalLoss, trainingAlg, currentState, predictions, outputs],
                feed_dict={
                    inputX: testX,
                    inputY: testY,
                    initialState: _finalState
                })
        avgTestLoss += _totalLoss

        # Compute the number of correct predictions
        for i in range(len(testY)):
           maxPos = -1
           maxVal = 0.0
           for j in range(numClasses):
               if maxVal < _predictions[i][j]:
                   maxVal = _predictions[i][j]
                   maxPos = j
           if maxPos == testY[i]:
               numCorrect = numCorrect + 1
    print(f"\nLoss for 3000 randomly chosen documents is {avgTestLoss / predictIter}, number correct labels is {numCorrect} out of {len(test)}")
