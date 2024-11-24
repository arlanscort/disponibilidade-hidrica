import numpy as np
from scipy.stats import pearsonr

def kge(Qobs, Qsim):
    mask = ~np.isnan(Qobs) & ~np.isnan(Qsim)
    Qobs = Qobs[mask]
    Qsim = Qsim[mask]

    r, _ = pearsonr(Qobs, Qsim)
    
    mu_obs = np.mean(Qobs)
    mu_sim = np.mean(Qsim)
    
    sigma_obs = np.std(Qobs)
    sigma_sim = np.std(Qsim)
    
    kge_value = 1 - np.sqrt((r - 1)**2 + (mu_sim / mu_obs - 1)**2 + (sigma_sim / sigma_obs - 1)**2)
    
    return kge_value


def nse(Qobs, Qsim):
    mask = ~np.isnan(Qobs) & ~np.isnan(Qsim)
    Qobs = Qobs[mask]
    Qsim = Qsim[mask]
    
    mu_obs = np.mean(Qobs)
    
    nse_value = 1 - np.sum((Qobs - Qsim)**2) / np.sum((Qobs - mu_obs)**2)
    
    return nse_value