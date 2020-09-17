import os
import numpy as np
import pytest
from alchemistry_toolkit.estimators.free_energy_estimator import *

current_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_path, 'sample_inputs')
hills_file = data_path + "/HILLS_2D"
test = FreeEnergy_HILLS(hills_file)

class Test_FreeEnergy_HILLS:
    
    def test_init(self):
        assert test.hills == hills_file
    
    def test_deltaF_average(self):
        hills_modified = hills_file + '_modified'
        sample_cmd = 'plumed sum_hills --idw lambda --min -pi,0 --max pi,8 --bin 50,8 --outfile fes_test --kt 2.4777090399459767'
        # 2.4777090399459767
        assert os.path.isfile(hills_modified) is False
        assert os.path.isfile('fes_test') is False

        delta_f_1 = test.deltaF_average(sample_cmd, 18000)
        assert os.path.isfile(hills_modified) is True
        assert os.path.isfile('fes_test') is True
        assert delta_f_1 == 18.253219211

        os.system('rm fes_test')
        os.system(f'rm {hills_modified}')

        delta_f_2 = test.deltaF_average(sample_cmd, 18000, 20000)
        assert os.path.isfile(hills_modified) is True
        assert os.path.isfile('fes_test') is True
        assert delta_f_1 == delta_f_2
    
        os.system('rm fes_test')
        os.system(f'rm {hills_modified}')

    def test_deltaF_evolution(self):
        sample_cmd_1 = f'plumed sum_hills --hills {hills_file} --min -pi,0 --max pi,8 --bin 50,8'
        sample_cmd_2 = f'plumed sum_hills --hills {hills_file} --idw lambda --min -pi,0 --max pi,8 --bin 50,8 --kt 2.4777090399459767'
        delta_F_1 = test.deltaF_evolution(sample_cmd_1, 500, stride=1000)
        delta_F_2 = test.deltaF_evolution(sample_cmd_2, 500, stride=1000)
        
        # np.testing.assert_array_almost_equal(delta_F_1, delta_F_2)









