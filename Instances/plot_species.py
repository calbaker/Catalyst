"""Generates two contour plots for species concentration in two
dimensions, one for first term and one for multi term."""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

cmd_folder = os.path.dirname('../Modules/')
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import catalyst
reload(catalyst)

x_array = np.linspace(0., 61., 100)
# max should be 30 to be consistent with experiment
y_array = np.linspace(0, 1., 50)

Pe = 50.
Da = 0.1
# reasonable Pe and Da for experimental conditions are Pe = 20 to 50
# and Da = 0.01 to 0.15

catmax = catalyst.Catalyst()
catmax.terms = 4
catmax.x_array = x_array
catmax.y_array = y_array
catmax.Vdot = 500e-6 / 60.
catmax.T = 400. + 273.15
Pe = catmax.get_Pe()
Da = catmax.get_Da()
catmax.Yxy = np.zeros([x_array.size, y_array.size])

cathipe = catalyst.Catalyst()
cathipe.terms = 4
cathipe.x_array = x_array
cathipe.y_array = y_array
cathipe.Yxy = np.zeros([x_array.size, y_array.size])

cat1 = catalyst.Catalyst(terms=1)
cat1.x_array = x_array
cat1.y_array = y_array
cat1.Yxy = np.zeros([x_array.size, y_array.size])

cat_num = catalyst.Catalyst()
cat_num.Pe = Pe
cat_num.Da = Da
cat_num.x_array = x_array
cat_num.y_array = y_array
cat_num.solve_numeric()

cat_1dflow = catalyst.Catalyst()
cat_1dflow.Pe = Pe
cat_1dflow.Da = Da
cat_1dflow.x_array = x_array
cat_1dflow.y_array = y_array
cat_1dflow.init_numerical1dflow()
cat_1dflow.solve_numeric()

for i in range(x_array.size):
    x_ = x_array[i]
    for j in range(y_array.size):
        y_ = y_array[j]
        catmax.Yxy[i, j] = catmax.get_Y(x_, y_, Pe=Pe, Da=Da)
        cathipe.Yxy[i, j] = cathipe.get_Y(x_, y_, Pe=100., Da=Da)
        cat1.Yxy[i, j] = cat1.get_Y(x_, y_, Pe=Pe, Da=Da)

catmax.Yxy = (
    np.concatenate((catmax.Yxy[:, ::-1][:, 1:], catmax.Yxy), 1)
    )
cathipe.Yxy = (
    np.concatenate((cathipe.Yxy[:, ::-1][:, 1:], cathipe.Yxy), 1)
    )
cat1.Yxy = (
    np.concatenate((cat1.Yxy[:, ::-1][:, 1:], cat1.Yxy), 1)
    )
cat_num.Yxy_num = (
    np.concatenate((cat_num.Yxy_num[:, ::-1][:, 1:], cat_num.Yxy_num),
    1)
    )
cat_1dflow.Yxy_num = (
    np.concatenate((cat_1dflow.Yxy_num[:, ::-1][:, 1:], cat_1dflow.Yxy_num),
    1)
    )

y_array = np.concatenate((-y_array[1:][::-1], y_array), 0)

# Plot configuration
FONTSIZE = 30
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

TICKS = np.linspace(cat_1dflow.Yxy_num.min(), 1, 6)
LEVELS = np.linspace(cat_1dflow.Yxy_num.min(), cat_1dflow.Yxy_num.max(), 12)

plt.close()

x_2d, y_2d = np.meshgrid(x_array, y_array)

np.savetxt('../output/plot_species/x_2d', x_2d)
np.savetxt('../output/plot_species/y_2d', y_2d)
np.savetxt('../output/plot_species/cat_num.Yxy_num', cat_num.Yxy_num)
np.savetxt('../output/plot_species/cat_1dflow.Yxy_num', cat_1dflow.Yxy_num)
np.savetxt('../output/plot_species/catmax.Yxy', catmax.Yxy)
np.savetxt('../output/plot_species/cat1.Yxy', cat1.Yxy)
np.savetxt(
    '../output/plot_species/' + str(catmax.terms) + ' Yxy',
    catmax.Yxy
    )

