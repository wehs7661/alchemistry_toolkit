import matplotlib.pyplot as plt
from matplotlib import rc

def customize_font():
    rc('font', **{
       'family': 'sans-serif',
       'sans-serif': ['DejaVu Sans'],
       'size': 10
    })
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family='serif')

def plot_sci(x, y):
    if max(abs(x)) >= 10000:
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))  
    if max(abs(y)) >= 10000:
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

