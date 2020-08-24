import numpy as np
import pytest
import copy
import alchemistry_toolkit
from alchemistry_toolkit.parsers.log_parser import *

file_lambda_MetaD = 'sample_files/lambda_MetaD.log'
file_EXE_updating = 'sample_files/EXE_updating.log'
file_EXE_equilibrated = 'sample_files/EXE_equilibrated.log'
file_EXE_fixed = 'sample_files/EXE_fixed.log'

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
                      'input': 'sample_files/lambda_MetaD.log',
                      'dt': 0.002, 'nstlog': 1000, 'N_states': 9,
                      'fixed': False, 'cutoff': 0.001, 'wl-scale': 0.8,
                      'wl-ratio': 0.8, 'temp': 298.0, 'plumed_ver': '2.7.0-dev',
                      'type': 'lambda-MetaD', 'start': 506}

        # the metadata of EXE_upating.log and EXE_equilibrated.log are the same
        expected_2 = {'init_w': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
                      'input': 'sample_files/EXE_updating.log', 'dt': 0.002, 
                      'nstlog': 1000.0, 'N_states': 9, 'fixed': False, 'cutoff': 0.001, 
                      'wl-scale': 0.8, 'wl-ratio': 0.8, 'temp': 298.0, 'start': 455, 
                      'type': 'expanded_ensemble'}   
        
        expected_3 = copy.deepcopy(expected_2)
        expected_3['input'] = 'sample_files/EXE_equilibrated.log'

        expected_4 = {'init_w': [0.0, 7.67256, 13.8818, 16.9028, 18.8082, 20.5498, 21.2318, 17.6905, 14.8862], 
                      'input': 'sample_files/EXE_fixed.log', 
                      'dt': 0.002, 'nstlog': 1000.0, 'N_states': 9, 
                      'fixed': True, 'wl-scale': 0.8, 'wl-ratio': 0.8, 'temp': 298.0, 
                      'start': 454, 'type': 'expanded_ensemble'}

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

        assert (c1 == test_1.get_final_data()[0]).all()
        assert (w1 == test_1.get_final_data()[1]).all()
        assert (c2 == test_2.get_final_data()[0]).all()
        assert (w2 == test_2.get_final_data()[1]).all()
        assert (c3 == test_3.get_final_data()[0]).all()
        assert (w3 == test_3.get_final_data()[1]).all()
        assert (c4 == test_4.get_final_data()[0]).all()
        assert (w4 == test_4.get_final_data()[1]).all()

        assert test_1.final_t == 5000
        assert test_2.final_t == 1000
        assert test_3.final_t == 5000
        assert test_4.final_t == 5000


