'''
2-way Factorization machine baseline based on libfm

See baseline_fm_tf.py for an equivalent implementation using Tensorflow,
which has a drastically improved trainiong speed.
'''
import sys
sys.path.insert(0, '..')

import time
import numpy
from baseline import Baseline
from data_mangle.cv_fold_reader import CVFoldReader
from utils import constants
from fastFM.als import FMClassification
from scipy.sparse import csr_matrix


class BaselineFM(Baseline):
    def to_label_vector(self, M_o):
        """
        libFM only accepts labels being -1 and 1.
        """
        return  numpy.where(M_o == 0.0, -1.0, 1.0)

    def to_feature_matrix(self, M_r_C, M_b_C, M):
        train_data = numpy.zeros((M_r_C.shape[0], 2*M))
        t1 = time.time()
        for z, (MrC, MbC) in enumerate(zip(M_r_C, M_b_C)):
            train_data[z, MrC] = 1
            train_data[z, M+MbC] = 1
        train_data = csr_matrix(train_data)
        print "finish sparse feature matrix construction", time.time()-t1
        return train_data

    def print_model(self, model):
        """ return description of a model as a string """
        data_src = self.reader.data_path.split('/')[-1].split('.')[0]
        return '{0}_FM_rank{1}_l2regw{2}_l2regV{3}'.format(data_src, model.rank, model.l2_reg_w, model.l2_reg_V)

if __name__ == "__main__":
    baseline = BaselineFM(models=[FMClassification(rank=200, l2_reg_w=0.1, l2_reg_V=0.1),
                                  # add more grid search models here ...
                                  ],
                          reader=CVFoldReader(data_path=constants.dota2_pickle, folds=10))
    baseline.cross_valid()

    # save best model
    # with open('../output/{0}.pickle'.format(baseline.print_model(best_model)), 'w') as f:
    #     pickle.dump(w, f)