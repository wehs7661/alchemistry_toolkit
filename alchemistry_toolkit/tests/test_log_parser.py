import os
import numpy as np
import pytest
import copy
import alchemistry_toolkit
from alchemistry_toolkit.parsers.log_parser import *

current_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_path, 'sample_files')

file_lambda_MetaD = data_path + '/lambda_MetaD.log'
file_EXE_updating = data_path + '/EXE_updating.log'
file_EXE_equilibrated = data_path + '/EXE_equilibrated.log'
file_EXE_fixed = data_path + '/EXE_fixed.log'

# Test_1: lambda-MetaD simulaiton
test_1 = EXE_LogInfo(file_lambda_MetaD)

# Test 2: EXE with weights being updated by the WL algorithm (not yet equilibrated)
test_2 = EXE_LogInfo(file_EXE_updating)

# Test 3: EXE with weights being updated by the WL algorithm (equilibrated)
test_3 = EXE_LogInfo(file_EXE_equilibrated)

# Test_4: EXE with fixed weights
test_4 = EXE_LogInfo(file_EXE_fixed)

class Test_EXE_LogInfo:
         
    def test_init(self):
        expected_1 = {'init_w': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      'input': file_lambda_MetaD, 'dt': 0.002, 
                      'nstlog': 1000, 'N_states': 9, 'fixed': False, 'cutoff': 0.001, 
                      'wl_scale': 0.8, 'wl_ratio': 0.8, 'init_wl': 0.5, 'temp': 298.0, 
                      'plumed_ver': '2.7.0-dev', 'type': 'lambda-MetaD', 'start': 506}

        # the metadata of EXE_upating.log and EXE_equilibrated.log are the same
        expected_2 = {'init_w': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
                      'input': file_EXE_updating, 'dt': 0.002, 
                      'nstlog': 1000, 'N_states': 9, 'fixed': False, 'cutoff': 0.001, 
                      'wl_scale': 0.8, 'wl_ratio': 0.8, 'init_wl': 0.5, 'temp': 298.0, 
                      'start': 455, 'type': 'expanded_ensemble'}   
        
        expected_3 = copy.deepcopy(expected_2)
        expected_3['input'] = file_EXE_equilibrated

        expected_4 = {'init_w': [0.0, 7.67256, 13.8818, 16.9028, 18.8082, 20.5498, 21.2318, 17.6905, 14.8862], 
                      'input': file_EXE_fixed, 'dt': 0.002, 
                      'nstlog': 1000, 'N_states': 9, 'fixed': True, 'wl_scale': 0.8, 
                      'wl_ratio': 0.8, 'init_wl': 1, 'temp': 298.0, 'start': 454, 
                      'type': 'expanded_ensemble'}

        assert vars(test_1) == expected_1
        assert vars(test_2) == expected_2
        assert vars(test_3) == expected_3
        assert vars(test_4) == expected_4

    def test_get_final_data(self):
        c1 = np.array([31385, 29431, 27909, 27179, 26740, 26431, 26432, 26926, 27567])
        w1 = np.array([0, 7.74194, 14.13403, 17.32355, 19.28278, 20.68103, 20.67645, 18.44879, 15.61786])
        c2 = np.array([435, 370, 218, 222, 272, 313, 343, 197, 135])
        w2 = np.array([0, 7.82554, 14.33914, 17.30932, 18.97291, 20.22864, 20.66241, 18.78573, 16.29028])
        c3 = np.array([13776, 11901, 11877, 13516, 12248, 14788, 15091, 6630, 6415])
        w3 = np.array([0, 7.67256, 13.88177, 16.90285, 18.80824, 20.54981, 21.23185, 17.69051, 14.88619])
        c4 = np.array([35254, 29835, 28314, 31311, 28662, 34624, 37771, 13790, 10439])
        w4 = copy.deepcopy(w3)

        np.testing.assert_array_almost_equal(c1, test_1.get_final_data()[0], 10)
        np.testing.assert_array_almost_equal(w1, test_1.get_final_data()[1], 10)
        np.testing.assert_array_almost_equal(c2, test_2.get_final_data()[0], 10)
        np.testing.assert_array_almost_equal(w2, test_2.get_final_data()[1], 10)
        np.testing.assert_array_almost_equal(c3, test_3.get_final_data()[0], 10)
        np.testing.assert_array_almost_equal(w3, test_3.get_final_data()[1], 10)
        np.testing.assert_array_almost_equal(c4, test_4.get_final_data()[0], 10)
        np.testing.assert_array_almost_equal(w4, test_4.get_final_data()[1], 10)

        assert test_1.final_t == 5000
        assert test_2.final_t == 1000
        assert test_3.final_t == 5000
        assert test_4.final_t == 5000

        assert test_2.EXE_status == 'updating'

    
    def test_get_WL_data(self):
        # Test 1: EXE_updating
        t1 = np.array([0, 0.01758, 0.02574, 0.04432, 0.062, 0.07464, 0.10316, 
                       0.12102, 0.1402, 0.1864, 0.24034, 0.26614, 0.31396, 
                       0.32938, 0.42008, 0.5014, 0.56918, 0.6576, 0.7434, 0.9499])
        w1 = np.array([0.5, 0.4, 0.32, 0.256, 0.2048, 0.16384, 0.131072 , 0.1048576, 
                       0.0838861, 0.0671089, 0.0536871, 0.0429497, 0.0343597, 
                       0.0274878, 0.0219902, 0.0175922, 0.0140737, 0.011259 ,
                       0.0090072, 0.0072058])

        np.testing.assert_array_almost_equal(t1, test_2.get_WL_data()[0], 10)
        np.testing.assert_array_almost_equal(w1, test_2.get_WL_data()[1], 10)
        assert test_2.EXE_status == 'updating'

        # Test 2: EXE_equilibrated
        t2 = np.array([0, 0.01498, 0.02138, 0.0353 , 0.0536 , 0.07438, 0.09064,
                       0.11154, 0.13876, 0.18484, 0.21016, 0.26386, 0.31684, 0.33002,
                       0.3672, 0.43502, 0.50318, 0.58672, 0.67496, 0.7618 , 0.89586,
                       0.9931, 1.175, 1.27582, 1.57056, 1.66066, 1.90268, 2.19516,
                       2.87514])
        w2 = np.array([0.5, 0.4, 0.32, 0.256, 0.2048, 0.16384, 0.131072 , 0.1048576, 
                       0.0838861, 0.0671089, 0.0536871, 0.0429497, 0.0343597, 0.0274878, 
                       0.0219902, 0.0175922, 0.0140737, 0.011259, 0.0090072, 0.0072058, 
                       0.0057646, 0.0046117, 0.0036893, 0.0029515, 0.0023612, 0.0018889, 
                       0.0015112, 0.0012089, 0.0009671])
        equil_c = np.array([3158.0, 3449.0, 3599.0, 3654.0, 3723.0, 3576.0, 3408.0, 4653.0, 4722.0])
        equil_w = ' 0.00000 7.67256 13.88177 16.90285 18.80824 20.54981 21.23185 17.69051 14.88619\n'

        np.testing.assert_array_almost_equal(t2, test_3.get_WL_data()[0], 10)
        np.testing.assert_array_almost_equal(w2, test_3.get_WL_data()[1], 10)
        np.testing.assert_array_almost_equal(equil_c, test_3.equil_c, 10)
        assert test_3.EXE_status == 'equilibrated'
        assert test_3.equil_t == 2.87516
        assert test_3.equil_w == equil_w
        

    



