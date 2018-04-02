import optparse
import sys


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
    (kwargs, args) = parser.parse_args()
    return kwargs
