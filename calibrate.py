"""Module for plotting results of first term model."""

import scipy as sp
import matplotlib.pyplot as mpl
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import experimental_data as expdata

data1 = expdata.Data()
data1.source = '300sccm 20nmPtPd VariedT.xls'

# data1.T = sp.array([350., 400., 450., 500., 550., 600.])
# data1.HCin = sp.array([3830., 3880., 3860., 3800., 3840., 3850.])
# data1.HCout = sp.array([3780., 3730., 3660., 3560., 3380., 1714.])

data1.Vdot = sp.array([300.]) * 1.e-6 / 60. 
data1.T_array = sp.array([350., 450., 550])
data1.HCin = sp.array([3830., 3860., 3840])
data1.HCout = sp.array([3780., 3660., 3380]) 
data1.set_eta()

data1.A_arr = 6.e10 
data1.T_a = 13.2e3

