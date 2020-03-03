"""
Script plots vertical profile of zonal wind change over epochs

Notes
-----
    Author : Zachary Labe
    Date   : 3 March 2020
"""

### Import modules
import datetime
import numpy as np
import matplotlib.pyplot as plt
import cmocean
import calc_Utilities as UT
import scipy.stats as sts
import read_OBS as REAN

### Define directories
directoryfigure = '/home/zlabe/Desktop/AA/Reanalysis/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Plotting Reanalysis vertical U - %s----' % titletime)

### Add parameters
datareader = True
latpolar = 65.
epochq = 10
variable = 'U'
period = 'DJF' 
level = 'profile'
dataERA = 'ERAI_Present'

### Create images
if dataERA == 'ERAI_Present':
    datatitle = 'ERA-Interim'
else:
    datatitle = 'ERA5'

###############################################################################
###############################################################################
###############################################################################
### Read in data
if datareader == True:
    ###########################################################################
    ### Read in reanalysis data
    years = np.arange(1979,2017+1,1)
    late,lone,leve,vare = REAN.readOBS(dataERA,variable,level,period) 
    latr,lonr,levr,varr = REAN.readOBS('NCEP1',variable,level,period)
    
    varpole = np.nanmean(vare,axis=3)
    varpolr = np.nanmean(varr,axis=3)
    
###############################################################################
###############################################################################
###############################################################################
### Calculate reanalysis epochs
oldthicke = np.nanmean(varpole[:epochq],axis=0)   # 1979-1988
newthicke = np.nanmean(varpole[-epochq:],axis=0)  # 2008-2017
diffe = newthicke - oldthicke

oldthickr = np.nanmean(varpolr[:epochq],axis=0)   # 1979-1988
newthickr = np.nanmean(varpolr[-epochq:],axis=0)  # 2008-2017
diffr = newthickr - oldthickr

### Significance testing
prunse = UT.calc_FDR_ttest(varpole[:epochq],varpole[-epochq:],0.1)
prunsr = UT.calc_FDR_ttest(varpolr[:epochq],varpolr[-epochq:],0.1)

###############################################################################
###############################################################################
###############################################################################
### Calculate climatology
clime = np.nanmean(varpole,axis=0)
climr = np.nanmean(varpolr,axis=0)

############################################################################
############################################################################
############################################################################
#### Plot temperature profile
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

fig = plt.figure()
ax1 = plt.subplot(121)

### Set limits for contours and colorbars
limit = np.arange(-3,3.01,0.25)
limitclim = np.arange(-70,71,5)
barlim = np.arange(-3,4,1)
zscale = np.array([1000,700,500,300,200,
                    100,50,30,10])
timeqe,levqe = np.meshgrid(late,leve)

ax1.spines['top'].set_color('dimgrey')
ax1.spines['right'].set_color('dimgrey')
ax1.spines['bottom'].set_color('dimgrey')
ax1.spines['left'].set_color('dimgrey')
ax1.spines['left'].set_linewidth(2)
ax1.spines['bottom'].set_linewidth(2)
ax1.spines['right'].set_linewidth(2)
ax1.spines['top'].set_linewidth(2)
ax1.tick_params(axis='y',direction='out',which='major',pad=3,
                width=2,color='dimgrey')
ax1.tick_params(axis='x',direction='out',which='major',pad=3,
                width=2,color='dimgrey')    
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')

cs = plt.contourf(timeqe,levqe,diffe,limit,extend='both')
cs2 = plt.contourf(timeqe,levqe,prunse,colors='None',
               hatches=['//////'],linewidths=0.4)
cs3 = plt.contour(timeqe,levqe,clime,limitclim,linewidths=0.6,colors='dimgrey')

plt.ylabel(r'\textbf{Pressure [hPa]}',color='k',fontsize=9)
plt.xlabel(r'\textbf{Latitude [$\bf{^{\circ}}$N]}',color='k',fontsize=9)
plt.title(r'\textbf{%s}' % datatitle,color='k',fontsize=11)

