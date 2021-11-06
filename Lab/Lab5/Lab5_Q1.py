# For your reference, here is the dictionary-based LDA for use with the first sub-problem.

import numpy as np
import time


# This returns a number whose probability of occurrence is p
def sampleValue(p):
    return np.flatnonzero(np.random.multinomial(1, p, 1))[0]


# There are 2000 words in the corpus
alpha = np.full(2000, .1)
# There are 100 topics
beta = np.full(100, .1)

# This gets us the probability of each word happening in each of the 100 topics
wordsInTopic = np.random.dirichlet(alpha, 100)
# wordsInCorpus[i] will be a dictionary that gives us the number of each word in the document
wordsInCorpus = {}

# Generate each doc
for doc in range(0, 50):
    # No words in this doc yet
    wordsInDoc = {}

    # Get the topic probabilities for this doc
    topicsInDoc = np.random.dirichlet(beta)

    # Generate each of the 2000 words in this document
    for word in range(0, 2000):
        # Select the topic and the word
        whichTopic = sampleValue(topicsInDoc)
        whichWord = sampleValue(wordsInTopic[whichTopic])

        # And record the word
        wordsInDoc[whichWord] = wordsInDoc.get(whichWord, 0) + 1
    # Now, remember this document
    wordsInCorpus[doc] = wordsInDoc

# Q1 Answer
start = time.time()
# coOccurrences will be a map where the key is a
# (wordOne, wordTwo) pair, and the value is the number of times
# those two words co-occurred in a document, so this will be a
# value between zero and 50
coOccurrences = {}

# now, have a nested loop that piles up coOccurrences
# YOUR CODE HERE
for doc in wordsInCorpus:
    for wordOne in wordsInCorpus[doc]:
        for wordTwo in wordsInCorpus[doc]:
            if wordOne <= wordTwo:
                if (wordOne, wordTwo) not in coOccurrences:
                    coOccurrences[(wordOne, wordTwo)] = 1
                else:
                    coOccurrences[(wordOne, wordTwo)] += 1

end = time.time()
print("Q1 Dictionary Implementation:", end - start)
