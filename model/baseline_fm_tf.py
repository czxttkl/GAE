""" Tensorflow based 2-way factorization machine baseline """
import sys
sys.path.insert(0, '..')

import time
import numpy
from baseline import Baseline
from data_mangle.cv_fold_reader import CVFoldReader
from utils import constants
from scipy.sparse import csr_matrix
from tffm import TFFMClassifier
import tensorflow as tf
import pickle


class BaselineTFFM(Baseline):

    def to_feature_matrix(self, M_r_C, M_b_C, M):
        train_data = numpy.zeros((M_r_C.shape[0], 2 * M))
        t1 = time.time()
        for z, (MrC, MbC) in enumerate(zip(M_r_C, M_b_C)):
            train_data[z, MrC] = 1
            train_data[z, M + MbC] = 1
        train_data = csr_matrix(train_data)
        print "finish sparse feature matrix construction", time.time() - t1
        return train_data

    def print_model(self, model):
        """ return description of a model as a string """
        data_src = self.reader.data_path.split('/')[-1].split('.')[0]
        return '{0}_FM_rank{1}_l2regw{2}'.format(data_src, model.core.rank, model.core.reg)

if __name__ == "__main__":
    fm200_reg0 = TFFMClassifier(
                        order=2,
                        rank=200,
                        optimizer=tf.train.AdamOptimizer(),
                        n_epochs=100,
                        batch_size=1000,
                        init_std=0.001,
                        reg=0,
                        input_type='sparse')

    baseline = BaselineTFFM(models=[fm200_reg0,
                                    # add more grid search models here ...
                                    ],
                                    reader=CVFoldReader(data_path=constants.dota2_pickle, folds=10))
    best_model = baseline.cross_valid()

    # save best model
    # with open('../output/{0}.pickle'.format(baseline.print_model(best_model)), 'w') as f:
    #     pickle.dump(w, f)
