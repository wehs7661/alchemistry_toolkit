import os 
import numpy as np
import pytest
from alchemistry_toolkit.visuals.plot_2d import *

def test_plot_xy():
    x = np.arange(0, 6000, 100)
    y = 2 * x
    assert os.path.isfile('test.png') is False
    
    plot_xy(x, y, '$ x $', '$ y $', 'x as a function of y', 'test.png')
    assert os.path.isfile('test.png') is True

    os.system('rm test.png')


