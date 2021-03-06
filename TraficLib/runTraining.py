import time
import os.path
import tensorflow as tf
import numpy as np
import networkDef as nn
import argparse
import sys
from fiberfileIO import *
YELLOW = "\033[0;33m"
NC = "\033[0m"
flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_float('learning_rate', 0.001, 'Initial learning rate.')
flags.DEFINE_integer('num_epochs', 3, 'Number of epochs to run trainer.')
flags.DEFINE_integer('num_hidden', 1024, 'Number of hidden layers.')
flags.DEFINE_integer('batch_size', 5, 'Batch size.')
flags.DEFINE_string('data_dir', '',
                    'Directory with the training data.')
flags.DEFINE_string('checkpoint_dir', '',
                    """Directory where to write model checkpoints.""")
flags.DEFINE_string('summary_dir', '',
                    """Directory where to write summary.""")
flags.DEFINE_boolean('multiclass', False,
                         """Whether Multiclassification or Biclassification.""")


# def run_training(data_dir, checkpoint_dir, summary_dir, num_epochs=3, learning_rate=0.001, batch_size=5, num_hidden=1024, multiclass=False):
    
#     if multiclass:
#       num_classes = 54
#     else:
#       num_classes = 2

#     # construct the graph
#     with tf.Graph().as_default():

#         # specify the training data file location

#         # read the images and labels

#         ## NoConv
#         fibers, labels = nn.inputs(data_dir, 'train', batch_size=batch_size, num_epochs=num_epochs, conv=False)
#         results = nn.inference(fibers, num_hidden, num_classes, is_training=True)

#         # ### Conv
#         # fibers, labels = nn.inputs(data_dir, 'train', batch_size=batch_size, num_epochs=num_epochs, conv=True)
#         # results = nn.inference_conv(fibers, 2, 34, 50, num_hidden, num_classes, is_training=True)

#         labels = nn.reformat_train_label(labels, num_classes)

#         # calculate the loss from the results of inference and the labels
#         loss = nn.loss(results, labels)

#         # setup the training operations
#         train_op = nn.training(loss, learning_rate)

#         # setup the summary ops to use TensorBoard
#         summary_op = tf.summary.merge_all()

#         # init to setup the initial values of the weights
#         init_op = tf.group(tf.global_variables_initializer(),
#                            tf.local_variables_initializer())

#         # setup a saver for saving checkpoints
#         saver = tf.train.Saver()

#         # create the session
#         sess = tf.Session()

#         # specify where to write the log files for import to TensorBoard
#         summary_writer = tf.summary.FileWriter(summary_dir,
#                                                 graph=sess.graph)

#         # initialize the graph
#         sess.run(init_op)

#         # setup the coordinato and threadsr.  Used for multiple threads to read data.
#         # Not strictly required since we don't have a lot of data but typically
#         # using multiple threads to read data improves performance
#         coord = tf.train.Coordinator()
#         threads = tf.train.start_queue_runners(sess=sess, coord=coord)

#         # loop will continue until we run out of input training cases
#         try:
#             step = 0
#             while not coord.should_stop():

#                 # start time and run one training iteration
#                 start_time = time.time()
#                 _, loss_value = sess.run([train_op, loss])
#                 duration = time.time() - start_time

#                 if step % 100 == 0:
#                     print('Step %d: loss = %.12f (%.3f sec)' % (step, loss_value, duration))
#                     print ""
#                     sys.stdout.flush()

#                     # output some data to the log files for tensorboard
#                     summary_str = sess.run(summary_op)
#                     summary_writer.add_summary(summary_str, step)
#                     summary_writer.flush()

#                 # less frequently output checkpoint files.  Used for evaluating the model
#                 if step % 10000 == 0:
#                     checkpoint_path = os.path.join(checkpoint_dir,
#                                                    'model.ckpt')
#                     saver.save(sess, checkpoint_path, global_step=step)
#                 step += 1

