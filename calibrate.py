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

max_iter = 50
A_arr = sp.zeros(max_iter)
T_a = sp.zeros(max_iter)
dRdA_arr = sp.zeros(max_iter - 1)
dRdT_a = sp.zeros(max_iter - 1)
d2RdA_arr2 = sp.zeros(max_iter - 2)
d2RdT_a2 = sp.zeros(max_iter - 2)
R = sp.zeros(max_iter * 2)               

# The idea here is to find the 2nd derivative by perturbing the
# solution for R with 2 changes in A_arr or T_a, and then change the
# values until the desired 1st derivative is achieved.  To do this
# properly, only 1 of the two independent variables can be changed at
# a time.  


i = 3
j = 0
k = 0
criteria = 0.001

print "\ndRdA_arr =", dRdA_arr
print "dRdT_a =", dRdT_a

# Steps to solve for both partials of R = 0.  1. Guess three values of
# A_arr and calculate first and second derivatives.  2. Use 2nd
# derivative to guess correct value of A_arr to put 1st derivative
# equal to zero.  3. Guess three values of T_a and repeat.  

A_arr[0:3] = sp.array([30., 40., 50.]) * 1.e10
T_a[0:3] = sp.array([15., 16., 17.]) * 1.e3
R[0:3] = sp.array([1, 2, 4])

#while sp.absolute(R[i] - R[i-3]) > 0.01:
for p in sp.arange(10):
    print "outer while", i
    for j in sp.arange(j, j+3):
        real_cat.A_arr = A_arr[j]
        R[i] = get_R(real_cat, data1)
    dRdA_arr[0:2] = (R[1:3] - R[0:2]) / (A_arr[1:3] - A_arr[0:2])
    d2RdA_arr2[0:1] = ( (dRdA_arr[1:2] - dRdA_arr[0:1]) /
                        (A_arr[1:2] - A_arr[0:1]) )
    # while ( sp.absolute(dRdA_arr[j-1] - dRdA_arr[j-2]) / dRdA_arr[j-2]
    # > criteria ):
    for pafealk in sp.arange(10):
        print "while1", j
        A_arr[j+1] = -dRdA_arr[j-1] / d2RdA_arr2[j-2]
        real_cat.A_arr = A_arr[j+1]
        R[i] = get_R(real_cat, data1)
        dRdA_arr[j] = (R[i] - R[i-1]) / (A_arr[j+1] - A_arr[j])
        d2RdA_arr2[j-1] = ( (dRdA_arr[j+1] - dRdA_arr[j]) /
                            (A_arr[j+1] - A_arr[j]) )
        j = j + 1
        i = i + 1
        
    for i in sp.arange(k, k+3):
        real_cat.T_a = T_a[i-3]
        R[i] = get_R(real_cat, data1)
    dRdT_a[0:2] = (R[4:6] - R[3:5]) / (T_a[1:3] - T_a[0:2])
    d2RdT_a2[0:1] = ( (dRdT_a[1:2] - dRdT_a[0:1]) /
                      (T_a[1:2] - T_a[0:1]) ) 

    # while ( sp.absolute(dRdT_a[k-1] - dRdT_a[k-2]) / dRdT_a[k-2] >
    #     criteria ):
    for faeafe in sp.arange(10):
        print "while2", k
        T_a[k+1] = -dRdT_a[k-1] / d2RdA_arr2[j-2]
        real_cat.A_arr = T_a[k+1]
        R[i] = get_R(real_cat, data1)
        dRdT_a[k] = (R[i] - R[i-1]) / (T_a[k+1] - T_a[k])
        d2RdA_arr2[j-1] = ( (dRdT_a[k+1] - dRdT_a[k]) /
                        (T_a[k+1] - T_a[k]) )
        k = k + 1
        i = i + 1

    
