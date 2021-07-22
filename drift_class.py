import dill as pickle
import numpy as np
import math
from GBM2 import Brownian

# Base class for different drifts
class Drift(Brownian):
    def __init__(self, deltaT, dt, s0, musig) -> None:
        """
        Params:
        dT - Duration, for plug and play with BSE
        metadata - Metadata for the drift
        stock price generates GBM with drift using 
        functions defined below.
        """
        
        # Get the total number of time steps
        super().__init__(s0=s0)
        self.n_steps = int(deltaT/dt)

        # Init musig class
        self.musig = musig(n_steps = self.n_steps)
        self.gbm_offset_vec = self.stock_price(mu_fn=self.musig.sig, \
            sigma_fn=self.musig.mu, dt=dt, deltaT=deltaT)
        
        self.dt = dt
        self.meta_data = {
            'drift_type': 'abrupt',
            'drift_times': ['1.9293','38.9383'],
            'params_varied': ['mu','sigma'],
        }

    
    def dump_offset(self, path):
        np.save(path, np.array(self.gbm_offset_vec))

    def offset_fn(self, t):
        """
        Returns the offset 
        """
        try:
            offset = self.gbm_offset_vec[math.floor(t/self.dt)]
            return int(round(offset, 0))
        except:
            # For some reason, some time idx seem to go off the end
            print('WARNING: schedule offset clipped')
            return int(round(self.gbm_offset_vec[-1],0))
    

class MuSigma:
    def __init__(self, n_steps) -> None:
        self.n_steps = n_steps
    
    def mu(self, n):
        t_pct = (n/self.n_steps)
        return 0.000123
    
    def sig(self, n):
        t_pct = (n/self.n_steps)
        return 0.0000123


cls = Drift(600,0.125,50, MuSigma)

with open('pickle_test', "wb") as pf:
    pickle.dump(cls, pf)