#                 # quit after we run out of input files to read
#         except tf.errors.OutOfRangeError:
#             print('Done training for %d epochs, %d steps.' % (num_epochs,
#                                                               step))
#             sys.stdout.flush()
#             checkpoint_path = os.path.join(checkpoint_dir,
#                                            'model.ckpt')
#             saver.save(sess, checkpoint_path, global_step=step)

#         finally:
#             coord.request_stop()

#         # shut down the threads gracefully
#         coord.join(threads)
#         sess.close()


def run_training(data_dir, checkpoint_dir, summary_dir, num_epochs=3, learning_rate=0.001, batch_size=5, num_hidden=1024, multiclass=False):
    
    if multiclass:
      num_classes = 54
    else:
      num_classes = 2

    # construct the graph
    with tf.Graph().as_default():

        # specify the training data file location

        # read the images and labels

        ## NoConv
        fibers, labels = nn.inputs(data_dir, 'train', batch_size=batch_size, num_epochs=num_epochs, conv=False)
        results = nn.inference(fibers, num_hidden, num_classes, is_training=True)

        # ### Conv
        # fibers, labels = nn.inputs(data_dir, 'train', batch_size=batch_size, num_epochs=num_epochs, conv=True)
        # results = nn.inference_conv(fibers, 2, 34, 50, num_hidden, num_classes, is_training=True)

        labels = nn.reformat_train_label(labels, num_classes)

        # calculate the loss from the results of inference and the labels
        loss = nn.loss(results, labels)

        # setup the training operations
        train_op = nn.training(loss, learning_rate)

        # setup the summary ops to use TensorBoard
        summary_op = tf.summary.merge_all()

        # init to setup the initial values of the weights
        init_op = tf.group(tf.global_variables_initializer(),
                           tf.local_variables_initializer())

        # setup a saver for saving checkpoints
        saver = tf.train.Saver()

        # create the session
        sess = tf.Session()

        # specify where to write the log files for import to TensorBoard
        summary_writer = tf.summary.FileWriter(summary_dir,
                                                graph=sess.graph)

        # initialize the graph
        sess.run(init_op)

        # setup the coordinato and threadsr.  Used for multiple threads to read data.
        # Not strictly required since we don't have a lot of data but typically
        # using multiple threads to read data improves performance
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        # loop will continue until we run out of input training cases
        try:
            step = 0
            while not coord.should_stop():

                # start time and run one training iteration
                start_time = time.time()
                _, loss_value = sess.run([train_op, loss])
                duration = time.time() - start_time

                if step % 100 == 0:
                    print('Step %d: loss = %.12f (%.3f sec)' % (step, loss_value, duration))

                    print ""

                    sys.stdout.flush()

                    # output some data to the log files for tensorboard
                    summary_str = sess.run(summary_op)
                    summary_writer.add_summary(summary_str, step)
                    summary_writer.flush()

                # less frequently output checkpoint files.  Used for evaluating the model
                if step % 10000 == 0:
                    checkpoint_path = os.path.join(checkpoint_dir,
                                                   'model.ckpt')
                    saver.save(sess, checkpoint_path, global_step=step)
                step += 1

                # quit after we run out of input files to read
        except tf.errors.OutOfRangeError:
            print('Done training for %d epochs, %d steps.' % (num_epochs,
                                                              step))
            checkpoint_path = os.path.join(checkpoint_dir,
                                           'model.ckpt')
            saver.save(sess, checkpoint_path, global_step=step)

        finally:
            coord.request_stop()

        # shut down the threads gracefully
        coord.join(threads)
        sess.close()


def main(_):
    start = time.time()
    run_training(FLAGS.data_dir, FLAGS.checkpoint_dir, FLAGS.summary_dir, FLAGS.num_epochs, FLAGS.learning_rate, FLAGS.batch_size, FLAGS.num_hidden, FLAGS.multiclass)
    end = time.time()
    print "Training Process took %dh%02dm%02ds" % (convert_time(end - start))


if __name__ == '__main__':
    tf.app.run()
