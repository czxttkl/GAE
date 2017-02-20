""" The parent class for Tensorflow-based model. """
import pickle
import numpy


class TFModel(object):

    def __init__(self, reader):
        self.reader = reader

    def train_once(self, **kwargs):
        """ Train a model just using one fold   """
        M_o_train, M_r_C_train, M_b_C_train, M_o_test, M_r_C_test, M_b_C_test, \
        M_o_valid, M_r_C_valid, M_b_C_valid, M = self.reader.read_train_test_valid_fold(0)
        kwargs['fold'] = 0
        self._train(M_o_train, M_r_C_train, M_b_C_train, M_o_test, M_r_C_test, M_b_C_test,
                    M_o_valid, M_r_C_valid, M_b_C_valid, M, **kwargs)

    def train_cv(self, **kwargs):
        """ Train multiple models, each using a fold of data"""
        test_accs, test_aucs = [], []
        for i in xrange(self.reader.folds):
            M_o_train, M_r_C_train, M_b_C_train, M_o_test, M_r_C_test, M_b_C_test, \
            M_o_valid, M_r_C_valid, M_b_C_valid, M = self.reader.read_train_test_valid_fold(i)
            kwargs['fold'] = i
            test_acc, test_auc = self._train(M_o_train, M_r_C_train, M_b_C_train, M_o_test, M_r_C_test, M_b_C_test,
                                             M_o_valid, M_r_C_valid, M_b_C_valid, M, **kwargs)
            test_accs.append(test_acc)
            test_aucs.append(test_auc)

        print "finish cross validation. Average test acc: {0}. Average test auc: {1}".\
            format(numpy.mean(test_accs), numpy.mean(test_aucs))

    def _train(self, M_o_train, M_r_C_train, M_b_C_train, M_o_test, M_r_C_test, M_b_C_test,
               M_o_valid, M_r_C_valid, M_b_C_valid, M, **kwargs):
        """ This method is the specific implementation of training process.
        This method should be implemented by child class.
        :return: (test accuracy, test auc). Test acc/auc are obtained when the model trained on train dataset achieves
         the highest accuracy on a validation dataset.
        """
        pass

    def save_model(self, **kwargs):
        with open('../output/' + self.model_file_name(**kwargs), 'w') as f:
            pickle.dump(self.collect_model_variables(), f)

    def model_file_name(self, **kwargs):
        """ This method returns the file name used for storing model. It should be implemented by specific model. """
        pass

    def collect_model_variables(self):
        """ This method returns the variables to be stored. """
        pass