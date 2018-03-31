import copy
import numpy
import time
from sklearn.metrics import roc_auc_score


class Baseline(object):
    def __init__(self, models, reader, writer):
        self.models = models
        self.reader = reader
        self.writer = writer

    def cross_valid(self, show_progress=False):
        """
        Cross validate a list of models self.models
        :return: the last fold's best model
        """
        for raw_model in self.models:
            train_accs = []
            test_accs = []
            train_aucs = []
            test_aucs = []
            durations = []

            for i in range(self.reader.folds):
                train_data, train_labels, test_data, test_labels = self.to_data_labels(i)
                model = copy.deepcopy(raw_model)

                t1 = time.time()
                if show_progress:
                    model.fit(train_data, train_labels, show_progress=True)
                else:
                    model.fit(train_data, train_labels)
                train_time = int(time.time() - t1)
                durations.append(train_time)

                train_acc = model.score(train_data, train_labels)
                test_acc = model.score(test_data, test_labels)
                train_accs.append(train_acc)
                test_accs.append(test_acc)

                train_predict_probs = model.predict_proba(train_data)
                test_predict_probs = model.predict_proba(test_data)
                # some model outputs probabilities for both classes. we only need probs for positive class.
                if len(train_predict_probs.shape) > 1:
                    train_predict_probs = train_predict_probs[:, 1]
                if len(test_predict_probs.shape) > 1:
                    test_predict_probs = test_predict_probs[:, 1]
                train_auc = roc_auc_score(train_labels, train_predict_probs)
                test_auc = roc_auc_score(test_labels, test_predict_probs)
                train_aucs.append(train_auc)
                test_aucs.append(test_auc)

                print("{}, {}, {}, fold {}: train acc/auc: {:.5f}/{:.5f}, test acc/auc: {:.5f}/{:.5f}, train time: {}"
                      .format(self.reader.data_src, self.print_model(model), self.reader.print_feature_config(),
                              i, train_acc, train_auc, test_acc, test_auc, train_time))

            self.writer.write_result(self.reader.data_src, self.print_model(model), self.reader.print_feature_config(),
                                     numpy.mean(durations), numpy.mean(train_accs), numpy.mean(train_aucs),
                                     numpy.mean(test_accs), numpy.mean(test_aucs))

    def to_data_labels(self, fold):
        """ Read a specific fold. Convert to model usable feature matrix and label vector. """
        train_data, train_labels, test_data, test_labels = self.reader.read_train_test_fold(fold)
        return train_data, train_labels, test_data, test_labels

    def print_model(self, model):
        """ return description of a model as a string """
        return "null"

