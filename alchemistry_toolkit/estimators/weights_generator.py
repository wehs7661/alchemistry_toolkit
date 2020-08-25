import sys
import numpy as np 
sys.path.append('../')
from parsers.log_parser import EXE_LogInfo

def adjust_weights(counts, weights):
    """
    This function adjusts weights using the following formula:
    g'_k = g_k + ln(count_(k - 1) / count_k)
    Common choicse are using final counts to adjust the final weights 
    or using equilibrated counts to adjust the equilibrated weights

    Parameters
    ----------
    counts (np.array): the counts of all lambda states
    weights (np.array): the weights of all lambda states

    Returns
    -------
    weights_adjusted (np.array): adjusted weights
    RMSD (float): the RMSD value of the adjusted weights (ref: original weights)
    """
    weights_adjusted = np.zeros(len(weights))
    for i in range(len(weights)):
        if i == 0:
            weights_adjusted[i] = 0
        else:
            weights_adjusted[i] = weights[i] + np.log(counts[i - 1] / counts[i])
    RMSD = np.round(np.sqrt((1/len(weights) * sum((weights - weights_adjusted) ** 2))), 5)

    return weights_adjusted, RMSD

