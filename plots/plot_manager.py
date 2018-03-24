import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt


class PlotManager:
    def __init__(self):
        pass

    def hist(self, count_list: list, show=True, save_path=None, **kwargs):
        """
        show=True: display
        show=False: save to path
        """
        plt.figure()
        plt.hist(count_list, **kwargs)
        if show:
            plt.show()
        else:
            if save_path:
                plt.savefig(save_path)
            else:
                plt.savefig('hist.png')
            plt.close('all')
