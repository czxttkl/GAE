""" Data reader for cross validation. """
from sklearn.model_selection import ShuffleSplit
import pickle
import numpy


class CVFoldReader(object):
    def __init__(self, data_path, folds, seed=None):
        """
        Read data files and then split data into K folds.
        """
        with open(data_path, 'r') as f:
            self.M_o, self.M_r_C, self.M_b_C, self.match_id2idx_dict, self.champion_id2idx_dict, self.Z, self.M = \
                pickle.load(f)

        print "CVFoldReader. Z: {0}, M: {1}".format(self.Z, self.M)

        self.data_path = data_path
        self.folds = folds

        # use 80% as train data, 10% test data and 10% as validation data
        ss = ShuffleSplit(n_splits=folds, test_size=0.2, train_size=0.8, random_state=seed)
        self.train_split_idx = {}
        self.test_split_idx = {}
        self.valid_split_idx = {}

        i = 0
        for train_idx, test_idx in ss.split(numpy.arange(self.Z)):
            self.train_split_idx[i], self.test_split_idx[i], self.valid_split_idx[i] = \
                train_idx, test_idx[:len(test_idx)/2], test_idx[len(test_idx)/2:]
            i += 1

    def read_train_test_valid_fold(self, i):
        """
        Read i-th fold of splitted train/test/validation data


        Data format:

        M_o (n_matches): 1D vector of outcomes, in which 0 denotes the blue team wins and 1 denotes the red team wins

        M_r_C (n_matches, 5): avatar ids in the red team for each match

        M_b_C (n_matches, 5): avatar ids in the blue team for each match

        M: the number of avatars in the dataset.
        """
        train_idx, test_idx, valid_idx = self.train_split_idx[i], self.test_split_idx[i], self.valid_split_idx[i]

        M_o_train = self.M_o[train_idx]
        M_r_C_train = self.M_r_C[train_idx]
        M_b_C_train = self.M_b_C[train_idx]
        M_o_test = self.M_o[test_idx]
        M_r_C_test = self.M_r_C[test_idx]
        M_b_C_test = self.M_b_C[test_idx]
        M_o_valid = self.M_o[valid_idx]
        M_r_C_valid = self.M_r_C[valid_idx]
        M_b_C_valid = self.M_b_C[valid_idx]

        return M_o_train, M_r_C_train, M_b_C_train, M_o_test, M_r_C_test, M_b_C_test, \
            M_o_valid, M_r_C_valid, M_b_C_valid, self.M
