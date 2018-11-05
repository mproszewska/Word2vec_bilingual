import math
import os
import random
import zipfile
import re
from os.path import isfile, join

try:    from sklearn.manifold import TSNE
except: print("Please install sklearn, matplotlib, and scipy to visualize embeddings.")

import numpy as np
from six.moves import urllib
import tensorflow as tf 

vocabulary_size = 5000
num_steps = 100001 # Number of steps in training
num_words = 1000 # Number of words returned
embedding_size = 100  # Dimension of the embedding vector.
skip_window = 3  # How many words to consider left and right.
num_skips = 2  # How many times to reuse an input to generate a label.
min_words = 1 # Minimal number of words needed to start
batch_size = 32
learning_rate = 0.1

# Random validation set to sample nearest neighbors.
valid_size = 16  # Random set of words to evaluate similarity on.
valid_window = 100  # Only pick dev samples in the head of the distribution.
valid_examples = np.random.choice(valid_window, valid_size, replace=False)
num_sampled = 64  # Number of negative examples to sample.

# TSNE  
tsne_perplexity = 30
tsne_n_components = 2
tsne_init="pca"
tsne_n_iter = 5000

def generate(foldername):
    # Read the data from file into a list of strings.
    def read_data(foldername):
        ret = []
        files = [f for f in os.listdir(foldername)]
        for filename in files:
            with open(foldername+"/"+filename) as f:
                data = f.read().lower().split()
                for d in data: ret.append(re.sub("[,.?!:;()\"]","",d))
        return ret

    words = read_data(foldername)
    if len(words) < min_words: return [],[],[]

    # Build the dictionary and replace rare words with UNK token.
    def build_dataset(words, vocabulary_size):
        count = [['UNK', -1]]
        count.extend(collections.Counter(words).most_common(vocabulary_size - 1))
        dictionary = dict()
        for word, _ in count:
            dictionary[word] = len(dictionary)
        data = []
        unk_count = 0
        for word in words:
            if word in dictionary:
                index = dictionary[word]
            else:
                index = 0  # dictionary['UNK']
                unk_count += 1
            data.append(index)
        count[0][1] = unk_count
        reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
        return data, count, dictionary, reverse_dictionary

    data, count, dictionary, reverse_dictionary = build_dataset(words, vocabulary_size)
    del words

    # Function to generate a training batch for the skip-gram model.
    data_index = 0
    def generate_batch(batch_size, num_skips, skip_window):
        nonlocal data_index
        assert batch_size % num_skips == 0
        assert num_skips <= 2 * skip_window
        batch = np.ndarray(shape=(batch_size), dtype=np.int32)
        labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
        span = 2 * skip_window + 1  # neighbourhood
        buffer = collections.deque(maxlen=span)
        if data_index + span > len(data):
            data_index = 0
        buffer.extend(data[data_index:data_index + span])
        data_index += span
        for i in range(batch_size // num_skips):
            context_words = [w for w in range(span) if w != skip_window]
            words_to_use = random.sample(context_words, num_skips)
            for j, context_word in enumerate(words_to_use):
                batch[i * num_skips + j] = buffer[skip_window]
                labels[i * num_skips + j, 0] = buffer[context_word]
            if data_index == len(data):
                buffer.extend(data[0:span])
                data_index = span
            else:
                buffer.append(data[data_index])
                data_index += 1
        # Backtrack to avoid skipping words in the end of a batch
        data_index = (data_index + len(data) - span) % len(data)
        return batch, labels

    # Build and train a skip-gram model.
    graph = tf.Graph()
    with graph.as_default():
        # Input data.
        train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
        train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
        valid_dataset = tf.constant(valid_examples, dtype=tf.int32)

        # Ops and variables pinned to the CPU because of missing GPU implementation
        with tf.device('/cpu:0'):
            # Look up embeddings for inputs.
            embeddings = tf.Variable(tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
            embed = tf.nn.embedding_lookup(embeddings, train_inputs)

            # Construct the variables for the NCE loss
            nce_weights = tf.Variable(
                tf.truncated_normal([vocabulary_size, embedding_size],
                                    stddev=1.0 / math.sqrt(embedding_size)))
            nce_biases = tf.Variable(tf.zeros([vocabulary_size]))

        # Compute the average NCE loss for the batch.
        # tf.nce_loss automatically draws a new sample of the negative labels each
        # time we evaluate the loss.
        loss = tf.reduce_mean(
            tf.nn.nce_loss(weights=nce_weights,
                           biases=nce_biases,
                           labels=train_labels,
                           inputs=embed,
                           num_sampled=num_sampled,
                           num_classes=vocabulary_size))

        # Construct the SGD optimizer using a learning rate
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(loss)

        # Compute the cosine similarity between minibatch examples and all embeddings.
        norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keepdims=True))
        normalized_embeddings = embeddings / norm
        valid_embeddings = tf.nn.embedding_lookup(
            normalized_embeddings, valid_dataset)
        similarity = tf.matmul(
            valid_embeddings, normalized_embeddings, transpose_b=True)

        # Add variable initializer.
        init = tf.global_variables_initializer()

    # Begin training.
    with tf.Session(graph=graph) as session:
        # We must initialize all variables before we use them.
        init.run()

        for step in range(num_steps):
            batch_inputs, batch_labels = generate_batch(
                batch_size, num_skips, skip_window)
            feed_dict = {train_inputs: batch_inputs, train_labels: batch_labels}
            session.run([optimizer, loss], feed_dict=feed_dict)

        final_embeddings = normalized_embeddings.eval()

    #  Generating embeddings with lower dim in order to visualize results
    tsne = TSNE(perplexity=tsne_perplexity, n_components=tsne_n_components, init=tsne_init, n_iter=tsne_n_iter)
    low_dim_embeddings = tsne.fit_transform(final_embeddings)
    return [reverse_dictionary[i] for i in range(len(reverse_dictionary))], final_embeddings, low_dim_embeddings

# Generate two vector spaces from sources

def start():
    # Return result if already generated
    bLabels,bEmbeddings,bLow_dim_embeddings = generate("sources/blue/")
    rLabels, rEmbeddings, rLow_dim_embeddings = generate("sources/red")

    return [bLabels,bEmbeddings,bLow_dim_embeddings],[rLabels,rEmbeddings,rLow_dim_embeddings]