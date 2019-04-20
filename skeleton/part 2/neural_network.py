import numpy as np
import math

"""
    Minigratch Gradient Descent Function to train model
    1. Format the data
    2. call four_nn function to obtain losses
    3. Return all the weights/biases and a list of losses at each epoch
    Args:
        epoch (int) - number of iterations to run through neural net
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - starting weights
        x_train (np array) - (n,d) numpy array where d=number of features
        y_train (np array) - (n,) all the labels corresponding to x_train
        num_classes (int) - number of classes (range of y_train)
        shuffle (bool) - shuffle data at each epoch if True. Turn this off for testing.
    Returns:
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - resulting weights
        losses (list of ints) - each index should correspond to epoch number
            Note that len(losses) == epoch
    Hints:
        Should work for any number of features and classes
        Good idea to print the epoch number at each iteration for sanity checks!
        (Stdout print will not affect autograder as long as runtime is within limits)
"""
def minibatch_gd(epoch, w1, w2, w3, w4, b1, b2, b3, b4, x_train, y_train, num_classes, shuffle=True):

    batch_size = 200
    losses = []
    
    for e in range(epoch):
        print("Epoch " + str(e))
        if shuffle:
            rand = np.random.get_state()
            np.random.shuffle(x_test)
            np.random.set_state(rand)
            np.random.shuffle(y_test)
        for i in range(len(y_train)//batch_size):
            loss = four_nn(x_train, w1, w2, w3, w4, b1, b2, b3, b4, y_train)

        losses.append(loss)

    return w1, w2, w3, w4, b1, b2, b3, b4, losses

"""
    Use the trained weights & biases to see how well the nn performs
        on the test data
    Args:
        All the weights/biases from minibatch_gd()
        x_test (np array) - (n', d) numpy array
        y_test (np array) - (n',) all the labels corresponding to x_test
        num_classes (int) - number of classes (range of y_test)
    Returns:
        avg_class_rate (float) - average classification rate
        class_rate_per_class (list of floats) - Classification Rate per class
            (index corresponding to class number)
    Hints:
        Good place to show your confusion matrix as well.
        The confusion matrix won't be autograded but necessary in report.
"""
def test_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test, y_test, num_classes):

    avg_class_rate = 0.0
    class_rate_per_class = [0.0] * num_classes
    return avg_class_rate, class_rate_per_class

"""
    4 Layer Neural Network
    Helper function for minibatch_gd
    Up to you on how to implement this, won't be unit tested
    Should call helper functions below
"""
def four_nn(x_train, w1, w2, w3, w4, b1, b2, b3, b4, y_train):

    z1, acache1 = affine_forward(X, w1, b1)
    a1, rcache1 = relu_forward(z1)
    z2, acache2 = affine_forward(a1, w2, b2)
    a2, rcache2 = relu_forward(z2)
    z3, acache3 = affine_forward(a2, w3, b3)
    a3, rcache3 = relu_forward(z3)
    F, acache4 = affine_forward(a3, w4, b4)

    loss, dF = cross_entropy(F, y_train)

    da3, dw4, db4 = affine_backward(dF, acache4)
    dz3 = relu_backward(da3, rcache3)
    da2, dw3, db3 = affine_backward(dz3, acache3)
    dz2 = relu_backward(da2, acache2)
    da1, dw2, db2 = affine_backward(dz2, acache2)
    dz1 = relu_backward(da1, acache1)
    dX, dw1, db1 = affine_backward(dz1, acache1)

    eta = 0.1
    w1 = w1 - eta*dw1
    w2 = w2 - eta*dw2
    w3 = w3 - eta*dw3
    w4 = w4 - eta*dw4

    return loss

"""
    Next five functions will be used in four_nn() as helper functions.
    All these functions will be autograded, and a unit test script is provided as unit_test.py.
    The cache object format is up to you, we will only autograde the computed matrices.

    Args and Return values are specified in the MP docs
    Hint: Utilize numpy as much as possible for max efficiency.
        This is a great time to review on your linear algebra as well.
"""
def affine_forward(A, W, b):

    Z = np.matmul(A, W)

    for j in range(Z.shape[1]):
        Z[:,j] += b[j]
    
    return Z, (A, W, b)

def affine_backward(dZ, cache):

    W = cache[1]
    A = cache[0]
    b= cache[2]

    dA = np.matmul(dZ, np.transpose(W))
    dW = np.matmul(np.transpose(A), dZ)
    db = dZ.sum(axis=0)
    
    return dA, dW, db

def relu_forward(Z):
    
    Z = Z.clip(min=0)
    
    return Z, np.copy(Z)

def relu_backward(dA, cache):

    for i in range(dA.shape[0]):
        for j in range(dA.shape[1]):
            if cache[i, j] == 0:
                dA[i, j]  = 0
    
    return dA

def cross_entropy(F, y):

    n = len(y)

    F_columns = [np.sum( math.e**F[i,:] ) for i in range(n)]

    outer_sum = sum([F[i, int(y[i])] - math.log(F_columns[i]) for i in range(n)])
    L = (-1/n)*outer_sum

    dF = np.zeros(F.shape)
    for i in range(F.shape[0]):
        for j in range(F.shape[1]):
            left = 0
            if j == int(y[i]):
                left = 1
            dF[i, j] = (-1/n) * ( left - math.exp(F[i, j])/F_columns[i] )
    
    
    return L, dF
