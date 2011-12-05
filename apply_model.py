"""Script for running the model on new and exciting things."""

import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import multi_term
reload(multi_term)

plt.close('all')

cat = multi_term.Catalyst()
cat.T_a = 7207.
cat.A_arr = 1.005e7

cat.eta_t = np.zeros(50)

# for i in range(cat.eta_t.shape[0]):
    
