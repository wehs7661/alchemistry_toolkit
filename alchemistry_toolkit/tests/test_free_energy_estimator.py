import os
import numpy as np
import pytest
from alchemistry_toolkit.estimators.free_energy_estimator import *

current_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_path, 'sample_files')
hills_file = data_path + "/HILLS_2D"

def test_average_deltaF():
    sample_cmd = 'plumed sum_hills --idw lambda --min -pi,0 --max pi,8 --bin 50,8 --outfile fes_test'
    average_deltaF(hills_file, 19000, sample_cmd)










