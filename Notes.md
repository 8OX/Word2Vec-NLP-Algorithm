## Data Augmentation 

The data consists of about 12,000 reviews, which is not enough to learn meaningful word vectors. We need to perform data augmentation to artificially create more information. When performing data augmentation is an image related task, one could add noise or apply transformations to the images and this could be sufficient augmentation, however with words, we can't simply as random words to our reviews as this would destroy hte syntactic relation between the words. Instead, we're going to duplicate the dataset and drop words randomly depending on their frequency. Words that are very common will have a higher probability of being dropped, whereas very uncommon words will have a lower probability of being dropped. This is meant to retain criticial information while artificially producing more data. 

To determine wether a word is dropped, we're going to **iterate through our vocabulary and assign a rejection probability to each word.** $$P_{\text{reject}}(w)=\text{max}(0, 1- \sqrt{ \frac{t}{f(w_i)} })$$
Where $f(w_i)$ is the frequency of a given word $\frac{N}{V_{\text{size}}}$, which is just the amount of a particular word divided by the amount of the words in the corpus. 

To augment the data, a new sentence will be created with fewer words by iterating through each word in the original sentence and comparing the rejection probability with a random number. We will only keep the sentences that we consider to be long, such as three or more words.


## Probabilities in Word2Vec

We want to calculate the probabities of getting certain arrangments of words within some context. In other words, we want to find the probability of some context word $W_x$ given a center word $W_c$ . $$P(W_x|W_c)$$

As an example, let's consider the setence: $$\text{"If life were predictable it would cease to be life"}$$
With a context window of two words, our context word would be have to start at $\text{"were"}$. Just like finding the likelyhood of returning four heads in a row during a coin toss would be $P(\text{head})^4 = \frac{1}{4}$, our likelyhood calculation is a muliplication of the probabilities of our center word given each context word. $$P(\text{were}|\text{If}) * P(\text{were}|\text{life})* P(\text{were}|\text{predictable}) * P(\text{were}|\text{it}) = P(A)$$
choosing the next context word $\text{"predictable"}$

$$P(\text{predictable}|\text{life}) * P(\text{predictable}|\text{were})* P(\text{predictable}|\text{it}) * P(\text{predictable}|\text{would}) = P(B)$$

Again, like the coin toss, a muliplication of probabilities

$$P(\text{"If life were predictable it would cease to be life"}) = P(A) * P(B)$$

To generalize, if we're going to calculate the likelyhood of a large body of text, it is given by multiplying the product over all the words in the corpus and the the product of the words in the context.

$$\text{Probability} = \prod_{ \text{corpus}}\prod_{ \text{ context}} P(W_x|W_c, \theta)$$

$\theta$ exists in here just to delcare that the probabilities depend on the components of the actual word vector. That means in the calculations, we're going to be taking multiple products of vector products and getting real numbers out. 

Instead of using a single vector representation as assumed above, **we will use two vector representations for each word in our implemenation**. This is because it makes more sense to have one vector for a word when it is a center word and another vector for when a word is a context or outside word. This doesn't doesn't change the mathematics. 

To summarize, we want to calculate the probability of a sequence of words appearing together which will depend our word vector components $\theta$. The probability of a sequence of words in a body of text is given by the double product over the corpus and each individual window of the probabilites of each word pairing within that window. 