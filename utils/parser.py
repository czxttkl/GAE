import optparse
import sys
from data_mangle.cv_fold_sparse_reader import CVFoldSparseReader
from data_mangle.cv_fold_lol_sparse_reader import CVFoldLoLSparseReader
from utils import constants


def parse_parameters():
    if len(sys.argv) < 2:
        print('no argument set. use default.')
        return None

    parser = optparse.OptionParser(usage="usage: %prog [options]")
    parser.add_option("--fm_order", dest="fm_order", type="int", default=0)
    parser.add_option("--fm_rank", dest="fm_rank", type="int", default=0)
    parser.add_option("--fm_epoch", dest="fm_epoch", type="int", default=0)
    parser.add_option("--fm_reg", dest="fm_reg", type="float", default=0.0)
    parser.add_option("--fm_featconfig", dest="fm_featconfig", type="string", default='')
    parser.add_option("--dataset", dest='dataset', type='string', default='')
    (kwargs, args) = parser.parse_args()
    return kwargs


def parse_reader(dataset, feature_config):
    if dataset == 'lol':
        reader = CVFoldLoLSparseReader(data_path=constants.lol_pickle, folds=10, feature_config=feature_config)
    elif dataset == 'dota':
        reader = CVFoldSparseReader(data_path=constants.dota_pickle, folds=10, feature_config=feature_config)
    elif dataset == 'dota2':
        reader = CVFoldSparseReader(data_path=constants.dota2_pickle, folds=10, feature_config=feature_config)
    else:
        raise NotImplementedError
    return reader

