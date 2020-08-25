import os 
import sys
import numpy as np
import copy 
sys.path.append('../')
from utils import ParameterError
#from alchemistry_toolkit.utils import ParameterError

global kb, Na
kb = 1.38064852E-23     # Boltzmann constant
Na = 6.0221409E23       # Avogadro's number

def logger(output, *args, **kwargs):
    print(*args, **kwargs)
    with open(output, "a") as f:
        print(file=f, *args, **kwargs)

def set_params(obj, line, param_name, attr_name=None, dtype=float):
    """
    Assign the parameters in the log file as attributes of an object (self).

    Parameters
    ----------
    obj (object): any Python object, typically self
    line (str): a certain line in the log file
    param_name (str): the name of the parameter
    attr_name (str): the name of the attribute
    dtype (type): the data type of the attribute
    """
    if attr_name is None:
        attr_name = param_name
    if param_name in line and hasattr(obj, attr_name) is False:
        setattr(obj, attr_name, dtype(line.split('=')[1]))
    

class EXE_LogInfo:

    def __init__(self, logfile):
        """
        Assign the simulation parameters of expanded ensemble or alchemical 
        metadynamics as attributes by parsing the metadat of the log file.

        Parameters
        ----------
        logfile (str): The filename of the log file
        """
        f = open(logfile, 'r')
        lines = f.readlines()
        f.close()

        line_n = -1  # line number (starts from 0)
        self.init_w = []
        self.input = logfile

        for l in lines:
            line_n += 1

            # general parameters
            set_params(self, l, 'dt  ', 'dt')
            set_params(self, l, 'nstlog')
            set_params(self, l, 'n-lambdas', 'N_states', int)
            if 'ref-t' in l and hasattr(self, 'temp') is False:
                self.temp = float(l.split(':')[1])

            # parameters specific for EXE (deactivated in lambda-MetaD)
            set_params(self, l, 'weight-equil-wl-delta', 'cutoff')
            set_params(self, l, 'init-wl-delta', 'init_wl')
            set_params(self, l, 'wl-ratio', 'wl_ratio')
            set_params(self, l, 'wl-scale', 'wl_scale')

            # parameters specific for lambda-MetaD
            if 'PLUMED: Version: ' in l and hasattr(self, 'type') is False:
                self.plumed_ver = l.split('Version: ')[1].split(' ')[0]
                self.type = 'lambda-MetaD'

            # parameters work for either EXE or lambda-MetaD or others
            if 'init-lambda-weights[' in l:
                self.init_w.append(float(l.split('=')[1]))
            if 'lmc-stats' in l and hasattr(self, 'fixed') is False:
                if l.split('=')[1].split()[0] == 'no':
                    self.fixed = True 
                else:
                    self.fixed = False
            if 'free-energy' in l and hasattr(self, 'type') is False:
                free_energy = l.split('=')[1].split()[0]
            if 'Started mdrun' in l:
                self.start = line_n  # the line number that the simulation starts
                break     

        # Determine the simulation type
        if hasattr(self, 'plumed_ver') is False and free_energy == 'expanded':
            self.type = 'expanded_ensemble'

    def get_final_data(self):
        """
        This function parses the log file and finds out the count and weight
        of each labmda state at the last time frame.

        Returns
        -------
        final_counts (np.array): the counts of states at the last time frame
        final_weights (np.array): the weights of states at the last time frame
        """
        f = open(self.input, 'r')
        lines = f.readlines()
        f.close()
        lines.reverse()

        find_found = False
        line_n = -1  # the line number from the bottom of the file (starts from 0)
        final_counts, final_weights = np.zeros(self.N_states), np.zeros(self.N_states)
        for l in lines:
            line_n += 1

            if 'MC-lambda information' in l: 
                final_found = True
                # The position of the column name in EXE_updating is different from others
                if 'Wang-Landau incrementor is: ' in lines[line_n - 1]: 
                    self.EXE_status = 'updating'
                    data_line = line_n - 3   # data starts from here
                else:
                    data_line = line_n - 2

                # Start extracting data
                for i in range(self.N_states):
                    if lines[data_line - i].split()[-1] == '<<':
                        final_weights[i] = float(lines[data_line - i].split()[-3])
                        final_counts[i] = float(lines[data_line - i].split()[-4])
                    else:
                        final_weights[i] = float(lines[data_line - i].split()[-2])
                        final_counts[i] = float(lines[data_line - i].split()[-3])

            if '  Step  ' in l and final_found is True:
                if hasattr(self, 'final_t') is False:
                    self.final_t = float(lines[line_n - 1].split()[1])  # in ps
                break 

        self.err_kt_f = np.round(np.abs(np.log(final_counts[0] / final_counts[-1])), 5)
        self.err_kcal_f = np.round(self.err_kt_f * (kb * Na * float(self.temp) / 1000) * 0.23900573613, 5)
            
        return final_counts, final_weights
    
    def get_WL_data(self):
        """
        This function parses the log file and performs the following tasks:
        1. Extract the data of WL incrementor as a function of time
        2. Extract the data of free energy difference (between the coupled and 
            uncoupled state) as a function of time
        3. Assign equilibrated weights (if exist) as an attribute

        Returns
        -------
        update_time (np.array): the array of time at which the WL incrementor was updated
        delta_w (np.array): Wang Landau incrementor as a function of time
        """
        f = open(self.input, 'r')
        lines = f.readlines()
        f.close()

        delta_w = [self.init_wl]  # Wang-Landau incrementor \delta_w
        step = [0]     # simulation steps at which the WL incrementor was updated
        n_updates = 0
        line_n = self.start

        for l in lines[self.start:]: # skip the metadata
            line_n += 1 

            if 'weights are now:' in l:
                if hasattr(self, 'EXE_status') is False:
                    self.EXE_status = 'updating'
                n_updates += 1
                delta_w.append(np.round(self.init_wl * self.wl_scale ** n_updates, 7))
                step.append(int(l.split(':')[0].split()[1]))

            # Info about weights equilibration
            if 'Weights have equilibrated' in l :
                # Part 1: Basic information
                self.EXE_status = 'equilibrated'
                self.equil_c = []   # equilibrated counts
                self.equil_w = []   # equilibrated weights
                equil_step = l.split(':')[0].split()[1]
                self.equil_t = np.round(float(equil_step) * self.dt / 1000, 5)  # units: ns

                # Part 2: Search for equilibrated weights
                search_lines = lines[line_n - 8 : line_n]  
                for l_search in search_lines:
                    if 'weights are now: ' in l_search:
                        self.equil_w = [float(l_search.split(':')[2].split()[i]) for i in range(self.N_states)]

                        # convert to str:
                        # " ".join([str(self.equil_w[i]) for i in range(len(self.equil_w))])

                # Part 3: Search for equilibrated counts
                search_lines = lines[line_n - (30 + self.N_states): line_n]  # for searching equilibrated counts
                search_line_n = line_n - (30 + self.N_states)
                for l_search in search_lines:
                    search_line_n += 1
                    if 'MC-lambda information' in l_search:  # lines[search_line_n - 1]
                        for i in range(self.N_states):
                            if lines[search_line_n + 2 + i].split()[-1] == '<<':
                                self.equil_c.append(float(lines[search_line_n + 2 + i].split()[-4]))
                            else:
                                self.equil_c.append(float(lines[search_line_n + 2 + i].split()[-3]))

                # Part 4: N_ratio (max and min)
                avg_counts =  sum(self.equil_c) / len(self.equil_c)
                self.max_Nratio = np.round(max(self.equil_c) / avg_counts, 5)
                self.min_Nratio = np.round(min(self.equil_c) / avg_counts, 5)

                # Part 5: Uncertainty estimation based on equilibrated data
                kb = 1.38064852E-23     # Boltzmann constant
                Na = 6.0221409E23       # Avogadro's number
                self.err_kt_eq = np.round(np.abs(np.log(self.equil_c[0] / self.equil_c[-1])), 5)
                self.err_kcal_eq = np.round(self.err_kt_eq * (kb * Na * float(self.temp) / 1000) * 0.23900573613, 5)
                
                break 
        
        update_time = np.array(step) * self.dt / 1000  # time array for plotting (units :ns)
        delta_w = np.array(delta_w)

        return update_time, delta_w

    def get_avg_weights(self, avg_len):
        """
        This function performs the weights average calculation.

        Parameters
        ----------
        avg_len (float): the period which the weights average over. Value of 1 means averaing 
                         the last 1 ns of the simulation.
        
        Returns
        -------
        weights_avg (np.array): the average of the weights over a certain period
        free_energy_diff (np.array): free energy difference as a function of time
        """
        # This function does not apply to self.EXE_status == 'equlibrated' or 'fixed'
        if hasattr(self, 'final_t') is False:
            _, _ = self.get_final_data()
        avg_start = self.final_t - avg_len * 1000   # units: ps
        if avg_start < 0: 
            raise ParameterError('Warning: The starting point of the weights average calculation is less than 0!')

        f = open(self.input, 'r')
        lines = f.readlines()
        f.close()

        search_start = False 
        line_n = self.start
        weights = []        # to store weights at each time frame to be averaged
        weights_all = []    # a list of lists of weights at different time frames

        # Part 1: Average weights calculation
        for l in lines[self.start:]:    # skip the metadata
            line_n += 1

            if 'Step' in l and 'Time' in l:
                if (avg_start / self.dt) == float(lines[line_n].split()[0]) and \
                    avg_start == float(lines[line_n].split()[1]):
                    search_start = True 
                
            if 'MC-lambda information' in l and search_start is True:
                for i in range(self.N_states):
                    if hasattr(self, 'EXE_status') is True and self.EXE_status == 'updating':
                        if lines[line_n + i + 2].split()[-1] == '<<':
                            weights.append(float(lines[line_n + i + 2].split()[-3]))
                        else:
                            weights.append(float(lines[line_n + i + 2].split()[-2]))
                    else:   # lambda-MetaD
                        if lines[line_n + i + 1].split()[-1] == '<<':
                            weights.append(float(lines[line_n + i + 1].split()[-3]))
                        else:
                            weights.append(float(lines[line_n + i + 1].split()[-2]))
                weights_all.append(weights)
                weights = []

        weights_all = np.array(weights_all)
        weights_avg = np.array(list(map(lambda x: np.round(x, 5), sum(weights_all)/len(weights_all))))

        # Part 2: Free energy estimate from averaging (more suitable for 1D lambda-MetaD)
        free_energy_diff = np.array([weights_all[i][-1] for i in range(len(weights_all))])

        return weights_avg, free_energy_diff


        



                












        

        

                

        

                
            

