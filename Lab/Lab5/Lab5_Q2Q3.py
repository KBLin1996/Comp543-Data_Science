# And here is the array-based LDA for use with the second two.

import numpy as np
import time

# There are 2000 words in the corpus
alpha = np.full(2000, .1)

# There are 100 topics
beta = np.full(100, .1)

# This gets us the probability of each word happening in each of the 100 topics
wordsInTopic = np.random.dirichlet(alpha, 100)

# wordsInCorpus[i] will give us the vector of words in document i
wordsInCorpus = np.zeros((50, 2000))

# Generate each doc
for doc in range(0, 50):
    # Get the topic probabilities for this doc
    topicsInDoc = np.random.dirichlet(beta)
    # Assign each of the 2000 words in this doc to a topic
    wordsToTopic = np.random.multinomial(2000, topicsInDoc)
    # And generate each of the 2000 words
    for topic in range(0, 100):
        wordsFromCurrentTopic = np.random.multinomial(wordsToTopic[topic], wordsInTopic[topic])
        wordsInCorpus[doc] = np.add(wordsInCorpus[doc], wordsFromCurrentTopic)

# Q2 Answer
start = time.time()
# coOccurrences[i, j] will give the count of the number of times that
# word i and word j appear in the same document in the corpus
coOccurrences = np.zeros((2000, 2000))

# Now, have a nested loop that piles up coOccurrences
# YOUR CODE HERE
for doc in range(len(wordsInCorpus)):
    wordsInCorpus[doc] = np.clip(wordsInCorpus[doc], 0, 1)
    coOccurrences += np.outer(wordsInCorpus[doc], wordsInCorpus[doc])

end = time.time()
print("Q2 Numpy Vector Multiply:", end - start)

# Q3 Answer
start = time.time()
coOccurrences = np.zeros((2000, 2000))

# Now, create coOccurrences via a matrix multiply
# YOUR CODE HERE
for doc in range(len(wordsInCorpus)):
    wordsInCorpus[doc] = np.clip(wordsInCorpus[doc], 0, 1)
wordsInCorpusTrans = np.transpose(wordsInCorpus)
coOccurrences = np.dot(wordsInCorpusTrans, wordsInCorpus)

end = time.time()
print("Q3 Numpy Matrix Multiply:", end - start)