fig_max = plt.figure(str(catmax.terms) + ' terms')
FCS = plt.contourf(x_2d, y_2d, catmax.Yxy.T, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', format='%.2f', ticks=TICKS)
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
plt.ylim(-1, 1)
#plt.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$')
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/plot_species/species4 Da=' + str(Da) + ' Pe=' + str(Pe)
            + '.pdf')
paper_dir = '/home/chad/Documents/Catalyst/Paper/version 2.1/Figures/'
plt.savefig(paper_dir + 'species_4term.pdf')

TICKShipe = np.linspace(cathipe.Yxy.min(), 1, 6)
LEVELShipe = np.linspace(cathipe.Yxy.min(), cathipe.Yxy.max(), 12)

fig_one = plt.figure('1 term')
FCS = plt.contourf(x_2d, y_2d, cat1.Yxy.T, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', format='%.2f', ticks=TICKS)
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
# plt.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$' +
#           '\nDa=' + str(cat1.Da) + ' Pe=' + str(cat1.Pe))
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/plot_species/species1 Da=' + str(Da) + ' Pe=' + str(Pe)
            + '.pdf')
plt.savefig(paper_dir + 'species_1term.pdf')

fig_num = plt.figure('numerical')
FCS = plt.contourf(x_2d, y_2d, cat_num.Yxy_num.T, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS, format='%.2f')
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/plot_species/species num Da=' + str(Da) + ' Pe=' + str(Pe)
            + '.pdf')
plt.savefig(paper_dir + 'species_num.pdf')

fig_1dflow = plt.figure('1d flow')
FCS = plt.contourf(x_2d, y_2d, cat_1dflow.Yxy_num.T, levels=LEVELS)
CB = plt.colorbar(FCS, orientation='vertical', ticks=TICKS, format='%.2f')
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/plot_species/species 1dflow Da=' + str(Da) + ' Pe=' + str(Pe)
            + '.pdf')
plt.savefig(paper_dir + 'species_1dflow.pdf')

FONTSIZE = 18
plt.rcParams['axes.labelsize'] = FONTSIZE
plt.rcParams['axes.titlesize'] = FONTSIZE
plt.rcParams['legend.fontsize'] = FONTSIZE
plt.rcParams['xtick.labelsize'] = FONTSIZE
plt.rcParams['ytick.labelsize'] = FONTSIZE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 10

fig_hipe = plt.figure(str(cathipe.terms) + ' terms, hi Pe')
FCS = plt.contourf(x_2d, y_2d, cathipe.Yxy.T, levels=LEVELShipe)
CB = plt.colorbar(FCS, orientation='vertical', format='%.2f', ticks=TICKShipe)
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
plt.ylim(-1, 1)
#plt.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$')
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)
plt.subplots_adjust(right=0.7)
plt.savefig('../Plots/plot_species/species4 Da=' + str(Da) + ' Pe=' + str(Pe)
            + ' hipe.pdf')

fig_max2 = plt.figure(str(catmax.terms) + ' terms alt')
FCS2 = plt.contourf(x_2d, y_2d, catmax.Yxy.T, levels=LEVELS)
CB2 = plt.colorbar(FCS2, orientation='vertical', format='%.2f', ticks=TICKS)
plt.grid()
plt.xlabel(r'$\tilde{x}$')
plt.ylabel(r'$\tilde{y}$')
plt.ylim(-1, 1)
#plt.title(r'Species Concentration v. $\tilde{x}$ and $\tilde{y}$')
plt.ylim(-1, 1)
plt.subplots_adjust(bottom=0.10)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.75)
plt.savefig('../Plots/plot_species/species4 Da=' + str(Da) + ' Pe=' + str(Pe)
            + 'alt.pdf')

plt.show()

