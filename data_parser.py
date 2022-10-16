import numpy as np
import random

class Dataset:

    def __init__(self, fname, source="standford") -> None:
        self.fname = fname
        self.source = source
        # parse our file to a dataset member variable
        self.dataset = self.read_file_to_datast()
        # get vocab list and vocab size
        self.vocabulary, self.vocabulary_size = self.get_vocabulary_size()
        # get unique integer to word mappings
        self.word_map = self.get_mappings()
        # get our word counts
        self.word_counts = self.get_word_counts()

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
        first = self.source == "sanford"
        offset = int(first)

        for line in range(n_reviews):
            if first:
                first = False
                continue
            # list of lowered words from a sentence
            sentence = [w.lower() for w in reviews[line].split()[offset:]]
            sentences.append(sentence)
        print(f"conpiled list of {len(sentences)} sentences")
        return sentences