import math
import numpy as np
#import matplotlib.pyplot as plt

class NaiveBayes(object):
    def __init__(self,num_class,feature_dim,num_value):
        """Initialize a naive bayes model. 

        This function will initialize prior and likelihood, where 
        prior is P(class) with a dimension of (# of class,)
            that estimates the empirical frequencies of different classes in the training set.
        likelihood is P(F_i = f | class) with a dimension of 
            (# of features/pixels per image, # of possible values per pixel, # of class),
            that computes the probability of every pixel location i being value f for every class label.  

        Args:
            num_class(int): number of classes to classify
            feature_dim(int): feature dimension for each example 
            num_value(int): number of possible values for each pixel 
        """

        self.num_value = num_value
        self.num_class = num_class
        self.feature_dim = feature_dim

        self.prior = np.zeros((num_class))
        self.likelihood = np.zeros((feature_dim,num_value,num_class))

    def train(self,train_set,train_label):
        """ Train naive bayes model (self.prior and self.likelihood) with training dataset. 
            self.prior(numpy.ndarray): training set class prior (in log) with a dimension of (# of class,),
            self.likelihood(numpy.ndarray): traing set likelihood (in log) with a dimension of 
                (# of features/pixels per image, # of possible values per pixel, # of class).
            You should apply Laplace smoothing to compute the likelihood. 

        Args:
            train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
            train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
        """

        k = 0.1
        training_count = len(train_label)
        pixel_count = self.feature_dim
        shade_count = self.num_value
        class_count = self.num_class

        class_counts = {} #index: class num
        pixel_counts = {} #index: (pixelnum, shade, classnum)

        for i in range(training_count):
            label = train_label[i]
            class_counts[label] = class_counts.get(label, 0) + 1
            
            image = train_set[i]
            for j in range(len(image)):
                shade = image[j]
                index = (j, shade, label)
                pixel_counts[index] = pixel_counts.get(index, 0) + 1

        for i in class_counts.keys():
            self.prior[i] = math.log(class_counts[i]/training_count)

        for pixelnum in range(pixel_count):
            for shade in range(shade_count):
                for classnum in range(class_count):
                    index = (pixelnum, shade, classnum)

                    self.likelihood[pixelnum, shade, classnum] = math.log( (pixel_counts.get(index, 0)+k) / (class_counts[classnum] + k*pixel_count) )

    def test(self,test_set,test_label):
        """ Test the trained naive bayes model (self.prior and self.likelihood) on testing dataset,
            by performing maximum a posteriori (MAP) classification.  
            The accuracy is computed as the average of correctness 
            by comparing between predicted label and true label. 

        Args:
            test_set(numpy.ndarray): testing examples with a dimension of (# of examples, feature_dim)
            test_label(numpy.ndarray): testing labels with a dimension of (# of examples, )

        Returns:
            accuracy(float): average accuracy value  
            pred_label(numpy.ndarray): predicted labels with a dimension of (# of examples, )
        """    
        pred_label = []
#        high_low_probability_per_class = {}
#        for classnum in range(self.num_class):
#            high_low_probability_per_class[classnum, True] = (None, None, float('-inf'))
#            high_low_probability_per_class[classnum, False] = (None, None, float('inf'))

        for itemno in range(len(test_set)):
            item = test_set[itemno]
            true_label = test_label[itemno]
            maximum_value = float('-inf')
            maximum_class = -1
            
            for classnum in range(self.num_class):
                posterior_probability = self.prior[classnum]
                for i in range(self.feature_dim):
                    posterior_probability = posterior_probability + self.likelihood[i, item[i], classnum]
                if posterior_probability > maximum_value:
                    maximum_value = posterior_probability
                    maximum_class = classnum

#                if (classnum == true_label and posterior_probability > high_low_probability_per_class[classnum, True][2]):
#                    high_low_probability_per_class[classnum, True] = (item, itemno, posterior_probability)
#                if (classnum == true_label and posterior_probability < high_low_probability_per_class[classnum, False][2]):
#                    high_low_probability_per_class[classnum, False] = (item, itemno, posterior_probability)

            pred_label.append(maximum_class)
                

        accuracy = len([i for i in range(len(test_set)) if pred_label[i] == test_label[i]])/len(test_set)
#        print("Accuracy: " + str(accuracy))

#        for classnum in range(self.num_class):
#            print("--class " + str(classnum) + "--")
#            print("high probability index: " + str(high_low_probability_per_class[classnum, True][1]) + " value: " + str(high_low_probability_per_class[classnum, True][2]))
#            item = high_low_probability_per_class[classnum, True][0]
#            fig, ax = plt.subplots(1, 2, figsize=(12, 5))
#            ax[0].imshow(item.reshape((28, 28)), cmap="Greys")
#            ax[0].set_xticks([])
#            ax[0].set_yticks([])
#            ax[0].set_title("(high) class " + str(classnum))
#            print("low probability index: " + str(high_low_probability_per_class[classnum, False][1]) + " value: " + str(high_low_probability_per_class[classnum, False][2]))
#            item = high_low_probability_per_class[classnum, False][0]
#            ax[1].imshow(item.reshape((28, 28)), cmap="Greys")
#            ax[1].set_xticks([])
#            ax[1].set_yticks([])
#            ax[1].set_title("(low) class " + str(classnum))
#            plt.show()
        
        return accuracy, pred_label


    def save_model(self, prior, likelihood):
        """ Save the trained model parameters 
        """    

        np.save(prior, self.prior)
        np.save(likelihood, self.likelihood)

    def load_model(self, prior, likelihood):
        """ Load the trained model parameters 
        """ 

        self.prior = np.load(prior)
        self.likelihood = np.load(likelihood)

    def intensity_feature_likelihoods(self, likelihood):
        """
        Get the feature likelihoods for high intensity pixels for each of the classes,
            by sum the probabilities of the top 128 intensities at each pixel location,
            sum k<-128:255 P(F_i = k | c).
            This helps generate visualization of trained likelihood images. 
        
        Args:
            likelihood(numpy.ndarray): likelihood (in log) with a dimension of
                (# of features/pixels per image, # of possible values per pixel, # of class)
        Returns:
            feature_likelihoods(numpy.ndarray): feature likelihoods for each class with a dimension of
                (# of features/pixels per image, # of class)
        """
        
        feature_likelihoods = np.zeros((likelihood.shape[0],likelihood.shape[2]))

        for classnum in range(self.num_class):
            for pixelnum in range(self.feature_dim):
                shade_sum = 0
                for shade in range(128, 256):
                    shade_sum += math.exp(self.likelihood[pixelnum, shade, classnum])
                feature_likelihoods[pixelnum, classnum] = math.exp(shade_sum)

        return feature_likelihoods
