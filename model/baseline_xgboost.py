'''
Xgboost baseline
'''
import sys
sys.path.insert(0, '..')

import numpy
from baseline import Baseline
from data_mangle.cv_fold_reader import CVFoldReader
from utils import constants
import xgboost as xgb
from sklearn.metrics import accuracy_score
import time


class MyXgboost():
    def __init__(self, nthread, nrounds, max_depth, l2_reg, eta):
        self.max_depth = max_depth
        self.l2_reg = l2_reg
        self.eta = eta
        self.num_round = nrounds

        param = {'max_depth': max_depth, 'lambda':l2_reg, 'eta': eta, 'silent': 0, 'objective': 'binary:logistic',
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

    def to_feature_matrix(self, M_r_C, M_b_C, M):
        train_data = numpy.zeros((M_r_C.shape[0], 2*M))
        t1 = time.time()
        for z, (MrC, MbC) in enumerate(zip(M_r_C, M_b_C)):
            train_data[z, MrC] = 1
            train_data[z, M+MbC] = 1
        print "finish feature matrix conversion. time:", time.time() - t1
        return train_data

    def print_model(self, model):
        """ return description of a model as a string """
        data_src = self.reader.data_path.split('/')[-1].split('.')[0]
        return "{0}_GBDT_max_depth{1}_l2_reg{2}_eta{3}_rounds{4}".\
            format(data_src, model.max_depth, model.l2_reg, model.eta, model.num_round)


if __name__ == "__main__":
    baseline = BaselineXgboost(models=[MyXgboost(nthread=8, nrounds=200, max_depth=6, l2_reg=20, eta=0.1),
                                       # add more grid search models here ...
                                       ],
                                       reader=CVFoldReader(data_path=constants.dota2_pickle, folds=10))
    baseline.cross_valid()
