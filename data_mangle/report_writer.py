import os


class ReportWriter:

    def __init__(self, path):
        self.path = path

    def write_result_train_test(self, data_src, model, feature, duration, train_acc, train_auc, test_acc, test_auc):
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                line = "data_src, model, feature, duration, train_acc, train_auc, test_acc, test_auc\n"
                f.write(line)

        with open(self.path, 'a') as f:
            line = "{:>10s}, {:>20s}, {:>10s}, {:.2f}, {:.5f}, {:.5f}, {:.5f}, {:.5f}\n"\
                .format(data_src, model, feature, duration, train_acc, train_auc, test_acc, test_auc)
            f.write(line)
        print(
            "FINISH CV. {}, {}, {}, train acc/auc: {:.5f}/{:.5f}, test acc/auc: {:.5f}/{:.5f}, train time: {}\n"
                .format(data_src, model, feature, train_acc, train_auc, test_acc, test_auc, duration))

    def write_result_train_test_valid(
            self, data_src, model, feature, duration, train_acc, train_auc, test_acc, test_auc, valid_acc, valid_auc):
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                line = "data_src, model, feature, duration, train_acc, train_auc, test_acc, test_auc, valid_acc, valid_auc\n"
                f.write(line)

        with open(self.path, 'a') as f:
            line = "{:>10s}, {:>20s}, {:>10s}, {:.2f}, {:.5f}, {:.5f}, {:.5f}, {:.5f}, {:.5f}, {:.5f}\n"\
                .format(data_src, model, feature, duration, train_acc, train_auc, test_acc, test_auc, valid_acc, valid_auc)
            f.write(line)
        print(
            "FINISH CV. {}, {}, {}, train acc/auc: {:.5f}/{:.5f}, test acc/auc: {:.5f}/{:.5f}, valid acc/auc: {:.5f}/{:.5f}, train time: {}\n"
                .format(data_src, model, feature, train_acc, train_auc, test_acc, test_auc, valid_acc, valid_auc, duration))

