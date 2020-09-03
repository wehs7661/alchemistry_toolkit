import os
import numpy as np

def average_deltaF(hills_file, t_0, sample_cmd):

    # Modify the HILLS file
    f = open(hills_file, 'r')
    lines = f.readlines()
    f.close()
    
    metatext = ''
    for l in lines:
        if l[0] == '#':
            metatext += l[3:]  # remove "#! "
        else:
            break

    data = np.transpose(np.loadtxt(hills_file))
    time = data[0]
    height = data[-2]
    t_f = time[-1]

    for i in range(len(height)):
        if time[i] > t_0:  # t_0 in ps
            height *= (t_f - time[i]) / (t_f - t_0)
    data[-2] = height
    np.savetxt(hills_file + "_modified", np.transpose(data), header=metatext[:-1], comments='#! ', delimiter='    ')

    # Sum up the modified hills and get delta_F
    os.system(sample_cmd + f" --hills {hills_file + '_modified'}")

        
        




# class free_energy_alchemlyb 



