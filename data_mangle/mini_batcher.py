""" Generate Mini batches """
import numpy


class MiniBatcher(object):

    def __init__(self, batch_size, seed):
        self.batch_size = batch_size
        numpy.random.seed(seed)

    def next_batch(self, *args):
        K = len(args)
        res = [0] * K
        N = len(args[0])
        batch_idx = numpy.random.choice(N, self.batch_size)
        for idx, arg in enumerate(args):
            res[idx] = arg[batch_idx]
        return res