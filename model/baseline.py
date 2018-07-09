import copy
import numpy
import time
from sklearn.metrics import roc_auc_score, accuracy_score
import pickle


class Baseline(object):
    def __init__(self, models, reader, writer):
        self.models = models
        self.reader = reader
        self.writer = writer

    def cross_valid(self, validation=True):
        """
        Cross validate a list of models self.models
        :return: the last fold's best model
        """
        for raw_model in self.models:
            train_accs = []
            test_accs = []
            valid_accs = []
            train_aucs = []
            test_aucs = []
            valid_aucs = []
            durations = []

            for i in range(self.reader.folds):
                if not validation:
                    train_data, train_labels, test_data, test_labels = self.reader.read_train_test_fold(i)
                else:
                    train_data, train_labels, test_data, test_labels, valid_data, valid_labels = \
                        self.reader.read_train_test_valid_fold(i)

                model = copy.deepcopy(raw_model)

                t1 = time.time()
                model.fit(train_data, train_labels)
                train_time = int(time.time() - t1)
                durations.append(train_time)

                train_predict_probs = model.predict_proba(train_data)
                test_predict_probs = model.predict_proba(test_data)
                if validation:
                    valid_predict_probs = model.predict_proba(valid_data)

                # some model outputs probabilities for both classes. we only need probs for positive class.
                if len(train_predict_probs.shape) > 1:
                    train_predict_probs = train_predict_probs[:, 1]
                if len(test_predict_probs.shape) > 1:
                    test_predict_probs = test_predict_probs[:, 1]
                if validation and len(valid_predict_probs.shape) > 1:
                    valid_predict_probs = valid_predict_probs[:, 1]

                train_auc = self.get_auc(train_labels, train_predict_probs)
                train_aucs.append(train_auc)
                test_auc = self.get_auc(test_labels, test_predict_probs)
                test_aucs.append(test_auc)
                if validation:
                    valid_auc = self.get_auc(valid_labels, valid_predict_probs)
                    valid_aucs.append(valid_auc)

                train_acc = self.get_acc(train_labels, train_predict_probs)
                train_accs.append(train_acc)
                test_acc = self.get_acc(test_labels, test_predict_probs)
                test_accs.append(test_acc)
                if validation:
                    valid_acc = self.get_acc(valid_labels, valid_predict_probs)
                    valid_accs.append(valid_acc)

                if not validation:
                    print("{}, {}, {}, fold {}: train acc/auc: {:.5f}/{:.5f}, test acc/auc: {:.5f}/{:.5f}, train time: {}"
                          .format(self.reader.data_src, self.print_model(model), self.reader.print_feature_config(),
                                  i, train_acc, train_auc, test_acc, test_auc, train_time))
                else:
                    print(
                        "{}, {}, {}, fold {}: train acc/auc: {:.5f}/{:.5f}, test acc/auc: {:.5f}/{:.5f}, valid acc/auc: {:.5f}/{:.5f}, train time: {}"
                        .format(self.reader.data_src, self.print_model(model), self.reader.print_feature_config(),
                                i, train_acc, train_auc, test_acc, test_auc, valid_acc, valid_auc, train_time))

            if not validation:
                self.writer.write_result_train_test(
                    self.reader.data_src, self.print_model(model), self.reader.print_feature_config(),
                    numpy.mean(durations), numpy.mean(train_accs), numpy.mean(train_aucs),
                    numpy.mean(test_accs), numpy.mean(test_aucs))
            else:
                self.writer.write_result_train_test_valid(
                    self.reader.data_src, self.print_model(model), self.reader.print_feature_config(),
                    numpy.mean(durations),
                    numpy.mean(train_accs), numpy.mean(train_aucs),
                    numpy.mean(test_accs), numpy.mean(test_aucs),
                    numpy.mean(valid_accs), numpy.mean(valid_aucs),
                )

            self.reader.save_match_id_record()
            self.last_model = model

    def get_auc(self, labels, predict_probs):
        auc = roc_auc_score(labels, predict_probs)
        return auc

    def get_acc(self, labels, predict_probs):
        predict_labels = (predict_probs > 0.5).astype(labels.dtype)
        acc = accuracy_score(labels, predict_labels)
        return acc

    def print_model(self, model):
        """ return description of a model as a string """
        return "null"

    def save_model(self):
        assert self.last_model is not None
        with open('../output/{}_{}.pickle'.format(self.print_model(self.last_model), self.reader.data_src), 'wb') as f:
            pickle.dump((self.last_model, self.reader.M), f)

