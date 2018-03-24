import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

class PlotManager:
    def __init__(self):
        pass

    def hist(self, count_list: list, show=True, save_path=None, xlabel_str='', ylabel_str='',
             force_x_axis_integer=True, **kwargs):
        """
        show=True: display
        show=False: save to path
        force_x_axis_integer=True: x axis shown as integer
        """
        ax = plt.figure().gca()
        plt.hist(count_list, **kwargs)
        plt.xlabel(xlabel_str)
        plt.ylabel(ylabel_str)

        # force y axis shown as integers anyway
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        if force_x_axis_integer:
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        if show:
            plt.show()
        else:
            if save_path:
                plt.savefig(save_path)
            else:
                plt.savefig('hist.png')
            plt.close('all')
