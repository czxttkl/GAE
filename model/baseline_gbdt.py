'''
GBDT implemented in scikit learn.
'''
import sys
sys.path.insert(0, '..')

from baseline import Baseline
from sklearn.ensemble import GradientBoostingClassifier
from data_mangle.report_writer import ReportWriter
from utils.parser import parse_ml_parameters, parse_reader


class BaselineGBDT(Baseline):

    def print_model(self, model):
        """ return description of a model as a string """
        return "gbdt_ntree{}_lr{}_md{}_msl{}"\
            .format(model.n_estimators, model.learning_rate, model.max_depth, model.min_samples_leaf)


if __name__ == "__main__":
    kwargs = parse_ml_parameters()

    dataset = 'dota' if not kwargs else kwargs.dataset
    density = 'dense' if not kwargs else kwargs.density
    fold = 3 if not kwargs else kwargs.fold
    seed = 718 if not kwargs else kwargs.seed

    feature_config = 'one_way_one_team' if not kwargs else kwargs.gbdt_featconfig
    gbdt_ntree = 100 if not kwargs else kwargs.gbdt_ntree
    gbdt_lr = 0.1 if not kwargs else kwargs.gbdt_lr
    gbdt_md = 3 if not kwargs else kwargs.gbdt_maxdepth
    gbdt_msl = 1 if not kwargs else kwargs.gbdt_minsampleleaf

    print('use parameter: dataset {}, feature_config: {}, density: {}, fold: {}, seed: {}, n_tree: {}, lr: {}, max_depth: {}, min_sample_leaf: {}'
          .format(dataset, feature_config, density, fold, seed, gbdt_ntree, gbdt_lr, gbdt_md, gbdt_msl))
    reader = parse_reader(dataset, feature_config, density, fold, seed)

    baseline = \
        BaselineGBDT(
            models=[GradientBoostingClassifier(n_estimators=gbdt_ntree,
                                               learning_rate=gbdt_lr,
                                               max_depth=gbdt_md,
                                               min_samples_leaf=gbdt_msl,
                                               verbose=True),
                    # add more grid search models here ...
                    ],
            # reader=CVFoldLoLSparseReader(data_path=constants.lol_pickle, folds=10,
            #                              feature_config='champion_summoner_one_team'),
            # reader=CVFoldSparseReader(data_path=constants.dota_pickle, folds=10,
            #                           feature_config='one_way_one_team'),
            reader=reader,
            writer=ReportWriter('result.csv'))
    baseline.cross_valid(validation=True)

    # baseline.save_model()
