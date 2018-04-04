'''
Logistic regression baseline
'''
import sys
sys.path.insert(0, '..')

import numpy
from baseline import Baseline
from data_mangle.cv_fold_sparse_reader import CVFoldSparseReader
from data_mangle.cv_fold_lol_sparse_reader import CVFoldLoLSparseReader
from sklearn.linear_model import LogisticRegression
from utils import constants
from data_mangle.report_writer import ReportWriter


class BaselineLR(Baseline):

    def print_model(self, model):
        """ return description of a model as a string """
        return "lR_C{}".format(model.C)


if __name__ == "__main__":
    baseline = \
        BaselineLR(
            models=[LogisticRegression(fit_intercept=False, n_jobs=-1, C=0.00001, penalty='l2'),
                    LogisticRegression(fit_intercept=False, n_jobs=-1, C=0.0001, penalty='l2'),
                    LogisticRegression(fit_intercept=False, n_jobs=-1, C=0.001, penalty='l2'),
                    LogisticRegression(fit_intercept=False, n_jobs=-1, C=0.01, penalty='l2'),
                    LogisticRegression(fit_intercept=False, n_jobs=-1, C=0.1, penalty='l2'),
                    LogisticRegression(fit_intercept=False, n_jobs=-1, C=1.0, penalty='l2'),
                    LogisticRegression(fit_intercept=False, n_jobs=-1, C=10., penalty='l2'),
                    LogisticRegression(fit_intercept=False, n_jobs=-1, C=100., penalty='l2'),
                    LogisticRegression(fit_intercept=False, n_jobs=-1, C=1000., penalty='l2'),
                    LogisticRegression(fit_intercept=False, n_jobs=-1, C=10000., penalty='l2'),
                    # add more grid search models here ...
                    ],
            reader=CVFoldLoLSparseReader(data_path=constants.lol_pickle, folds=10,
                                         feature_config='champion_summoner_one_team'),
            writer=ReportWriter('result.csv'))
    baseline.cross_valid()
