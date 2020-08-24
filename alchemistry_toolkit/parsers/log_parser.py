import numpy as np

def logger(output, *args, **kwargs):
    print(*args, **kwargs)
    with open(output, "a") as f:
        print(file=f, *arsg, **kwargs)

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
            set_params(self, l, 'init-wl-deta', 'init_wl')
            set_params(self, l, 'wl-ratio')
            set_params(self, l, 'wl-scale')

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
        if hasattr(self, 'plumed_ver') is False:
            if free_energy == 'no':
                self.type = 'lambda_MD'
            elif free_energy == 'expanded':
                self.type = 'expanded_ensemble'

    def get_final_data(self):
        """
        This function parses the log file and finds out the count and weight
        of each labmda state at the last time frame.
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
            
        return final_counts, final_weights
    
    def get_equil_data(self):
        pass

        

                

        

                
            

