# TextClassifier.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Dhruv Agarwal (dhruva2@illinois.edu) on 02/21/2019
import math

"""
You should only modify code within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
class TextClassifier(object):
    def __init__(self):
        """Implementation of Naive Bayes for multiclass classification

        :param lambda_mixture - (Extra Credit) This param controls the proportion of contribution of Bigram
        and Unigram model in the mixture model. Hard Code the value you find to be most suitable for your model
        """
        self.lambda_mixture = 0.0
        self.prior = {} #index: classnum
        self.likelihood = {} #index: word, classnum
        self.bigram_likelihood = {} #index (word, word) transition, classnum

    def fit(self, train_set, train_label):
        """
        :param train_set - List of list of words corresponding with each text
            example: suppose I had two emails 'i like pie' and 'i like cake' in my training set
            Then train_set := [['i','like','pie'], ['i','like','cake']]

        :param train_labels - List of labels corresponding with train_set
            example: Suppose I had two texts, first one was class 0 and second one was class 1.
            Then train_labels := [0,1]
        """

        
        k = 1
        training_count = len(train_label)

        class_counts = {} #index: class num
        words_per_class = {} #index: class num
        transitions_per_class = {} #index: classnum
        word_counts = {} #index: (word, classnum)
        transition_counts = {} #index: (transition, classnum)
        words = set()
        transitions = set()

        for i in range(training_count):
            label = train_label[i]
            class_counts[label] = class_counts.get(label, 0) + 1
            
            document = train_set[i]
            words_per_class[label] = words_per_class.get(label, 0) + len(document)
            transitions_per_class[label] = transitions_per_class.get(label, 0) + len(document) - 1
            
            for word in document:
                words.add(word)
                index = (word, label)
                word_counts[index] = word_counts.get(index, 0) + 1

            for i in range(1, len(document)):
                transition = (document[i-1], document[i])
                transitions.add(transition)
                index = (transition, label)
                transition_counts[index] = transition_counts.get(index, 0) + 1

        for i in class_counts.keys():
            self.prior[i] = math.log(class_counts[i]/training_count)

        for word in words:
            for classnum in class_counts.keys():
                index = (word, classnum)
                self.likelihood[word, classnum] = math.log( (word_counts.get(index, 0)+k) / (words_per_class[classnum] + k*len(words)) )

        for transition in transitions:
            for classnum in class_counts.keys():
                index = (transition, classnum)
                self.bigram_likelihood[transition, classnum] = math.log( (transition_counts.get(index, 0)+k) / (transitions_per_class[classnum] + k*len(transitions)) )

#        for classnum in class_counts.keys():
#            likely_words = []
#            for word, label in self.likelihood.keys():
#                if label == classnum:
#                    likely_words.append((self.likelihood[word, label], word))
#
#            print(str(classnum) + ":")
#            print(sorted(likely_words, key = lambda x: -x[0])[:20])
            

    def predict(self, x_set, dev_label, lambda_mix=0.0):
        """
        :param dev_set: List of list of words corresponding with each text in dev set that we are testing on
              It follows the same format as train_set
        :param dev_label : List of class labels corresponding to each text
        :param lambda_mix : Will be supplied the value you hard code for self.lambda_mixture if you attempt extra credit

        :return:
                accuracy(float): average accuracy value for dev dataset
                result (list) : predicted class for each text
        """

        test_set = x_set
        test_label = dev_label
        
        class_labels = self.prior.keys()
        pred_label = []

#        word_counts = {}

        for i in range(len(test_set)):
            document = test_set[i]
            true_label = test_label[i]
            maximum_value = float('-inf')
            maximum_class = -1

#            for word in document:
#                word_counts[word, true_label] = word_counts.get((word, true_label), 0) + 1
            
            for classnum in class_labels:
                posterior_probability = self.prior[classnum]
                for word in document:
                    if (word, classnum) in self.likelihood:
                        posterior_probability = posterior_probability + self.likelihood[word, classnum]

                bigram_posterior = self.prior[classnum] + self.likelihood.get((document[0], classnum), 0)
                for i in range(1, len(document)):
                    transition = (document[i-1], document[i])
                    if (transition, classnum) in self.bigram_likelihood:
                        bigram_posterior = bigram_posterior + self.bigram_likelihood[transition, classnum]
                   
                combined_posterior = (1 - lambda_mix) * posterior_probability + lambda_mix * bigram_posterior
                if combined_posterior > maximum_value:
                    maximum_value = combined_posterior
                    maximum_class = classnum

            pred_label.append(maximum_class)
                

        accuracy = len([i for i in range(len(test_set)) if pred_label[i] == test_label[i]])/len(test_set)

#        for classnum in class_labels:
#            likely_words = []
#            for word, label in word_counts.keys():
#                if (label == classnum):
#                    likely_words.append((word_counts[word, label], word))
#
#            print(str(classnum) + ":")
#            print (sorted(likely_words, key = lambda x: -x[0])[:5])

        return accuracy, pred_label

