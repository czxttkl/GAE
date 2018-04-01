""" Tensorflow based factorization machine baseline """
import sys
sys.path.insert(0, '..')

from data_mangle.report_writer import ReportWriter
from baseline import Baseline
from data_mangle.cv_fold_sparse_reader import CVFoldSparseReader
from utils import constants
from tffm import TFFMClassifier
import tensorflow as tf


class BaselineTFFM(Baseline):

    def print_model(self, model):
        """ return description of a model as a string """
        return 'FM_order{}_rank{}_l2regw{}_epoch{}'\
            .format(model.core.order, model.core.rank, model.core.reg, model.n_epochs)


if __name__ == "__main__":
    fm200_reg0 = TFFMClassifier(
                        order=2,
                        rank=200,
                        optimizer=tf.train.AdamOptimizer(),
                        n_epochs=50,
                        batch_size=1024,
                        init_std=0.001,
                        reg=0,
                        input_type='sparse')

    baseline = BaselineTFFM(models=[fm200_reg0,
                                    # add more grid search models here ...
                                    ],
                            reader=CVFoldSparseReader(data_path=constants.dota2_pickle, folds=10,
                                                      feature_config='one_way_two_teams'),
                            writer=ReportWriter('result.csv'))
    baseline.cross_valid(show_progress=True)

