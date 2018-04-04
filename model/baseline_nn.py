'''
neural network baseline
'''
import sys
sys.path.insert(0, '..')

from baseline import Baseline
from data_mangle.cv_fold_sparse_reader import CVFoldSparseReader
from data_mangle.cv_fold_lol_sparse_reader import CVFoldLoLSparseReader
from data_mangle.cv_fold_dense_reader import CVFoldDenseReader
from sklearn.neural_network import MLPClassifier
from utils import constants
from data_mangle.report_writer import ReportWriter


class BaselineNN(Baseline):

    def print_model(self, model):
        """ return description of a model as a string """
        return "NN_hiddenunit{}".format(model.hidden_layer_sizes[0])


if __name__ == "__main__":
    baseline = \
        BaselineNN(
            models=[MLPClassifier(hidden_layer_sizes=(1000,),),
                    # add more grid search models here ...
                    ],
            # reader=CVFoldLoLSparseReader(data_path=constants.lol_pickle, folds=10,
            #                              feature_config='champion_summoner_one_team'),
            # reader=CVFoldSparseReader(data_path=constants.dota_pickle, folds=10,
            #                           feature_config='one_way_one_team'),
            reader=CVFoldDenseReader(data_path=constants.dota_pickle, folds=10,
                                     feature_config='one_way_one_team'),
            writer=ReportWriter('result.csv'))
    baseline.cross_valid()
