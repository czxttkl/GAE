"""
GAE implemented in Tensorflow
"""
import sys
sys.path.insert(0, '..')

from utils import constants
from data_mangle.cv_fold_reader import CVFoldDenseReader
from data_mangle.mini_batcher import MiniBatcher
from tf_model import TFModel
import tensorflow as tf
import numpy
import time
from sklearn.metrics import roc_auc_score


class GAEModel(TFModel):

    def _train(self, M_o_train, M_r_C_train, M_b_C_train, M_o_test, M_r_C_test, M_b_C_test,
               M_o_valid, M_r_C_valid, M_b_C_valid, M, **kwargs):
        embedding_size = kwargs.get('embedding_size')
        seed = kwargs.get('seed')
        batch_size = kwargs.get('batch_size')
        early_stop_round = kwargs.get('early_stop_round')

        # Create the parameters of the model
        embeddings = tf.Variable(tf.random_uniform([M, embedding_size], -1.0, 1.0, seed=seed))
        w_counter = tf.Variable(tf.random_uniform([embedding_size, embedding_size], -1.0, 1.0, seed=seed))
        w_synergy = tf.Variable(tf.random_uniform([embedding_size, embedding_size], -1.0, 1.0, seed=seed))
        w_bias = tf.Variable(tf.random_uniform([M, 1], -1.0, 1.0, seed=seed))
        thres = tf.constant(0.5)

        # Define input output
        x_r = tf.placeholder(tf.int32, [None, 5])
        x_b = tf.placeholder(tf.int32, [None, 5])
        y = tf.placeholder(tf.int32)

        # feed forward
        embed_r = tf.nn.embedding_lookup(embeddings, x_r)
        embed_b = tf.nn.embedding_lookup(embeddings, x_b)
        embed_r_ave = tf.reduce_mean(embed_r, reduction_indices=1)    # shape: n_sample x embedding_size
        embed_b_ave = tf.reduce_mean(embed_b, reduction_indices=1)
        synergy_r = tf.reduce_mean(tf.multiply(tf.matmul(embed_r_ave, w_synergy), embed_r_ave), reduction_indices=1)
        synergy_b = tf.reduce_mean(tf.multiply(tf.matmul(embed_b_ave, w_synergy), embed_b_ave), reduction_indices=1)
        counter_r = tf.reduce_mean(tf.multiply(tf.matmul(embed_r_ave, w_counter), embed_b_ave), reduction_indices=1)
        counter_b = tf.reduce_mean(tf.multiply(tf.matmul(embed_b_ave, w_counter), embed_r_ave), reduction_indices=1)
        bias_r = tf.squeeze(tf.reduce_sum(tf.nn.embedding_lookup(w_bias, x_r), reduction_indices=1))
        bias_b = tf.squeeze(tf.reduce_sum(tf.nn.embedding_lookup(w_bias, x_b), reduction_indices=1))

        # _ trailing variables mean predicted values
        pre_y_ = tf.squeeze(synergy_r - synergy_b + counter_r - counter_b + bias_r - bias_b)
        prob_y_ = tf.nn.sigmoid(pre_y_)
        y_ = tf.cast(tf.greater(prob_y_, thres), tf.int32)

        # Define loss and optimizer
        cross_entropy = tf.reduce_mean(
            tf.nn.sigmoid_cross_entropy_with_logits(pre_y_, tf.cast(y, tf.float32)))
        loss = cross_entropy
        # Adagrad only supports to run on CPU
        # train_step = tf.train.AdagradOptimizer(0.5).minimize(loss)
        # AdamOptimizer supports to run on both CPU and GPU
        train_step = tf.train.AdamOptimizer().minimize(loss)

        # Test metrics
        accuracy = tf.contrib.metrics.accuracy(y_, y)

        # Train
        sess = tf.InteractiveSession()
        sess.run(tf.global_variables_initializer())
        sess.run(tf.local_variables_initializer())
        mini_batcher = MiniBatcher(batch_size=batch_size, seed=seed)

        best_valid_acc = 0
        best_valid_acc_round = 0
        test_acc = 0
        test_auc = 0

        for i in range(10000000):
            M_o_train_batch, M_r_C_train_batch, M_b_C_train_batch = \
                mini_batcher.next_batch(M_o_train, M_r_C_train, M_b_C_train)
            _, train_ce, train_acc, ws, wc, wb, e = \
                sess.run([train_step, cross_entropy, accuracy, w_synergy, w_counter, w_bias, embeddings],
                         feed_dict={x_r: M_r_C_train_batch, x_b: M_b_C_train_batch, y: M_o_train_batch})

            if i % 20 == 0:
                valid_acc = sess.run(accuracy, feed_dict={x_r: M_r_C_valid, x_b: M_b_C_valid, y: M_o_valid})

                if valid_acc > best_valid_acc:
                    best_valid_acc_round = i
                    best_valid_acc = valid_acc

                    test_acc, pred_test_probs = sess.run([accuracy, prob_y_], feed_dict={x_r: M_r_C_test, x_b: M_b_C_test, y: M_o_test})
                    test_auc = roc_auc_score(y_true=M_o_test, y_score=pred_test_probs)

                    self.ws, self.wc, self.wb,self.e, self.train_ce, self.train_acc, \
                        self.best_valid_acc, self.best_valid_acc_round, self.test_acc, self.test_auc \
                        = ws, wc, wb, e, train_ce, train_acc, best_valid_acc, best_valid_acc_round, test_acc, test_auc
                    self.save_model(**kwargs)

                print "batch", i, "test acc:", test_acc, "test auc:", test_auc, \
                    "train cross entropy:", train_ce, "train accuracy:", train_acc, \
                    "best valid acc", best_valid_acc, "at round", best_valid_acc_round, "at time", time.time()

            if i - best_valid_acc_round >= early_stop_round:
                break

        return test_acc, test_auc

    def model_file_name(self, **kwargs):
        """ Returns the file name used for storing model. """
        data_src = self.reader.data_path.split('/')[-1].split('.')[0]
        embedding_size = str(kwargs.get('embedding_size'))
        fold = str(kwargs.get('fold'))
        return "{0}_GAE_fold={1}_embed={2}.pickle".format(data_src, fold, embedding_size)

    def collect_model_variables(self):
        """ Returns the variables to be stored. """
        return self.ws, self.wc, self.wb, self.e, self.train_ce, self.train_acc, self.best_valid_acc, \
               self.best_valid_acc_round, self.test_acc, self.test_auc

if __name__ == "__main__":
    model = GAEModel(reader=CVFoldDenseReader(data_path=constants.dota2_pickle, folds=10, seed=715))
    model.train_cv(embedding_size=75, batch_size=1000, early_stop_round=30000)