plt.yscale('log',nonposy='clip')
plt.ylim([1000,10])
plt.xticks(np.arange(-90,91,15),map(str,np.arange(-90,91,15)),fontsize=6)
plt.yticks(zscale,map(str,zscale),ha='right',fontsize=6)
plt.xlim([-90,90])
plt.minorticks_off()
plt.gca().invert_yaxis()
           
cs.set_cmap(cmocean.cm.balance)

###############################################################################

ax1 = plt.subplot(122)

### Set limits for contours and colorbars
limit = np.arange(-3,3.01,0.25)
limitclim = np.arange(-70,71,5)
barlim = np.arange(-3,4,1)
zscale = np.array([1000,700,500,300,200,
                    100,50,30,10])
timeqr,levqr = np.meshgrid(latr,levr)

ax1.spines['top'].set_color('dimgrey')
ax1.spines['right'].set_color('dimgrey')
ax1.spines['bottom'].set_color('dimgrey')
ax1.spines['left'].set_color('dimgrey')
ax1.spines['left'].set_linewidth(2)
ax1.spines['bottom'].set_linewidth(2)
ax1.spines['right'].set_linewidth(2)
ax1.spines['top'].set_linewidth(2)
ax1.tick_params(axis='y',direction='out',which='major',pad=3,
                width=2,color='dimgrey')
ax1.tick_params(axis='x',direction='out',which='major',pad=3,
                width=2,color='dimgrey')    
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
plt.tick_params(axis='y',which='both',labelleft=False)

cs = plt.contourf(timeqr,levqr,diffr,limit,extend='both')
cs2 = plt.contourf(timeqr,levqr,prunsr,colors='None',
               hatches=['//////'],linewidths=0.4)
cs3 = plt.contour(timeqr,levqr,climr,limitclim,linewidths=0.6,colors='dimgrey')

plt.xlabel(r'\textbf{Latitude [$\bf{^{\circ}}$N]}',color='k',fontsize=9)
plt.title(r'\textbf{NCEP/NCAR Reanalysis I}',color='k',fontsize=11)

plt.yscale('log',nonposy='clip')
plt.ylim([1000,10])
plt.xticks(np.arange(-90,91,15),map(str,np.arange(-90,91,15)),fontsize=6)
plt.yticks(zscale,map(str,zscale),ha='right',fontsize=6)
plt.xlim([-90,90])
plt.minorticks_off()
plt.gca().invert_yaxis()
           
cs.set_cmap(cmocean.cm.balance)

plt.tight_layout()
cbar_ax = fig.add_axes([0.312,0.05,0.4,0.03])                
cbar = fig.colorbar(cs,cax=cbar_ax,orientation='horizontal',
                    extend='both',extendfrac=0.07,drawedges=False)
cbar.set_ticks(barlim)
cbar.set_ticklabels(list(map(str,barlim))) 
cbar.ax.tick_params(axis='x', size=.001,labelsize=6)
cbar.outline.set_edgecolor('dimgrey')
cbar.set_label(r'\textbf{[2017-2008]--[1988-1979] U m/s}',color='k',
                         fontsize=6,labelpad=-27)

plt.subplots_adjust(bottom=0.2)

plt.savefig(directoryfigure + 'VerticalU_Epoch_Reanalysis_%s.png' % datatitle,dpi=300)

############################################################################
############################################################################
############################################################################
##### Plot temperature profile
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

fig = plt.figure()
ax1 = plt.subplot(121)

### Set limits for contours and colorbars
limit = np.arange(-3,3.01,0.25)
limitclim = np.arange(-70,71,5)
barlim = np.arange(-3,4,1)
zscale = np.array([1000,925,850,700,500,300,200])
timeqe,levqe = np.meshgrid(late,leve)

ax1.spines['top'].set_color('dimgrey')
ax1.spines['right'].set_color('dimgrey')
ax1.spines['bottom'].set_color('dimgrey')
ax1.spines['left'].set_color('dimgrey')
ax1.spines['left'].set_linewidth(2)
ax1.spines['bottom'].set_linewidth(2)
ax1.spines['right'].set_linewidth(2)
ax1.spines['top'].set_linewidth(2)
ax1.tick_params(axis='y',direction='out',which='major',pad=3,
                width=2,color='dimgrey')
