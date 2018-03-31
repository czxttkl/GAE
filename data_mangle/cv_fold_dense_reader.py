""" Data reader for cross validation.
This reader only works for HotS, HoN and Dota datatsets.
This reader returns dense feature vectors
"""
from sklearn.model_selection import ShuffleSplit
import pickle
import numpy
import time


class CVFoldDenseReader(object):
    def __init__(self, data_path, folds, seed=None):
        """
        Read data files and then split data into K folds.
        """
        self.read_data_from_file(data_path, folds, seed)

    def read_data_from_file(self, data_path, folds, seed):
        """
        Data format:

        M_o (n_matches): 1D vector of outcomes, in which 0 denotes the blue team wins and 1 denotes the red team wins

        M_r_C (n_matches, 5): avatar ids in the red team for each match

        M_b_C (n_matches, 5): avatar ids in the blue team for each match

        M: the number of avatars in the dataset.
        """
        with open(data_path, 'rb') as f:
            self.M_o, self.M_r_C, self.M_b_C, self.match_id2idx_dict, self.champion_id2idx_dict, self.Z, self.M = \
                pickle.load(f)

        print("CVFoldReader. Z: {0}, M: {1}".format(self.Z, self.M))

        self.data_path = data_path
        self.folds = folds

        # use 90% as train data and 10% test data
        ss = ShuffleSplit(n_splits=folds, test_size=0.1, train_size=0.9, random_state=seed)
        self.train_split_idx = {}
        self.test_split_idx = {}

        i = 0
        for train_idx, test_idx in ss.split(numpy.arange(self.Z)):
            self.train_split_idx[i], self.test_split_idx[i] = train_idx, test_idx
            i += 1

        self.data_src = data_path.split('/')[-1].split('.')[0]

    def read_train_test_fold(self, i):
        """
        Read i-th fold of splitted train/test data
        """
        train_idx, test_idx = self.train_split_idx[i], self.test_split_idx[i]

        M_o_train = self.M_o[train_idx]
        M_r_C_train = self.M_r_C[train_idx]
        M_b_C_train = self.M_b_C[train_idx]
        M_o_test = self.M_o[test_idx]
        M_r_C_test = self.M_r_C[test_idx]
        M_b_C_test = self.M_b_C[test_idx]

        train_feature = self.to_feature_matrix(M_r_C_train, M_b_C_train)
        test_feature = self.to_feature_matrix(M_r_C_test, M_b_C_test)

        return train_feature, M_o_train, test_feature, M_o_test

    def to_feature_matrix(self, M_r_C, M_b_C):
        data = numpy.zeros((M_r_C.shape[0], 2 * self.M))
        t1 = time.time()
        for z, (MrC, MbC) in enumerate(zip(M_r_C, M_b_C)):
            data[z, MrC] = 1
            data[z, self.M + MbC] = 1
        print("finish feature matrix conversion. time:", time.time() - t1)
        return data

    def print_feature_config(self):
        return "one_way_two_teams_dense"