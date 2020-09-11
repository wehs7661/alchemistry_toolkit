import os
import numpy as np
import pytest
from alchemistry_toolkit.analysis.visualization_methods import *

current_path = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(current_path, 'sample_outputs')

@pytest.fixture
def plot_dict():
    input_dict = {}
    input_dict['xlabel'] = '$ x $'
    input_dict['ylabel'] = '$ y $'
    input_dict['title'] = 'x as a function of time'
    input_dict['png_name'] = 'test.png'

    return input_dict

def test_plot_xy(plot_dict):
    visuals = Visualization()
    x = np.arange(0, 12000, 100)
    y = 2 * x
    plot_dict['png_name'] = output_path + '/test_xy.png'
    if os.path.isfile(output_path + '/test_xy.png') is True:
        os.system(f'rm {output_path + "/test_xy.png"}')
    visuals.plot_xy(x, y, plot_dict)
    assert os.path.isfile(output_path + '/test_xy.png') is True

def test_plot_bar(plot_dict):
    visuals = Visualization()
    x = np.arange(10)
    h = np.array([2, 3, 4, 2, 5, 6, 3, 6, 19, 8])
    plot_dict['title'] = 'The histogram of $ x $'
    plot_dict['png_name'] = output_path + '/test_bar.png'
    if os.path.isfile(output_path + '/test_bar.png') is True:
        os.system(f'rm {output_path + "/test_bar.png"}')
    visuals.plot_histogram(x, h, plot_dict)
    assert os.path.isfile(output_path + '/test_bar.png') is True


def test_plot_matrix(plot_dict):
    visuals = Visualization()
    rng = np.random.RandomState(1)  # a separate random number generator (RNG)
    matrix = rng.rand(10, 10) * 0.1   # min: 0.00273 < default threshold
    plot_dict = {'title': 'Test matrix', 'var_name': 'n', 'png_name': output_path + '/test_matrix.png'}
    if os.path.isfile(output_path + '/test_matrix.png') is True:
        os.system(f'rm {output_path + "/test_matrix.png"}')
    visuals.plot_matrix(matrix, plot_dict=plot_dict)
    assert os.path.isfile(output_path + '/test_matrix.png') is True