ax1.tick_params(axis='x',direction='out',which='major',pad=3,
                width=2,color='dimgrey')    
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')

cs = plt.contourf(timeqe,levqe,diffe,limit,extend='both')
cs2 = plt.contourf(timeqe,levqe,prunse,colors='None',
               hatches=['//////'],linewidths=0.4)
cs3 = plt.contour(timeqe,levqe,clime,limitclim,linewidths=0.6,colors='dimgrey')

plt.ylabel(r'\textbf{Pressure [hPa]}',color='k',fontsize=9)
plt.xlabel(r'\textbf{Latitude [$\bf{^{\circ}}$N]}',color='k',fontsize=9)
plt.title(r'\textbf{%s}' % datatitle,color='k',fontsize=11)

plt.yscale('log',nonposy='clip')
plt.ylim([1000,200])
plt.xticks(np.arange(-90,91,15),map(str,np.arange(-90,91,15)),fontsize=6)
plt.yticks(zscale,map(str,zscale),ha='right',fontsize=6)
plt.xlim([45,90])
plt.minorticks_off()
plt.gca().invert_yaxis()
           
cs.set_cmap(cmocean.cm.balance)

###############################################################################

ax1 = plt.subplot(122)

### Set limits for contours and colorbars
limit = np.arange(-3,3.01,0.25)
limitclim = np.arange(-70,71,5)
barlim = np.arange(-3,4,1)
zscale = np.array([1000,925,850,700,500,300,200])
timeqr,levqr = np.meshgrid(latr,levr)

ax1.spines['top'].set_color('dimgrey')
ax1.spines['right'].set_color('dimgrey')
ax1.spines['bottom'].set_color('dimgrey')
ax1.spines['left'].set_color('dimgrey')
ax1.spines['left'].set_linewidth(2)
ax1.spines['bottom'].set_linewidth(2)
ax1.spines['right'].set_linewidth(2)
ax1.spines['top'].set_linewidth(2)
ax1.tick_params(axis='y',direction='out',which='major',pad=3,
                width=2,color='dimgrey')
ax1.tick_params(axis='x',direction='out',which='major',pad=3,
                width=2,color='dimgrey')    
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
plt.tick_params(axis='y',which='both',labelleft=False)

cs = plt.contourf(timeqr,levqr,diffr,limit,extend='both')
cs2 = plt.contourf(timeqr,levqr,prunsr,colors='None',
               hatches=['//////'],linewidths=0.4)
cs3 = plt.contour(timeqr,levqr,climr,limitclim,linewidths=0.6,colors='dimgrey')

plt.xlabel(r'\textbf{Latitude [$\bf{^{\circ}}$N]}',color='k',fontsize=9)
plt.title(r'\textbf{NCEP/NCAR Reanalysis I}',color='k',fontsize=11)

plt.yscale('log',nonposy='clip')
plt.ylim([1000,200])
plt.xticks(np.arange(-90,91,15),map(str,np.arange(-90,91,15)),fontsize=6)
plt.yticks(zscale,map(str,zscale),ha='right',fontsize=6)
plt.xlim([45,90])
plt.minorticks_off()
plt.gca().invert_yaxis()
           
cs.set_cmap(cmocean.cm.balance)

plt.tight_layout()
cbar_ax = fig.add_axes([0.312,0.05,0.4,0.03])                
cbar = fig.colorbar(cs,cax=cbar_ax,orientation='horizontal',
                    extend='both',extendfrac=0.07,drawedges=False)
cbar.set_ticks(barlim)
cbar.set_ticklabels(list(map(str,barlim))) 
cbar.ax.tick_params(axis='x', size=.001,labelsize=6)
cbar.outline.set_edgecolor('dimgrey')
cbar.set_label(r'\textbf{[2017-2008]--[1988-1979] U m/s}',color='k',
                         fontsize=6,labelpad=-27)

plt.subplots_adjust(bottom=0.2)

plt.savefig(directoryfigure + 'VerticalU_Troposphere_Epoch_Reanalysis_%s.png' % datatitle,dpi=300)