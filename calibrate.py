"""Module for plotting results of first term model."""

import scipy as sp
import matplotlib.pyplot as mpl
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

import first_term as ft
import experimental_data as expdata

real_cat = ft.One_Term_Catalyst()
real_cat.T_array = sp.array([350., 400., 450., 500., 550., 600.]) 
real_cat.Vdot = sp.array([300.]) * 1.e-6 / 60. 

data1 = expdata.Data()
data1.source = '300sccm 20nmPtPd VariedT.xls'
data1.Vdot_setpoint = 300.
data1.T = sp.array([350., 400., 450., 500., 550., 600.])
data1.HCin = sp.array([3830., 3880., 3860., 3800., 3840., 3850.])
data1.HCout = sp.array([3780., 3730., 3660., 3560., 3380., 1714.]) 
data1.set_eta_T()

def get_R(real_cat, data1):
    """Returns value for R for a particular A and T_a"""
    real_cat.set_eta_dimensional()
    R = sp.sum((real_cat.eta_ij[0,:] - data1.eta_T)**2)
    return R

