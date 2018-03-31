'''
Xgboost baseline
'''
import sys
sys.path.insert(0, '..')

import numpy
from baseline import Baseline
from data_mangle.cv_fold_dense_reader import CVFoldDenseReader
from data_mangle.report_writer import ReportWriter
from utils import constants
import xgboost as xgb
from sklearn.metrics import accuracy_score


class MyXgboost():
    def __init__(self, nthread, nrounds, max_depth, l2_reg, eta):
        self.max_depth = max_depth
        self.l2_reg = l2_reg
        self.eta = eta
        self.num_round = nrounds
        param = {'max_depth': max_depth, 'lambda': l2_reg, 'eta': eta, 'silent': 0, 'objective': 'binary:logistic',
                 'nthread': nthread}
        param['eval_metric'] = ['error']
        self.param = param

    def fit(self, train_data, train_labels):
        dtrain = xgb.DMatrix(train_data, label=train_labels)
        self.bst = xgb.train(self.param, dtrain, self.num_round, verbose_eval=100)

    def score(self, test_data, test_labels):
        pred_probs = self.bst.predict(xgb.DMatrix(test_data))
        pred_probs = numpy.where(pred_probs < 0.5, 0.0, 1.0)
        acc = accuracy_score(test_labels, pred_probs)
        return acc

    def predict_proba(self, test_data):
        pred_probs = self.bst.predict(xgb.DMatrix(test_data))
        return pred_probs


class BaselineXgboost(Baseline):

    def print_model(self, model):
        """ return description of a model as a string """
        return "GBDT_max_depth{}_l2_reg{}_eta{}_rounds{}"\
            .format(model.max_depth, model.l2_reg, model.eta, model.num_round)


if __name__ == "__main__":
    baseline = BaselineXgboost(models=[MyXgboost(nthread=50, nrounds=12, max_depth=3, l2_reg=20, eta=0.1),
                                       MyXgboost(nthread=50, nrounds=12, max_depth=6, l2_reg=20, eta=0.1),
                                       # add more grid search models here ...
                                       ],
                               reader=CVFoldDenseReader(data_path=constants.dota2_pickle, folds=10),
                               writer=ReportWriter('result.csv'))
    baseline.cross_valid()
