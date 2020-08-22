import numpy as np
import pytest 
import alchemistry_toolkit
from alchemistry_toolkit.parsers.log_parser import *

file_lambda_MetaD = 'sample_files/sys2.log'

class Test_EXE_LogInfo:
    def test_init__(self):
        # test_1: parse the log file of lambda-MetaD simulaiton
        # here we don't test the deactivated parameters
        test_1 = EXE_LogInfo(file_lambda_MetaD)
        assert test_1.dt == 0.002
        assert test_1.nstlog == 1000
        assert test_1.N_states == 9
        assert test_1.temp == 298
        assert test_1.plumed_ver == '2.7.0-dev'
        assert test_1.type == 'lambda-MetaD'
        assert test_1.init_w == list(np.zeros(9))
        assert test_1.fixed is False
        assert test_1.start == 506


        

