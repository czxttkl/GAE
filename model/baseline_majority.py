'''
majority class baseline
'''
import sys
sys.path.insert(0, '..')

from baseline import Baseline
from sklearn.dummy import DummyClassifier
from data_mangle.report_writer import ReportWriter
from utils.parser import parse_ml_parameters, parse_reader


class BaselineMajority(Baseline):

    def print_model(self, model):
        """ return description of a model as a string """
        return "MajorityClass"


if __name__ == "__main__":
    kwargs = parse_ml_parameters()

    dataset = 'dota' if not kwargs else kwargs.dataset
    density = 'dense' if not kwargs else kwargs.density
    fold = 3 if not kwargs else kwargs.fold
    seed = 718 if not kwargs else kwargs.seed

    # use nn_featconfig for the time being
    feature_config = 'one_way_one_team' if not kwargs else kwargs.nn_featconfig

    print('use parameter: dataset {}, feature_config: {}, density: {}, fold: {}, seed: {}'
          .format(dataset, feature_config, density, fold, seed))
    reader = parse_reader(dataset, feature_config, density, fold, seed)

    baseline = \
        BaselineMajority(
            models=[DummyClassifier(strategy='most_frequent')],
            # reader=CVFoldLoLSparseReader(data_path=constants.lol_pickle, folds=10,
            #                              feature_config='champion_summoner_one_team'),
            # reader=CVFoldSparseReader(data_path=constants.dota_pickle, folds=10,
            #                           feature_config='one_way_one_team'),
            reader=reader,
            writer=ReportWriter('result.csv'))
    baseline.cross_valid(validation=True)

    # baseline.save_model()
