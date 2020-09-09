import os
import numpy as np
import pytest
from alchemistry_toolkit.parsers.log_parser import *
from alchemistry_toolkit.estimators.weights_generator import *

current_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_path, 'sample_inputs')

file_lambda_MetaD = data_path + '/lambda_MetaD.log'
file_EXE_updating = data_path + '/EXE_updating.log'
file_EXE_equilibrated = data_path + '/EXE_equilibrated.log'
file_EXE_fixed = data_path + '/EXE_fixed.log'

test_1 = EXE_LogInfo(file_lambda_MetaD)
test_2 = EXE_LogInfo(file_EXE_updating)
test_3 = EXE_LogInfo(file_EXE_equilibrated)
test_4 = EXE_LogInfo(file_EXE_fixed)

def test_adjust_weights():
    # Part 1: Tests with final counts
    c1, w1 = test_1.get_final_data()
    c2, w2 = test_2.get_final_data()
    c3, w3 = test_3.get_final_data()
    c4, w4 = test_4.get_final_data()
    
    w_adj_1, rmsd_1 = adjust_weights(c1, w1)
    w_adj_2, rmsd_2 = adjust_weights(c2, w2)
    w_adj_3, rmsd_3 = adjust_weights(c3, w3)
    w_adj_4, rmsd_4 = adjust_weights(c4, w4)

    expected_1 = np.array([0, 7.80622153, 14.18712932, 17.3500546 , 19.29906404, 
                           20.69265301, 20.67641217, 18.43027303, 15.59433296])
    expected_2 = np.array([0, 7.98738303, 14.86814794, 17.29113768, 18.76978532, 
                           20.08823888, 20.57088274, 19.34025672, 16.66820895])
    expected_3 = np.array([0, 7.81886552, 13.88378867, 16.77357959, 18.90675151, 
                           20.36135662, 21.2115675 , 18.51300374, 14.91915581])
    expected_4 = np.array([0, 7.8394568 , 13.93409582, 16.80223691, 18.89663727, 
                           20.36083512, 21.14485547, 18.69810792, 15.1645849 ])
                           
    np.testing.assert_array_almost_equal(expected_1, w_adj_1)
    np.testing.assert_array_almost_equal(expected_2, w_adj_2)
    np.testing.assert_array_almost_equal(expected_3, w_adj_3)
    np.testing.assert_array_almost_equal(expected_4, w_adj_4)
    
    assert rmsd_1 == 0.03154
    assert rmsd_2 == 0.30296
    assert rmsd_3 == 0.29085
    assert rmsd_4 == 0.36279

    # Part 2: Test with equilibrated counts
    _, _ = test_3.get_WL_data()
    c5 = test_3.equil_c  # equilibrated counts
    w5 = test_3.equil_w  # equilibrated weights
    w_adj_5, rmsd_5 = adjust_weights(c5, w5)
    expected_5 = np.array([0, 7.58441458, 13.8391983 , 16.88768357, 18.78953266,       
                           20.59009494, 21.27996925, 17.37912344, 14.87146973])
    np.testing.assert_array_almost_equal(expected_5, w_adj_5)
    assert rmsd_5 == 0.11119





    

