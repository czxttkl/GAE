'''
Logistic regression baseline
'''
import sys
sys.path.insert(0, '..')

import numpy
from baseline import Baseline
from data_mangle.cv_fold_reader import CVFoldReader
from sklearn.linear_model import LogisticRegression
from utils import constants


class BaselineLR(Baseline):

    def to_feature_matrix(self, M_r_C, M_b_C, M):
        train_data = numpy.zeros((M_r_C.shape[0], M))
        for z, (MrC, MbC) in enumerate(zip(M_r_C, M_b_C)):
            train_data[z, MrC] = 1
            train_data[z, MbC] = -1
        return train_data

    def print_model(self, model):
        """ return description of a model as a string """
        data_src = self.reader.data_path.split('/')[-1].split('.')[0]
        return "{0}_lR_C{1}".format(data_src, model.C)

if __name__ == "__main__":
    baseline = \
        BaselineLR(
            models=[LogisticRegression(fit_intercept=False, n_jobs=-1, C=1.0, penalty='l2'),
                    # add more grid search models here ...
                    ],
            reader=CVFoldReader(data_path=constants.hon_output_pickle, folds=10))
    baseline.cross_valid()
