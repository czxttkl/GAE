import os


class ReportWriter:

    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            with open(path, 'w') as f:
                line = "data_src, model, feature, duration, train_acc, train_auc, test_acc, test_auc\n"
                f.write(line)

    def write_result(self, data_src, model, feature, duration, train_acc, train_auc, test_acc, test_auc):
        with open(self.path, 'a') as f:
            line = "{:>10s}, {:>20s}, {:>10s}, {:.2f}, {:.5f}, {:.5f}, {:.5f}, {:.5f}\n"\
                .format(data_src, model, feature, duration, train_acc, train_auc, test_acc, test_auc)
            f.write(line)
        print(
            "FINISH CV. {}, {}, {}, train acc/auc: {:.5f}/{:.5f}, test acc/auc: {:.5f}/{:.5f}, train time: {}\n"
                .format(data_src, model, feature, train_acc, train_auc, test_acc, test_auc, duration))

