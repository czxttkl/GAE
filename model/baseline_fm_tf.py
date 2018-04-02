""" Tensorflow based factorization machine baseline """
import sys
sys.path.insert(0, '..')

from data_mangle.report_writer import ReportWriter
from baseline import Baseline
from data_mangle.cv_fold_sparse_reader import CVFoldSparseReader
from data_mangle.cv_fold_lol_sparse_reader import CVFoldLoLSparseReader
from utils import constants
from tffm import TFFMClassifier
import tensorflow as tf
from utils.parser import parse_parameters


class BaselineTFFM(Baseline):

    def print_model(self, model):
        """ return description of a model as a string """
        return 'FM_order{}_rank{}_l2regw{}_epoch{}'\
            .format(model.core.order, model.core.rank, model.core.reg, model.n_epochs)


if __name__ == "__main__":
    kwargs = parse_parameters()

    feature_config = 'champion_summoner_two_teams' if not kwargs else kwargs.fm_featconfig

    fm_model = TFFMClassifier(
                        order=2 if not kwargs else kwargs.fm_order,
                        rank=200 if not kwargs else kwargs.fm_rank,
                        optimizer=tf.train.AdamOptimizer(),
                        n_epochs=5 if not kwargs else kwargs.fm_epoch,
                        batch_size=1024,
                        init_std=0.0000000001,
                        reg=0 if not kwargs else kwargs.fm_reg,
                        input_type='sparse')

    baseline = BaselineTFFM(models=[fm_model,
                                    # add more grid search models here ...
                                    ],
                            reader=CVFoldLoLSparseReader(data_path=constants.lol_pickle, folds=10,
                                                         feature_config=feature_config),
                            writer=ReportWriter('result.csv'))
    baseline.cross_valid(show_progress=True)

