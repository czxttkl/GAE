import copy
import numpy
import time
from sklearn.metrics import roc_auc_score


class Baseline(object):
    def __init__(self, models, reader):
        self.models = models
        self.reader = reader

    def cross_valid(self):
        """
        Cross validate a list of models self.models
        :return: the last fold's best model
        """
        test_accs = []
        test_aucs = []

        for i in xrange(self.reader.folds):
            train_data, train_labels, test_data, test_labels, valid_data, valid_labels = self.to_data_labels(i)

            valid_accs = []
            for raw_model in self.models:
                model = copy.deepcopy(raw_model)

                t1 = time.time()
                model.fit(train_data, train_labels)
                train_time = time.time() - t1

                train_acc, valid_acc = model.score(train_data, train_labels), model.score(valid_data, valid_labels)
                print "baseline fold {0}, {1}: train acc: {2}, valid acc: {3}, train time: {4}"\
                    .format(i, self.print_model(model), train_acc, valid_acc, train_time)
                valid_accs.append((model, valid_acc))

            best_model, best_valid_acc = max(valid_accs, key=lambda x: x[1])
            test_acc = best_model.score(test_data, test_labels)
            test_accs.append(test_acc)

            test_predict_probs = best_model.predict_proba(test_data)
            # some model outputs probabilities for both classes. we only need probs for positive class.
            if len(test_predict_probs.shape) > 1:
                test_predict_probs = test_predict_probs[:, 1]
            test_auc = roc_auc_score(test_labels, test_predict_probs)
            test_aucs.append(test_auc)

            print "baseline fold {0}, best model: {1}, best valid acc: {2}, test acc: {3}, test auc: {4}".\
                format(i, self.print_model(best_model), best_valid_acc, test_acc, test_auc)

        print "finish cross validation. Avg test acc: {0}, avg test auc: {1}".\
            format(numpy.mean(test_accs), numpy.mean(test_aucs))

        return best_model

    def to_data_labels(self, fold):
        """ Read a specific fold. Convert to model usable feature matrix and label vector. """
        M_o_train, M_r_C_train, M_b_C_train, M_o_test, M_r_C_test, M_b_C_test, \
            M_o_valid, M_r_C_valid, M_b_C_valid, M = self.reader.read_train_test_valid_fold(fold)

        train_data = self.to_feature_matrix(M_r_C_train, M_b_C_train, M)
        train_labels = self.to_label_vector(M_o_train)
        test_data = self.to_feature_matrix(M_r_C_test, M_b_C_test, M)
        test_labels = self.to_label_vector(M_o_test)
        valid_data = self.to_feature_matrix(M_r_C_valid, M_b_C_valid, M)
        valid_labels = self.to_label_vector(M_o_valid)

        return train_data, train_labels, test_data, test_labels, valid_data, valid_labels

    def to_feature_matrix(self, M_r_C, M_b_C, M):
        """ Convert raw data matrix into feature matrix which is to be used for model fitting.
        This method should be overwritten by child class.

        :return: a single feature matrix
        """
        pass

    def to_label_vector(self, M_o):
        """ Convert raw label vector to the label vector used for model fitting """
        return M_o

    def print_model(self, model):
        """ return description of a model as a string """
        return "null"

