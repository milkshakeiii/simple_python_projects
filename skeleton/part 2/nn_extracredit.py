from __future__ import absolute_import, division, print_function

import tensorflow as tf
import numpy as np

tf.logging.set_verbosity(tf.logging.INFO)


#created by following https://www.tensorflow.org/tutorials/estimators/cnn
#code nearly identical to code found in tutorial
def cnn_model_fn(features, labels, mode):

    input_layer = tf.reshape(features['x'], [-1, 28, 28, 1])
    
    conv1 = tf.layers.conv2d( inputs=input_layer,
                              filters=32,
                              kernel_size=[5, 5],
                              padding="same",
                              activation=tf.nn.relu)

    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

    conv2 = tf.layers.conv2d( inputs=pool1,
                              filters=64,
                              kernel_size=[5, 5],
                              padding="same",
                              activation=tf.nn.relu)

    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)


    pool2_flat = tf.reshape(pool2, [-1, 7 * 7 * 64])
    dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
    dropout = tf.layers.dropout(
      inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    logits = tf.layers.dense(inputs=dropout, units=10)

    predictions = {
      "classes": tf.argmax(input=logits, axis=1),
      "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)


    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())

        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)


    eval_metric_ops = {
      "accuracy": tf.metrics.accuracy(
          labels=labels, predictions=predictions["classes"])
    }
    return tf.estimator.EstimatorSpec(
      mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)




train_data = np.load("data/x_train.npy")
train_data = (train_data - np.mean(train_data, axis=0)) / np.std(train_data, axis=0)
train_labels = np.load("data/y_train.npy")
train_labels = train_labels.astype(np.int32)

eval_data = np.load("data/x_test.npy")
eval_data = (eval_data - np.mean(eval_data, axis=0))/np.std(eval_data, axis=0)
eval_labels = np.load("data/y_test.npy")
eval_labels = eval_labels.astype(np.int32)

# Create the Estimator
mnist_classifier = tf.estimator.Estimator(
    model_fn=cnn_model_fn, model_dir="/tmp/mnist_convnet_model")

# Set up logging for predictions
tensors_to_log = {"probabilities": "softmax_tensor"}

logging_hook = tf.train.LoggingTensorHook(
    tensors=tensors_to_log, every_n_iter=50)

# Train the model
train_input_fn = tf.estimator.inputs.numpy_input_fn(
    x={"x": train_data},
    y=train_labels,
    batch_size=100,
    num_epochs=None,
    shuffle=True)

# train one step and display the probabilties
mnist_classifier.train(
    input_fn=train_input_fn,
    steps=1,
    hooks=[logging_hook])

mnist_classifier.train(input_fn=train_input_fn, steps=1000)

eval_input_fn = tf.estimator.inputs.numpy_input_fn(
    x={"x": eval_data},
    y=eval_labels,
    num_epochs=1,
    shuffle=False)

eval_results = mnist_classifier.evaluate(input_fn=eval_input_fn)
print(eval_results)

predictions = mnist_classifier.predict(input_fn=eval_input_fn)
confusion = tf.confusion_matrix(labels=eval_labels, predictions=predictions, num_classes=10)
print(confusion)
