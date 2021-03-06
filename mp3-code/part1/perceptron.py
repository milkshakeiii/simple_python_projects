import numpy as np
#import matplotlib.pyplot as plt

class MultiClassPerceptron(object):
    def __init__(self,num_class,feature_dim):
        """Initialize a multi class perceptron model. 

        This function will initialize a feature_dim weight vector,
        for each class. 

        The LAST index of feature_dim is assumed to be the bias term,
            self.w[:,0] = [w1,w2,w3...,BIAS] 
            where wi corresponds to each feature dimension,
            0 corresponds to class 0.  

        Args:
            num_class(int): number of classes to classify
            feature_dim(int): feature dimension for each example 
        """

        self.w = np.zeros((feature_dim+1,num_class))

    def train(self,train_set,train_label):
        """ Train perceptron model (self.w) with training dataset. 

        Args:
            train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
            train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
        """
        
        n = 1
        iterations = 1

        for itr in range(iterations):
            updates = 0
            rand = np.random.get_state()
            np.random.shuffle(train_set)
            np.random.set_state(rand)
            np.random.shuffle(train_label)
            for i in range(len(train_set)):
                item = train_set[i]
                item = np.append(item, 1)
                label = train_label[i]

#                predicted_label = self.decide(item, {}, -1, -1)
                predicted_label = self.decide(item)
                if predicted_label != label:
                    updates += 1
                    self.w[:,label] = self.w[:,label] + item * n
                    self.w[:,predicted_label] = self.w[:,predicted_label] - item * n

            #print ("updates:" + str(updates))
            
#    def decide(self, feature_vector, high_low_probability_per_class, true_label, itemno):
    def decide(self, feature_vector):
        best_class = -1
        best_dot = float('-inf')
        for current_class in range(self.w.shape[1]):
            weight_vector = self.w[:,current_class]
            dot = np.dot(feature_vector, weight_vector)
            if dot > best_dot:
                best_dot = dot
                best_class = current_class

#            if (current_class == true_label and dot > high_low_probability_per_class[current_class, True][2]):
#                high_low_probability_per_class[current_class, True] = (feature_vector, itemno, dot)
#            if (current_class == true_label and dot < high_low_probability_per_class[current_class, False][2]):
#                high_low_probability_per_class[current_class, False] = (feature_vector, itemno, dot)

        return best_class

    def test(self,test_set,test_label):
        """ Test the trained perceptron model (self.w) using testing dataset. 
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
#        for classnum in range(self.w.shape[1]):
#            high_low_probability_per_class[classnum, True] = (None, None, float('-inf'))
#            high_low_probability_per_class[classnum, False] = (None, None, float('inf'))

        for i in range(len(test_set)):
            item = test_set[i]
            item = np.append(item, 1)
            true_label = test_label[i]
            pred_label.append(self.decide(item))
#            pred_label.append(self.decide(item, high_low_probability_per_class, true_label, i))

        accuracy = len([i for i in range(len(test_set)) if pred_label[i] == test_label[i]])/len(test_set)

#        for classnum in range(self.w.shape[1]):
#            print("--class " + str(classnum) + "--")
#            print("high probability index: " + str(high_low_probability_per_class[classnum, True][1]) + " value: " + str(high_low_probability_per_class[classnum, True][2]))
#            item = high_low_probability_per_class[classnum, True][0][:784]
#            fig, ax = plt.subplots(1, 2, figsize=(12, 5))
#            ax[0].imshow(item.reshape((28, 28)), cmap=None)
#            ax[0].set_xticks([])
#            ax[0].set_yticks([])
#            ax[0].set_title("(high) class " + str(classnum))
#            print("low probability index: " + str(high_low_probability_per_class[classnum, False][1]) + " value: " + str(high_low_probability_per_class[classnum, False][2]))
#            item = high_low_probability_per_class[classnum, False][0][:784]
#            ax[1].imshow(item.reshape((28, 28)), cmap=None)
#            ax[1].set_xticks([])
#            ax[1].set_yticks([])
#            ax[1].set_title("(low) class " + str(classnum))
#            plt.show()

#        print("Accuraccy: " + str(accuracy))
        return accuracy, pred_label

    def save_model(self, weight_file):
        """ Save the trained model parameters 
        """ 

        np.save(weight_file,self.w)

    def load_model(self, weight_file):
        """ Load the trained model parameters 
        """ 

        self.w = np.load(weight_file)

