"""Module for plotting results of first term model."""

import scipy as sp
import matplotlib.pyplot as mpl
import os
os.chdir('/home/chad/Documents/UT Stuff/Research/Catalyst/Model')

from first_term import *
import experimental_data as expdata
reload(expdata)

mpl.close('all')

def get_S(real_cat, data1):
    real_cat.set_eta_dimensional()
    S = sp.sum((real_cat.eta_ij[0,:] - data1.eta_T)**2)
    return S

def set_dS(real_cat, data1, A_arr, T_a):
    real_cat.S = sp.zeros([sp.size(A_arr), sp.size(T_a)])
    real_cat.dSdA = sp.zeros([sp.size(A_arr)-1, sp.size(T_a)])
    real_cat.dSdT = sp.zeros([sp.size(A_arr), sp.size(T_a)-1])
    for i in sp.arange(sp.size(A_arr)):
        if i%10 == 0:
            print 'i =',i,'of',sp.size(real_cat.dSdA,0)
        for j in sp.arange(sp.size(T_a)):
            real_cat.A_arr = A_arr[i]
            real_cat.T_a = T_a[j]
            real_cat.S[i,j] = get_S(real_cat, data1)
    real_cat.dSdA = ( (real_cat.S[1:,:] - real_cat.S[:-1,:]) /
    (A_arr[1:] - A_arr[:-1]) ) 
    real_cat.dSdT = ( (real_cat.S[:,1:] - real_cat.S[:,:-1]) /
    (T_a[1:] - T_a[:-1]) )
     
real_cat = One_Term_Catalyst()
real_cat.T_array = sp.array([350., 400., 450., 500., 550., 600.]) 
real_cat.Vdot = sp.array([300.]) * 1.e-6 / 60. 

data1 = expdata.Data()
data1.source = '300sccm 20nmPtPd VariedT.xls'
data1.Vdot_setpoint = 300.
data1.T = sp.array([350., 400., 450., 500., 550., 600.])
data1.HCin = sp.array([3830., 3880., 3860., 3800., 3840., 3850.])
data1.HCout = sp.array([3780., 3730., 3660., 3560., 3380., 1714.]) 
data1.set_eta_T()

A_arr = sp.linspace(1., 1000., 50) * 1e9
T_a = sp.linspace(5, 15, 50) * 1e3
set_dS(real_cat, data1, A_arr, T_a)

# Plot configuration
FONTSIZE = 14
mpl.rcParams['axes.labelsize'] = FONTSIZE
mpl.rcParams['axes.titlesize'] = FONTSIZE
mpl.rcParams['legend.fontsize'] = FONTSIZE
mpl.rcParams['xtick.labelsize'] = FONTSIZE
mpl.rcParams['ytick.labelsize'] = FONTSIZE
mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 10

# converts back to sccm for plotting
# TICKS = sp.arange(0,1.5,0.1)
LEVELS = sp.arange(0., 1.05, 0.05)

A,T = sp.meshgrid(A_arr[1:], T_a[:])

fig = mpl.figure()
FCS = mpl.contourf(A, T, real_cat.dSdA.T)
CB = mpl.colorbar(FCS, orientation='horizontal', format='%.0f')
mpl.grid()
mpl.title(r'Normalized $\frac{dS}{dA}$')
mpl.xlabel('Preexponential (1/s)')
mpl.ylabel('Activation Temperature (K)')
mpl.savefig('Plots/calibrate A.pdf')
mpl.savefig('Plots/calibrate A.png')

A,T = sp.meshgrid(A_arr[:], T_a[1:])

fig2 = mpl.figure()
FCS2 = mpl.contourf(A, T, real_cat.dSdT.T)
CB = mpl.colorbar(FCS2, orientation='horizontal', format='%.0f')
mpl.grid()
mpl.title(r'Normalized $\frac{dS}{dT}$')
mpl.xlabel('Preexponential (1/s)')
mpl.ylabel('Activation Temperature (K)')
mpl.savefig('Plots/calibrate T.pdf')
mpl.savefig('Plots/calibrate T.png')

mpl.show()
