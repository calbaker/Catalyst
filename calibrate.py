"""Module for plotting results of first term model."""

import scipy as sp
import matplotlib.pyplot as mpl
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import experimental_data as expdata
reload(expdata)

data1 = expdata.Data()
data1.source = 'Osman July 3'
data1.Vdot = sp.array([250.]) * 1.e-6 / 60. 
data1.T_array = sp.arange(350., 625., 25.)
data1.HCin = sp.array([[4900., 4950., 4940.], [4900., 4920., 4950.],
                       [5150., 5170., 5140.], [5760., 5450., 5560.],
                       [5550., 5560., 5580.], [4880., 4930., 4950.],
                       [4870., 4900., 4880.], [5140., 5150., 5140.],
                       [5050., 5040., 5050.], [4590., 4500., 4540.],
                       [4570., 4620., 4610.]])
data1.HCout = sp.array([[3910., 3895., 3890.], [3730., 3740., 3720.],
                        [3470., 3510., 3500.], [2890., 2700., 2740.],
                        [1855., 1924., 1935.], [1277., 1310., 1320.],
                        [0753., 0725., 0718.], [0400., 0381., 0377.],
                        [0239., 0220., 0225.], [0111., 0098., 0103.],
                        [0053., 0041., 0045.]])
data1.set_eta()
