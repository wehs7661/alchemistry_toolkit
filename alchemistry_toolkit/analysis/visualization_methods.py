import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import cm

class Plot_Utils:
    def customize_font(self):
        rc('font', **{
           'family': 'sans-serif',
           'sans-serif': ['DejaVu Sans'],
           'size': 10
        })
        rc('mathtext', **{'default': 'regular'})
        plt.rc('font', family='serif')

    def plot_sci(self, x, y):
        if max(abs(x)) >= 10000:
            plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        if max(abs(y)) >= 10000:
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

class Visualization(Plot_Utils):
    def plot_xy(self, x, y, plot_dict=None, style=True):
        """
        This function plot the dependent variable as a function of the independent 
        variable given a 2D data set.

        Parameters
        ----------
        x         (array-like): the data of the independent variable
        y         (array-like): the data of the dependent variable
        plot_dict (dict): a dictionary of settings, including labels, title, and output name
        style     (bool): whether the customized font in Plot_Utils should be used
        """
        if plot_dict is None:
            plot_dict = {'xlabel': None, 'ylabel': None, 'title': None, 'png_name': None}
        if style:
            self.customize_font()
        plt.figure()
        self.plot_sci(x, y)
        plt.plot(x, y)
        plt.xlabel(plot_dict['xlabel'])
        plt.ylabel(plot_dict['ylabel'])
        plt.title(plot_dict['title'])
        plt.grid()
        plt.savefig(plot_dict['png_name'], dpi=600)

    def plot_histogram(self, x, h, plot_dict=None, style=True):
        """
        This function plot a histogram given the counts of a variable.

        Parameters
        ----------
        x          (array-like): the x coordinates of the bars
        h          (array-like): the height(s) of the bars
        plot_dict  (dict): a dictionary of settings, incluing labels, title and output name
        style      (bool): whether the customized fonts in Plot_Utils should be used
        """
        if plot_dict is None:
            plot_dict = {'xlabel': None, 'ylabel': None, 'title': None, 'png_name': None}
        if style:
            self.customize_font()
        plt.figure()
        self.plot_sci(x, h)
        plt.bar(x, height=h)
        plt.xlabel(plot_dict['xlabel'])
        plt.ylabel(plot_dict['ylabel'])
        plt.title(plot_dict['title'])
        plt.minorticks_on()
        plt.grid()
        plt.savefig(plot_dict['png_name'], dpi=600) 

    def plot_matrix(self, matrix, start_idx=0, threshold=0.005, plot_dict=None, style=True):
        """
        This function plot a heatmap based on a 2D matrix.

        Parameters
        ----------
        matrix     (2d-array): the matrix to be plotted
        start_idx  (int): the data with indices below start_idx will be truncated
        threshold  (float): grids with values below the threshold will not be annotated with their values
        plot_dict  (dict): a dictionary of settings, including title and the names of the variable and the output.
        style      (bool): whether the customized font in Plot_Utils should be used
        """
        if plot_dict is None:
            plot_dict = {'title': None, 'var_name': None, 'png_name': None}
        if style:
            self.customize_font()
        
        K = len(matrix)
        plt.figure(figsize=(K / 3, K / 3))
        annot_matrix = np.zeros([K, K])   # for annotations
        if K > 5:
            annot_size = 6
        else:
            annot_size = 4
        
        for i in range(K):
            for j in range(K):
                annot_matrix[i, j] = round(matrix[i, j], 2)
        
        x_tick_labels = y_tick_labels = np.arange(start_idx, start_idx + K)
        ax = sns.heatmap(matrix, cmap="YlGnBu", linecolor='silver', linewidth=0.25,
                        annot=annot_matrix, annot_kws={"size": annot_size}, 
                        mask=matrix < threshold, square=True, fmt='.2f', cbar=False, 
                        xticklabels=x_tick_labels, yticklabels=y_tick_labels)

        # highlight the diagonal with bold texts
        for txt in ax.texts:
            if txt.get_position()[0] == txt.get_position()[1]:
                txt.set_weight('bold')

        ax.xaxis.tick_top()
        ax.tick_params(length=0)
        cmap = cm.get_cmap('YlGnBu')   # to get the facecolor
        ax.set_facecolor(cmap(0))      # use the brightest color (value = 0)
        for _, spine in ax.spines.items():
            spine.set_visible(True)    # add frames to the heat map
        plt.annotate(plot_dict['var_name'], xy=(0, 0), xytext=(-0.45, -0.20))
        plt.title(plot_dict['title'], fontsize=14, weight='bold')
        plt.tight_layout(pad=1.0)
        plt.savefig(plot_dict['png_name'], dpi=600)
