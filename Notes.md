## Data Augmentation 

The data consists of about 12,000 reviews, which is not enough to learn meaningful word vectors. We need to perform data augmentation to artificially create more information. When performing data augmentation is an image related task, one could add noise or apply transformations to the images and this could be sufficient augmentation, however with words, we can't simply as random words to our reviews as this would destroy hte syntactic relation between the words. Instead, we're going to duplicate the dataset and drop words randomly depending on their frequency. Words that are very common will have a higher probability of being dropped, whereas very uncommon words will have a lower probability of being dropped. This is meant to retain criticial information while artificially producing more data. 

To determine wether a word is dropped, we're going to **iterate through our vocabulary and assign a rejection probability to each word.** $$P_{\text{reject}}(w)=\text{max}(0, 1- \sqrt{ \frac{t}{f(w_i)} })$$
Where $f(w_i)$ is the frequency of a given word $\frac{N}{V_{\text{size}}}$, which is just the amount of a particular word divided by the amount of the words in the corpus. 

To augment the data, a new sentence will be created with fewer words by iterating through each word in the original sentence and comparing the rejection probability with a random number. We will only keep the sentences that we consider to be long, such as three or more words.

-----

