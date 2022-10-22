import numpy as np
import random


class Dataset:

    def __init__(self, fname, source="stanford") -> None:
        self.fname = fname
        self.source = source
        # parse the file to a dataset member variable
        self.dataset = self.read_file_to_dataset()
        # get vocab list and vocab size
        self.vocabulary, self.vocabulary_size = self.get_vocabulary()
        # get unique integer to word mappings
        self.word_map = self.get_mappings()
        # get our word counts
        self.word_counts = self.get_word_counts()
        # augment the data to artificially create more data
        self.augmented_data = self.augment_data()
        # generate random context and a center word
        self.context = self.get_random_context()

        # (optional) make the len function of our Dataset instance
        # to return the len of self.dataset. This just makes it
        # a little more pythonic
        self.size = len(self.dataset)


    def __len__(self):
        return self.size
    
    def read_file_to_dataset(self):
        print("CONVERTING FILE TO DATASET")
        sentences = []
        reviews = open(self.fname).readlines()
        n_reviews = len(reviews)
        first = self.source == "stanford"
        offset = int(first)

        for line in range(n_reviews):
            if first:
                first = False
                continue
            # list of lowered words from a sentence
            sentence = [w.lower() for w in reviews[line].split()[offset:]]
            sentences.append(sentence)
        print(f"Compiled list of {len(sentences)} sentences")
        return sentences

    def get_vocabulary(self):
        '''
        interate through the sentences and the the words of each
        sentence and if the word doesnt exist in our vocabulary
        it is added to the list
        '''
        print("TABULATING VOCABULARY")
        vocabulary = []
        for sentence in self.dataset:
            for word in sentence:
                if word not in vocabulary:
                    vocabulary.append(word)
                
        vocab_size = len(vocabulary)
        print(f"Found {vocab_size} distinct words")
        return vocabulary, vocab_size
    
    def get_mappings(self):
        '''
        Mapping words to integer endices to be stored in a dictionary
        '''
        print("CREATING MAPPING")
        mapping = {}
        index = 0 
        for word in self.vocabulary:
            mapping[word] = index
            index += 1
        return mapping
    
    def get_word_counts(self):
        '''
        Creates a dictionary with keys of every word and values of
        how often they appear in the dataset
        '''
        word_counts = {}
        count = 0

        for word in self.vocabulary:
            # make sure we have all words in our words
            # count data structure and it's value is set 
            # to zero
            word_counts[word] = 0
        
        for sentence in self.dataset:
            for word in sentence:
                word_counts[word] += 1

        return word_counts

    def augment_data(self, threshold=1e-5, N=30, min_length=3):
        print("AUGMENTING DATA")
        num_words = 0
        for word in self.word_counts:
            num_words += self.word_counts[word]
        
        reject_prob = np.zeros((self.vocabulary_size,), dtype=np.float32)

        for idx, x in enumerate(self.vocabulary):
            frequency = self.word_counts[word] / num_words
            reject_prob[idx] = max(0, 1 - np.sqrt(threshold/frequency))
        
        # iterate over the dataset N times and each time 
        # construct new sentences applying the rejection fuction,
        # also checking the word count of a new sentence is greater
        # than min_length 
        all_sentences = []
        for sentence in self.dataset * N:
            new_sentence = []
            for word in sentence:
                # if the rejection probability is 0 or greater than a random number,
                # it is appended to the new sentence 
                if reject_prob[self.word_map[word]] == 0 or random.random() >= reject_prob[self.word_map[word]]:
                    new_sentence.append(word)

            if len(new_sentence) >= min_length:
                all_sentences.append(new_sentence)
        return all_sentences

    def get_random_context(self, window=5):
        '''
        Generate center words and contexts. This program is 
        using the skip-gram techinque; attempting to predict context
        given a center word. Context being a small window of n words
        surrounding the center word.
        '''
        random_index = random.randint(0, len(self.augmented_data)-1)
        sentence = self.augmented_data[random_index]

        # pick a random context length, between 1 and the context window
        # and if it's too long, then a new context length will be chosen
        
        random_context_length = random.randint(1, window)
        # will never execute if the context length is not too large
        while len(sentence) < 2 * random_context_length + 1:
            random_context_length = random.randint(1, window)

        # get center word from sentence
        center_word_idx = random.randint(random_context_length, 
        len(sentence) - random_context_length)

        # considering a sentence of some length, there must be enough
        # space within the setence to accomodate random context length
        low_bound = center_word_idx - random_context_length
        # upper limit is exclusive so 1 is added to the high bound
        high_bound = center_word_idx + random_context_length + 1 
        context = sentence[low_bound:high_bound]
        center_word = sentence[center_word_idx]
        context.remove(center_word)

        return center_word, context

