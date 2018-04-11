""" Tensorflow based factorization machine baseline """
import sys
sys.path.insert(0, '..')

from data_mangle.report_writer import ReportWriter
from baseline import Baseline
from tffm import TFFMClassifier
import tensorflow as tf
from utils.parser import parse_ml_parameters, parse_reader


class BaselineTFFM(Baseline):

    def print_model(self, model):
        """ return description of a model as a string """
        return 'FM_order{}_rank{}_l2regw{}_epoch{}'\
            .format(model.core.order, model.core.rank, model.core.reg, model.n_epochs)


if __name__ == "__main__":
    kwargs = parse_ml_parameters()

    dataset = 'lol' if not kwargs else kwargs.dataset
    density = 'sparse' if not kwargs else kwargs.density

    feature_config = 'champion_summoner_two_teams' if not kwargs else kwargs.fm_featconfig
    order = 2 if not kwargs else kwargs.fm_order
    rank = 200 if not kwargs else kwargs.fm_rank
    n_epochs = 5 if not kwargs else kwargs.fm_epoch
    reg = 0 if not kwargs else kwargs.fm_reg
    print('use parameter: dataset {}, feature_config: {}, order: {}, rank: {}, n_epochs: {}, reg: {}'
          .format(dataset, feature_config, order, rank, n_epochs, reg))
    reader = parse_reader(dataset, feature_config, density)

    fm_model = TFFMClassifier(
                        order=order,
                        rank=rank,
                        optimizer=tf.train.AdamOptimizer(),
                        n_epochs=n_epochs,
                        batch_size=1024,
                        init_std=0.0000000001,
                        reg=reg,
                        input_type='sparse')

    baseline = BaselineTFFM(models=[fm_model,
                                    # add more grid search models here ...
                                    ],
                            reader=reader,
                            writer=ReportWriter('result.csv'))
    baseline.cross_valid(show_progress=True)

