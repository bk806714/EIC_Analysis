import matplotlib.pyplot as plt
import awkward as ak
import uproot as ur
import sys,os
import numpy as np
import math
from scipy.optimize import curve_fit
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
global ene
from matplotlib.legend_handler import HandlerLine2D
#from scipy.stats import norm
import matplotlib.lines as mlines
import matplotlib.colors as mcolors

Gev_To_MeV=1000
working_dir=os.getcwd()
new_dir="Plots"#'/home/bishnu/UCR_EIC/Plots/hepmc/'
try:
    os.makedirs(f"{working_dir}/{new_dir}",exist_ok=True)
except OSError:
    print("Directory creation Error "%new_dir)
else:
    print("Directory %s is created"%new_dir)
PathToPlot="./"+ new_dir  #Replace with your own variation! 
FIT_SIGMA=3
xrange=350
### FUNCTION FOR PLOTTING THE XY Distribution



def XY_plot2D(X,Y,energy_plot, particle):
    print(energy_plot)
    PosRecoX=X
    PosRecoY=Y
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    #hb=ax.hexbin(ak.flatten(PosRecoX),ak.flatten(PosRecoY),gridsize=50, cmap='viridis')
    #hb=ax.hexbin(ak.flatten(PosRecoX),ak.flatten(PosRecoY),gridsize=100, extent=(-xrange,xrange,-xrange,xrange))
    hb=ax.hexbin(PosRecoX,PosRecoY,gridsize=100, extent=(-xrange,xrange,-xrange,xrange))

    cb = fig.colorbar(hb, label='hits')
    if particle=='pi-':
        greek_particle='$\pi^{-}$'
    elif particle=='e-':
        greek_particle='$e^-$'
    else: print("You forgot to pick the particle")
    title='{0} GeV {1}'.format(energy_plot,greek_particle)
    plt.xlabel('position x [cm]')
   # plt.xlim(-50,30)
    plt.title(title)

    plt.ylabel('Position y [cm]')
    FigName='XY_distribution_{0}GeV_{1}.png'.format(energy_plot,particle)
    
    plt.savefig(f"{PathToPlot}{FigName}")
    plt.show()
    


def plot2D_energy_time(time,ene,energy_plot, particle,MIP):
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    #hb=ax.hexbin(ak.flatten(PosRecoX),ak.flatten(PosRecoY),gridsize=50, cmap='viridis')
    eneMIP=ene/MIP
    hb=ax.hexbin(ak.flatten(eneMIP),ak.flatten(time),gridsize=100, extent=(0,5,0,200))

    cb = fig.colorbar(hb, label='count')
    if particle=='pi-':
        greek_particle='$\pi^{-}$'
    elif particle=='e-':
        greek_particle='$e^-$'
    else: print("You forgot to pick the particle")
    title='{0} GeV {1}'.format(energy_plot,greek_particle)
    plt.xlabel('Energy [MeV]')
    #plt.xlim(-50,30)
    plt.title(title)

    plt.ylabel('Time [ns]')
    FigName='time_Energy_dist_{0}GeV_{1}.png'.format(energy_plot,particle)
    plt.savefig(f"{PathToPlot}{FigName}")
    plt.show()

def hcal_hcali_plot2D_energy(X,Y,energy_plot, particle):
    print(energy_plot)
    xrange=100
    PosRecoX=X
    PosRecoY=Y
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    #hb=ax.hexbin(ak.flatten(PosRecoX),ak.flatten(PosRecoY),gridsize=50, cmap='viridis')
    
    hb=ax.hexbin(PosRecoX,PosRecoY,gridsize=25, extent=(0,xrange,0,xrange))


    cb = fig.colorbar(hb, label='counts')
    if particle=='pi-':
        greek_particle='$\pi^{-}$'
    elif particle=='e-':
        greek_particle='$e^-$'
    else: print("You forgot to pick the particle")
    title='{0} GeV {1}'.format(energy_plot,greek_particle)
    plt.xlabel('HCali Energy (GeV)')
    #plt.xlim(-50,30)
    plt.title(title)

    plt.ylabel('HCal energy')
    FigName='Energy distribution_{0}GeV_{1}.png'.format(energy_plot,particle)
    print('before show')
    plt.savefig(f"{PathToPlot}{FigName}")
    plt.show()
    
def XY_plot2D_energy(X,Y,ene,energy_plot, particle):
    print(energy_plot)
    PosRecoX=X
    PosRecoY=Y
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    #hb=ax.hexbin(ak.flatten(PosRecoX),ak.flatten(PosRecoY),gridsize=50, cmap='viridis')
    #hb=ax.hexbin(ak.flatten(PosRecoX),ak.flatten(PosRecoY),C=ak.flatten(ene),gridsize=50, extent=(-xrange,xrange,-xrange,xrange))
    hb=ax.hexbin(PosRecoX,PosRecoY,C=ene,gridsize=50, extent=(-xrange,xrange,-xrange,xrange))

    cb = fig.colorbar(hb, label='energy')
    if particle=='pi-':
        greek_particle='$\pi^{-}$'
    elif particle=='e-':
        greek_particle='$e^-$'
    else: print("You forgot to pick the particle")
    title='{0} GeV {1}'.format(energy_plot,greek_particle)
    plt.xlabel('position x [cm]')
    #plt.xlim(-50,30)
    plt.title(title)

    plt.ylabel('Position y [cm]')
    FigName='XY_distribution_{0}GeV_{1}.png'.format(energy_plot,particle)
    print('before show')
    plt.savefig(f"{PathToPlot}{FigName}")
    plt.show()


## FUNCTION FOR PLOTTING ONE DIMENSION HISTOGRAM OF GIVEN VARIABLE
def distribution_1D(variable,title,energy_plot,particle):
        
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    #print(len(ene))
    if title=='Energy':
        MinRange=0.0
        MaxRange=5.0
        x_title='Energy (MeV)'
    elif title=='z_pos':
        MinRange=0.0
        MaxRange=150.0
        x_title='Z position (cm)'
    elif title =='y_pos':
        MinRange=0.0
        MaxRange=50.0
        x_title='Y position (cm)'
    elif title =='x_pos':
        MinRange=0.0
        MaxRange=50.0
        x_title='X position (cm)'

    elif title =='time':
        MinRange=0
        MaxRange=300
        x_title='time (ns)'
    else: print('PLEASE GIVE RIGHT TITLE')
    ax.hist(ak.flatten(variable),bins=100, range=(MinRange,MaxRange),color='r', linewidth='3', histtype='step')
    #ax.hist(energy,bins=100, range=(MinRange,MaxRange),color='b',histtype='step',linewidth='3')#
    if particle=='pi-':
        greek_particle='$\pi^{-}$'
    elif particle=='e-':
        greek_particle='$e^-$'

    elif particle=='mu-':
        greek_particle='$\mu^-$'
    title_plot='{0} GeV {1}'.format(energy_plot,greek_particle)
    
    ax.set_title(title_plot)
    ax.set_yscale('log')
    #ax.set_xscale('log')
    ax.set_xlabel(x_title)
    ax.set_ylabel('Hits')
    print(title)
    FigName='OneD_{0}_{1}GeV_{2}.png'.format(title,energy_plot,particle)
    plt.savefig(f"{PathToPlot}{FigName}")
    #ax.legend(['without cut', 'E>0.06 MeV & time<200 ns'],fontsize='25')
    #
    plt.show() 
    

## Particle ID
def ID_Plot(id,particle):
    fig,ax = plt.subplots(1,1, figsize=(8, 6),sharex=True,sharey=True)
    ax.hist(ak.flatten(id),color='r',linewidth='3', bins=51,range=(0,50))
    if particle=='Pion':
        greek_particle='$\pi^{-}$'
    elif particle=='electron':
        greek_particle='$e^-$'
    ax.set_title('MCParticles.PDG ({0})'.format(greek_particle))
    ax.set_xlabel('Particle ID')
    ax.set_yscale('log')
                 
    plt.show()


### DEFINATION OF GAUSSIAN AND LINEAR FUNCTION FOR FITTING    
#def gaussian(x, amp, mean, sigma):
#    return amp * np.exp( -(x - mean)**2 / (2*sigma**2) )

def gaussian(x, amp, mean, sigma):
    return amp * np.exp( -0.5*((x - mean)/sigma)**2) /sigma

def linear_fit(xl,slope,intercept):
    return (slope*xl)+intercept



## FUNCTION TO FIT THE ENERGY DISTRIBUION WITH GAUSSIAN AND DETERMINE THE MEAN,SIGMA
## FITTING RANGE WITHIN +-3 SIGMA AND FOR LEAKAGE EVENTS BELOW 3SIGMA ARE COUNTED
def get_resolution(good_energy,energy_plot, particle,Sigma_For_leakage,wt):
    if wt=='on':
        print("I am wt")
        sampling_fraction_hcali=0.0098*1000 #(GeV-1) old val 0.0092
        sampling_fraction_hcal=0.022*1000  #(GeV-1) old val 0.0215
        max_range=150
        xtitle='Energy (GeV)'
        ytitle='Count'
        nbins=75
        steps=20
    else:
        sampling_fraction_hcali=1 #(GeV-1)
        sampling_fraction_hcal=1  #(GeV-1)
        max_range=2500
        xtitle='Energy (GeV)'
        ytitle='Count'
        nbins=250
        steps=200

    
    ## Differenciate between energy or theta/etas on y axis
    greek_particle=get_greek_particle(particle)
    if energy_plot<5:
        eta=get_eta(energy_plot)
        title_head=r'$\eta*$={0:.2f}'.format(eta)
       
    elif energy_plot>5:    
         eta=energy_plot
         title_head='{0}, Energy = {1} GeV'.format(greek_particle,eta)
    else:
        print('IF ENERGY IS LESS THAN 5 GeV THAN MAKE SURE THIS TO CHANGE')
    #print('xxxxxxxxxxxxxxxxxxxxxx',title_head)
    #fig = plt.figure( figsize=(6, 4))
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    ene_good=good_energy

    
    ene_total_temp = np.sum(ene_good,axis=-1)
    ene_total = np.divide(ene_total_temp,sampling_fraction_hcali)
    
    #ene_total=np.add(ene_total_hcal,ene_total_hinsert)
    
    
    #ene_total = ak.sum(ene_good,axis=-1)

    ene_average = ak.mean(ene_good,axis=-1)
    #ene_nhits = ak.num(ene_good)
    #HCAL_total=HCAL_total[0:90]

    mean_guess=np.mean(ene_total)
    sigma_guess=np.std(ene_total)
    
    
   
    count, bins,_= plt.hist(np.array(ene_total),bins=nbins,alpha=0.5,range=(0,max_range),label='HCAL',color='b',linewidth=8)#histtype='step'            
    binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])
    
    #plt.show()
    #return 1
    #print (count)
    
    ax.set_xlabel(xtitle)
    ax.set_ylabel("Entries")
    ## CHOOSE THE DATA POINTS WITHIN GIVEN SIGMAS FOR FITTING
    mask=(binscenters>(mean_guess-FIT_SIGMA*sigma_guess)) & (binscenters<(mean_guess+FIT_SIGMA*sigma_guess))
    error_counts=np.sqrt(count)
    error_counts=np.where(error_counts==0,1,error_counts)
    
    # PARAMETER BOUNDS ARE NOT USED FOR NOW
    param_bounds=([-np.inf,-np.inf,-np.inf], [np.inf,np.inf,np.inf])
    popt, pcov = curve_fit(gaussian,binscenters[mask],count[mask],p0=[np.max(count),mean_guess,sigma_guess],bounds=param_bounds)
        
    ax.plot(binscenters[mask], gaussian(binscenters[mask], *popt), color='red', linewidth=2.5, label=r'F')
    
    #ax.set_title("Energy = {0} GeV ".format(energy_plot))
    #ax.set_title(title_head)
    
    #ax.set_title("Energy = {0} GeV, $\eta$=3.7".format(energy_plot))
    ax.xaxis.set_major_locator(MultipleLocator(steps))
    ax.set_xlabel(xtitle)
    ax.set_ylabel("Entries")
    FigName='Fit_SimEnergy_{0}_{1}.png'.format(energy_plot,particle)

    ### GET MEAN SIGMA AND ERRORS FROM FIT
    mean=popt[1]
    std=popt[2]
    
  
    
    
    #errors=np.sqrt(np.diag(pcov))
    mean_error=np.sqrt(pcov[1, 1])
    std_error=np.sqrt(pcov[2, 2])
    #print(mean_guess,'   sigma   ', sigma_guess,' actual mean ', mean,  'actual std',std)  
    ### GET THE BIN WITH VALUE WHERE IT LIES mEAN -3SIGMA
    two_sig_threshold=mean-(Sigma_For_leakage*std)
    bin_2sig=np.digitize(two_sig_threshold,bins)
    
    ### GET FRACTION OF lEAKAGE
    num_leak=np.sum(count[0:bin_2sig])
    deno_leak=np.sum(count)
    leak_per=(num_leak/deno_leak)*100
    if leak_per==0:
        leak_per_error=0
    else:    
        leak_per_error=np.sqrt((np.sqrt(num_leak)/num_leak)**2 + (np.sqrt(deno_leak)/deno_leak)**2)*leak_per

    resolution=(std/mean)
    resolution_error=(np.sqrt((std_error/std)**2 + (mean_error/mean)**2))*resolution
        
    #mean=f'{mean:.2f}'
    mean=format(mean,'.2f')
    mean_error='{0:.3f}'.format(mean_error)
    
    std= '{0:.2f}'.format(std)
    std_error= '{0:.3f}'.format( std_error)

    leak_per= '{0:.3f}'.format(leak_per)
    leak_per_error='{0:.4f}'.format(leak_per_error)
    
    resolution = '{0:.2f}'.format(resolution)
    resolution_error ='{0:.4f}'.format(resolution_error)
    
    ####### PRINT THE VERTICLE LINE WITH 2 SIGMA ################    
    #ax.vlines([two_sig_threshold,  two_sig_threshold],0, np.max(count),linestyles='dashed', colors='m', linewidth=5)
   
    ratio_ene=float(mean)/float(energy_plot)
    ratio_ene='{0:.2f}'.format(ratio_ene)
    ratio_ene=float(ratio_ene)
    ax.text(80,250,"Resolution={0}" .format(resolution))
    ax.text(80,300,r'$\frac{Pred_{E}}{Truth_{E}}$ =' + '{0:.2f}'.format(ratio_ene))
    #ax.tick_params('both', length=20, width=2, which='major')
    #ax.tick_params('both', length=10, width=1, which='minor')
    plt.savefig(f"{PathToPlot}{FigName}")
    
    plt.show()
    return mean, std, mean_error, std_error, leak_per,leak_per_error,resolution,resolution_error
    


#### Plot for the Resolution, Mean Sigma and Lakage

def plot_resolution(energies,particle,means, stds, mean_errors, std_errors, resolutions, resolution_errors, leaks_per,leaks_per_error,Sigma_For_leakage):
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    resolutions=np.multiply(resolutions,100)
    print(resolutions)
    resolution_errors=np.multiply(resolution_errors,100)
    
    
    ax.errorbar(energies,resolutions, resolution_errors,color="red",marker='o',markersize=20,label='Reconstructed')
    #ax.plot(energies,resolutions, color="blue",marker='*',label="Generated")
    ax.set_xlabel('Energy (GeV)')
    ax.set_ylabel('$\sigma$/E ')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.set_ylim(0,30)

    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(5))   
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    #ax.set_title("Resolution vs Energy")
    FigName="Resolution_Energy_{0}.png".format(particle)
    plt.savefig(f"{PathToPlot}{FigName}")

    plt.show()
    #print(resolutions)
    #print(resolution_errors)
  

    ############ FOR MEAN ################
    if particle=='pi-':
        lowLimit=0
        upperLimit=101
    else:
        lowLimit=0
        upperLimit=101
        
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    ax.errorbar(energies,means, mean_errors, color="red",marker='o',linestyle='None',markersize=20,label='Reconstructed')
    energies=np.asarray(energies)
    means=np.asarray(means)
    mask=(energies>lowLimit) &(energies<upperLimit)
    poptLin,_popcovLin=curve_fit(linear_fit,energies[mask],means[mask],p0=[0,10],bounds=(0,101))
    slope=poptLin[0]
    intercept=poptLin[1]
   
    ax.plot(energies[mask],linear_fit(energies[mask],*poptLin),label='Fit',color='b',linewidth='4')
    print(type(energies),'slope    ',type(slope))
    ax.set_xlabel('Energy (GeV)')
    ax.set_ylabel('Mean from fit (MeV)')
    #ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.set_ylim(0,2000)
    #ax.set_xlim(0,70)

    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(200))   
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    #ax.set_title("Fitted Mean vs  Energy")


    chisqLin=np.sum(((means-linear_fit(energies,slope,intercept))/mean_errors)**2)
    plt.figtext(0.15,0.8,"m= {0:.2f} and c={1:.2f}".format(slope,intercept),fontweight='bold',fontsize=40)
    #residuals=means-linear_fit(energies,*poptLin)
    print(chisqLin)
    FigName="MeanE_Energy_{0}.png".format(particle)
    
    plt.savefig(f"{PathToPlot}{FigName}")

    plt.show()

    print(means,energies)

    ############ FOR SIGMA ################
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    ax.errorbar(energies,stds, std_errors, color="red",marker='o',markersize=20,label='Reconstructed')
    #ax.plot(energies,resolutions, color="blue",marker='*',label="Generated")
    ax.set_xlabel('Energy (GeV)')
    ax.set_ylabel('Sigma (GeV)')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    #ax.set_ylim(0,10)

    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(20))   
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    #ax.set_title("Fitted sigma vs Energy")
    FigName="Sigma_Energy_{0}.png".format(particle)
    plt.savefig(f"{PathToPlot}{FigName}")
    plt.show()
    
    
    ############### Leakage below 2 Sigma ############
    if particle=='pi-':
        ylimit_leakage=20;
    else:
        ylimit_leakage=5;
        
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    ax.errorbar(energies,leaks_per, leaks_per_error,color="red",marker='o',markersize=20,label='Reconstructed')
    #ax.plot(energies,resolutions, color="blue",marker='*',label="Generated")
    ax.set_ylabel('Leakage [%]')
    ax.set_xlabel('Energy (GeV) ')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
      
    ax.set_ylim(-0.25,ylimit_leakage)
   
    ax.xaxis.set_major_locator(MultipleLocator(10))
    #ax.yaxis.set_major_locator(MultipleLocator(5))   
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    #ax.set_title("Fraction of events below {0}$\sigma$".format(Sigma_For_leakage))
    FigName="Leakage_Energy_{0}.png".format(particle)
    plt.savefig(f"{PathToPlot}{FigName}")
    plt.show()

### This program read the HCAL INSERT WITH ANY EXTENSITON
## OR READS THE ORGINAL INSERT FILE WITH 16 MM TUNGSTEN THICKNESS
def read_rootfile(fraction,FilePathReco,ienergy,theta,particle,Time_Threshold,Energy_Threshold):
    FileName="insert_reco_{0}_{1}GeV_theta_{2}deg.edm4hep.root".format(particle,ienergy,theta)
    events=ur.open(f"{FilePathReco}{FileName}:events")
    
    total_Events=events.num_entries
    event_cut=total_Events/fraction
    print('HELLO JELLO', total_Events)
    #events_cut=
    events.keys()
    arrays = events.arrays(entry_start=0,entry_stop=event_cut)
    #ene = Gev_To_MeV*(ak.flatten(arrays['HcalEndcapPInsertHitsReco.energy'][:])) # in Mev
    ene = Gev_To_MeV*(arrays['HcalEndcapPInsertHitsReco.energy'][:]) # in Mev
    
    time = (arrays['HcalEndcapPInsertHitsReco.time'][:]) # in ns
    #time = (ak.flatten(arrays['HcalEndcapPInsertHitsReco.time'][:])) # in ns
    PosRecoX = (arrays['HcalEndcapPInsertHitsReco.position.x'])/10.0
    PosRecoY = (arrays['HcalEndcapPInsertHitsReco.position.y'])/10.0
    PosRecoZ= (arrays['HcalEndcapPInsertHitsReco.position.z'])/10.0

    
    cut_primary = arrays["MCParticles.generatorStatus"]==1
    px = arrays['MCParticles.momentum.x'][cut_primary]
    py = arrays['MCParticles.momentum.y'][cut_primary]
    pz = arrays['MCParticles.momentum.z'][cut_primary]
    mass = arrays["MCParticles.mass"][cut_primary]
    ID=arrays['MCParticles.PDG']#[cut_primary]
    
    #Calculate generated primary particle properties
    mom = np.sqrt(px**2+py**2+pz**2)
    energy_gen = np.sqrt(mom**2+mass**2)
    #fig = plt.figure( figsize=(8, 6))
    phi = np.arctan2(py,px)


    mask=(ene>Energy_Threshold)  & (time<Time_Threshold) & (ene<1e10)
    ene_good=ene[mask]
     
    return ene,time,PosRecoX,PosRecoY,PosRecoZ,mass,mom,energy_gen,phi,ene_good



#-----------------------------------------------------------------------------------


def read_rootfile_ECAL(fileindex,fraction,FilePathReco,ienergy,theta,particle,Time_Threshold,Energy_Threshold):
    #FileName="insert_reco_{0}_{1}GeV_theta_{2}deg.edm4hep.root".format(particle,ienergy,theta)
    FileName="insert_reco_{0}_{1}GeV_theta_{2}{3}.edm4hep.root".format(particle,ienergy,theta,fileindex)
    events=ur.open(f"{FilePathReco}{FileName}:events")
    total_Events=events.num_entries
    event_cut=total_Events/fraction
    print('HELLO JELLO', total_Events)
    #events_cut=
    events.keys()
    arrays = events.arrays(entry_start=0,entry_stop=event_cut)
    #ene = Gev_To_MeV*(ak.flatten(arrays['EcalEndcapPHitsReco.energy'][:])) # in Mev
    ene = (arrays['EcalEndcapPHitsReco.energy'][:]) # in Mev
    
    time = (arrays['EcalEndcapPHitsReco.time'][:]) # in ns
    #time = (ak.flatten(arrays['EcalEndcapPHitsReco.time'][:])) # in ns
    PosRecoX = (arrays['EcalEndcapPHitsReco.position.x'])/10.0
    PosRecoY = (arrays['EcalEndcapPHitsReco.position.y'])/10.0
    PosRecoZ= (arrays['EcalEndcapPHitsReco.position.z'])/10.0
    
    
    cut_primary = arrays["MCParticles.generatorStatus"]==1
    px = arrays['MCParticles.momentum.x'][cut_primary]
    py = arrays['MCParticles.momentum.y'][cut_primary]
    pz = arrays['MCParticles.momentum.z'][cut_primary]
    mass = arrays["MCParticles.mass"][cut_primary]
    ID=arrays['MCParticles.PDG']#[cut_primary]
    
    #Calculate generated primary particle properties
    mom = np.sqrt(px**2+py**2+pz**2)
    energy_gen = np.sqrt(mom**2+mass**2)
    #fig = plt.figure( figsize=(8, 6))
    phi = np.arctan2(py,px)


    mask=(ene>Energy_Threshold)  & (time<Time_Threshold) & (ene<1e10)
    ene_good=ene[mask]
    
    return ene,time,PosRecoX,PosRecoY,PosRecoZ,mass,mom,energy_gen,phi,ene_good

### READS ECAL_INSERT WITH MIXTURE OF TUNGSTEN AND STEEL
def read_rootfile_ECAL_Insert(fileindex,fraction,FilePathReco,ienergy,theta,particle,Time_Threshold,Energy_Threshold):
    FileName="insert_reco_{0}_{1}GeV_theta_{2}{3}.edm4hep.root".format(particle,ienergy,theta,fileindex)
    events=ur.open(f"{FilePathReco}{FileName}:events")
    total_Events=events.num_entries
    event_cut=total_Events/fraction
    print('HELLO JELLO', total_Events)
    #events_cut=
    events.keys()
    arrays = events.arrays(entry_start=0,entry_stop=event_cut)
    ene = (arrays['EcalEndcapPInsertHitsReco.energy'][:]) # in Mev
    
    time = (arrays['EcalEndcapPInsertHitsReco.time'][:]) # in ns
    #time = (ak.flatten(arrays['EcalEndcapPInsertHitsReco.time'][:])) # in ns
    PosRecoX = (arrays['EcalEndcapPInsertHitsReco.position.x'])/10.0
    PosRecoY = (arrays['EcalEndcapPInsertHitsReco.position.y'])/10.0
    PosRecoZ= (arrays['EcalEndcapPInsertHitsReco.position.z'])/10.0

    
    cut_primary = arrays["MCParticles.generatorStatus"]==1
    px = arrays['MCParticles.momentum.x'][cut_primary]
    py = arrays['MCParticles.momentum.y'][cut_primary]
    pz = arrays['MCParticles.momentum.z'][cut_primary]
    mass = arrays["MCParticles.mass"][cut_primary]
    ID=arrays['MCParticles.PDG']#[cut_primary]
    
    #Calculate generated primary particle properties
    mom = np.sqrt(px**2+py**2+pz**2)
    energy_gen = np.sqrt(mom**2+mass**2)
    #fig = plt.figure( figsize=(8, 6))
    phi = np.arctan2(py,px)


    mask=(ene>Energy_Threshold)  & (time<Time_Threshold) & (ene<1e10)
    ene_good=ene[mask]
     
    return ene,time,PosRecoX,PosRecoY,PosRecoZ,mass,mom,energy_gen,phi,ene_good


##-----------------------------------------------------------------------------------







def res_comp_hole_nohole(energies,condition,el_resolutions,el_resolutions_errors, el_resolutions_NH,el_resolutions_errors_NH):

    if (condition=='el_pion_withhole') or (condition=='el_pion_wout_hole') :
        label1='$e^-$'
        label2='$\pi^-$'
    else:
        label1= 'with hole'
        label2='without hole'
        
    el_resolutions=np.multiply(el_resolutions,100)
    el_resolutions_errors=np.multiply(el_resolutions_errors,100)

    el_resolutions_NH=np.multiply(el_resolutions_NH,100)
    el_resolutions_errors_NH=np.multiply(el_resolutions_errors_NH,100)
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    #ax.errorbar(energies,pi_resolutions, pi_resolutions_errors ,color="red",marker='o',markersize=20,label='$\pi^-$')
    ax.errorbar(energies,el_resolutions_NH, el_resolutions_errors_NH ,color="red",marker='o',markersize=20,label=label2)
    ax.errorbar(energies,el_resolutions, el_resolutions_errors,color="blue",marker='o',markersize=20,label=label1)
    ax.set_ylabel('$\sigma$/E (%)')
    ax.set_xlabel('Energy (GeV) ')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.set_ylim(0,30)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    #ax.yaxis.set_major_locator(MultipleLocator(2))   
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    #ax.set_title("Resolution")
    FigName="Res_comp_{0}_Energy.png".format(condition)
    plt.legend()
    plt.savefig(f"{PathToPlot}{FigName}")
    plt.show()
   

def Leakage_comp(energies,condition,pi_leaks_per,pi_leaks_per_error,el_leaks_per,el_leaks_per_error):
    
    if (condition=='el_pion_withhole') or (condition=='el_pion_wout_hole') :
        label1='$e^-$'
        label2='$\pi^-$'
    else:
        label1= 'with hole'
        label2='without hole'
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    ax.errorbar(energies,pi_leaks_per, pi_leaks_per_error ,color="red",marker='o',markersize=20,label=label2)
    ax.errorbar(energies,el_leaks_per, el_leaks_per_error,color="blue",marker='o',markersize=20,label=label1)

    ax.set_ylabel('Leakage (%)')
    ax.set_xlabel('Energy (GeV) ')
    #ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.set_ylim(-0.25,16)

    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(2))   
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    #ax.set_title("Resolution")
    FigName="Leakage_comp_{0}_Energy.png".format(condition)
    plt.legend()
    plt.savefig(f"{PathToPlot}{FigName}")
    plt.show()
    
def print_decimal_pi(type,pi_means, pi_means_error, pi_stds,pi_stds_error,pi_leaks_per, pi_leaks_per_error,pi_resolutions,pi_resolution_errors):
    print('pi_means_{0}=['.format(type),end="")
    print(*pi_means,sep=',',end =" ")
    print( ']')
    
    print('pi_means_error_{0}=['.format(type),end="")
    print(*pi_means_error,sep=',',end =" ")
    print( ']')
    
    print('pi_stds_{0}=['.format(type),end =" ")
    print(*pi_stds,sep=',',end =" ")
    print( ']')
    
    print('pi_stds_error_{0}=['.format(type),end =" ")
    print(*pi_stds_error,sep=',',end =" ")
    print( ']')
    print('pi_leaks_per_{0}=['.format(type),end =" ")
    print(*pi_leaks_per,sep=',',end =" ")
    print( ']')
    
    print('pi_leaks_per_error_{0}=['.format(type),end =" ")
    print(*pi_leaks_per_error,sep=',',end =" ")
    print( ']')
    print('pi_resolutions_{0}=['.format(type),end =" ")
    print(*pi_resolutions,sep=',',end =" ")
    print( ']')
    print('pi_resolutions_errors_{0}=['.format(type),end =" ")
    print(*pi_resolution_errors,sep=',',end =" ") 
    print( ']')
    
    
def print_decimal_el(type,el_means, el_means_error, el_stds,el_stds_error,el_leaks_per, el_leaks_per_error,el_resolutions,el_resolution_errors):
    print('el_means_{0}=['.format(type),end="")
    print(*el_means,sep=',',end =" ")
    print( ']')
    
    print('el_means_error_{0}=['.format(type),end =" ")
    print(*el_means_error,sep=',',end =" ")
    print( ']')

    print('el_stds_{0}=['.format(type),end =" ")
    print(*el_stds,sep=',',end =" ")
    print( ']')

    print('el_stds_error_{0}=['.format(type),end =" ")
    print(*el_stds_error,sep=',',end =" ")
    print( ']')
    
    print('el_leaks_per_{0}=['.format(type),end =" ")
    print(*el_leaks_per,sep=',',end =" ")
    print( ']')
    
    print('el_leaks_per_error_{0}=['.format(type),end =" ")
    print(*el_leaks_per_error,sep=',',end =" ")
    print( ']')
    
    print('el_resolutions_{0}=['.format(type),end =" ")
    print(*el_resolutions,sep=',',end =" ")
    print( ']')
    
    print('el_resolutions_errors_{0}=['.format(type),end =" ") 
    print(*el_resolution_errors,sep=',',end =" ") 
    print( ']')


   
def Final_resolution_CALICE_W():
    
    pi_meansCAL_T=[197.80,401.81,599.18,1013.66,1221.68,1620.62,2025.23 ]
    pi_means_errorCAL_T=[0.851,1.887,1.451,2.335,3.250,3.645,5.167 ]
    pi_stdsCAL_T=[ 32.59,47.89,52.68,76.05,90.00,105.08,153.38 ]
    pi_stds_errorCAL_T=[ 0.851,1.887,1.451,2.335,3.250,3.645,5.167 ]
    pi_leaks_perCAL_T=[ 3.153,4.204,7.357,11.261,10.360,13.063,10.811 ]
    pi_leaks_per_errorCAL_T=[ 0.6988,0.8110,1.0890,1.3716,1.3103,1.4892,1.3412 ]
    pi_resolutionsCAL_T=[ 0.16479,0.11920,0.08792,0.07502,0.07367,0.06484,0.07573 ]
    pi_resolutions_errorsCAL_T=[ 0.0044,0.0047,0.0024,0.0023,0.0027,0.0023,0.0026 ]

    el_meansCAL_T=[206.04,413.35,625.44,825.73,1002.25 ]
    el_means_errorCAL_T=[ 1.514,0.650,1.090,2.888,2.253 ]
    el_stdsCAL_T=[ 19.02,24.22,29.76,35.23,49.65 ]
    el_stds_errorCAL_T=[ 1.521,0.651,1.091,2.893,2.261 ]
    el_leaks_perCAL_T=[ 0.000,0.200,0.000,0.600,0.000 ]
    el_leaks_per_errorCAL_T=[ 0.0000,0.2002,0.0000,0.3474,0.0000 ]
    el_resolutionsCAL_T=[ 0.09230,0.05861,0.04758,0.04267,0.04954 ]
    el_resolutions_errorsCAL_T=[ 0.0074,0.0016,0.0017,0.0035,0.0023 ]

    
def plot_eh_ratio(energies,mean_eg,mean_pi_eg):
    energies=np.asarray(energies)
    mean_e=np.asarray(mean_eg)
    mean_pi=np.asarray(mean_pi_eg)
    #print(energies, mean_e,mean_pi)
    
    mask=(energies<60)
    
    mean_pi=mean_pi[mask]
    mean_e=mean_e[mask]
    ratio_eh=np.divide(mean_e,mean_pi)
    print(ratio_eh)
    ax.plot(energies[mask],ratio_eh[mask], color="red",marker='o',linestyle='None',markersize=20,label='$\pi^-$')
    ax.set_xlim(0,60)
    ax.set_ylabel('e/h')
    ax.set_xlabel('Energy (GeV) ')
    plt.show()
    



def read_rootfile_HCAL(fileindex,fraction,FilePathReco,ienergy,theta,particle,Time_Threshold,Energy_Threshold):
    #FileName="insert_reco_{0}_{1}GeV_theta_{2}deg.edm4hep.root".format(particle,ienergy,theta)
    FileName="insert_reco_{0}_{1}GeV_theta_{2}{3}.edm4hep.root".format(particle,ienergy,theta,fileindex)
    events=ur.open(f"{FilePathReco}{FileName}:events")
    total_Events=events.num_entries
    event_cut=total_Events/fraction
    print('HELLO JELLO', total_Events)
    #events_cut=
    events.keys()
    arrays = events.arrays(entry_start=0,entry_stop=event_cut)
    #ene = Gev_To_MeV*(ak.flatten(arrays['HcalEndcapPHitsReco.energy'][:])) # in Mev
    ene = Gev_To_MeV*(arrays['HcalEndcapPHitsReco.energy'][:]) # in Mev
    
    time = (arrays['HcalEndcapPHitsReco.time'][:]) # in ns
    #time = (ak.flatten(arrays['HcalEndcapPHitsReco.time'][:])) # in ns
    PosRecoX = (arrays['HcalEndcapPHitsReco.position.x'])/10.0
    PosRecoY = (arrays['HcalEndcapPHitsReco.position.y'])/10.0
    PosRecoZ= (arrays['HcalEndcapPHitsReco.position.z'])/10.0
    
    
    cut_primary = arrays["MCParticles.generatorStatus"]==1
    px = arrays['MCParticles.momentum.x'][cut_primary]
    py = arrays['MCParticles.momentum.y'][cut_primary]
    pz = arrays['MCParticles.momentum.z'][cut_primary]
    mass = arrays["MCParticles.mass"][cut_primary]
    ID=arrays['MCParticles.PDG']#[cut_primary]
    
    #Calculate generated primary particle properties
    mom = np.sqrt(px**2+py**2+pz**2)
    energy_gen = np.sqrt(mom**2+mass**2)
    #fig = plt.figure( figsize=(8, 6))
    phi = np.arctan2(py,px)


    mask=(ene>Energy_Threshold)  & (time<Time_Threshold) & (ene<1e10)
    ene_good=ene[mask]
    
    return ene,time,PosRecoX,PosRecoY,PosRecoZ,mass,mom,energy_gen,phi,ene_good





def get_resolution_hcalall(good_energy_hcal,good_energy_hinsert,energy_plot, itheta,particle,Sigma_For_leakage,wt):
    if wt=='on':
        sampling_fraction_hcal=0.022*1000
        sampling_fraction_hcali=0.0098*1000
        max_range=150
        nbins=75
        steps=20
        
    else:
        sampling_fraction_hcal=1
        sampling_fraction_hcali=1
        nbins=150
        max_range=1500
        steps=200
        
    if energy_plot<5:
        eta=get_eta(energy_plot)
        xtitle='$\eta*={0:.2f}$, '.format(eta)
    elif energy_plot>5:    
         eta=energy_plot
         xtitle='Energy = {0} GeV, $\u03B8$={1:.2f} deg'.format(eta,itheta)
    else:
        print('IF ENERGY IS LESS THAN 5 GeV THAN MAKE SURE THIS TO CHANGE')
    
    #fig = plt.figure( figsize=(6, 4))
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    ene_good=good_energy_hcal
    
    ene_total_insert_temp = ak.sum(good_energy_hinsert,axis=-1)
    ene_total_insert_only = np.divide(ene_total_insert_temp,sampling_fraction_hcali)
    
    
    ene_total_hcal_temp = ak.sum(good_energy_hcal,axis=-1)
    ene_total_hcal_only = np.divide(ene_total_hcal_temp,sampling_fraction_hcal)
                
               
                
    ## Total        
    ene_total=np.add(ene_total_hcal_only,ene_total_insert_only)
  
    
    mean_guess=np.mean(ene_total)
    sigma_guess=np.std(ene_total)
    
    count, bins,_= plt.hist(np.array(ene_total),bins=nbins,alpha=0.5,range=(0,max_range),label='HCAL',linewidth='3',color='b')
    binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])
    #print (count)

    ## CHOOSE THE DATA POINTS WITHIN GIVEN SIGMAS FOR FITTING
    mask=(binscenters>(mean_guess-FIT_SIGMA*sigma_guess)) & (binscenters<(mean_guess+FIT_SIGMA*sigma_guess))
    error_counts=np.sqrt(count)
    error_counts=np.where(error_counts==0,1,error_counts)
    
    # PARAMETER BOUNDS ARE NOT USED FOR NOW
    param_bounds=([-np.inf,-np.inf,-np.inf], [np.inf,np.inf,np.inf])
    popt, pcov = curve_fit(gaussian, binscenters[mask], count[mask],p0=[np.max(count),mean_guess,sigma_guess],bounds=param_bounds)
        
    ax.plot(binscenters[mask], gaussian(binscenters[mask], *popt), color='red',linestyle='dashed', linewidth=2.5, label=r'F')
    #ax.set_title("Energy = {0} GeV ".format(energy_plot))
    ax.set_title(xtitle)
    ax.xaxis.set_major_locator(MultipleLocator(steps))
    ax.set_xlabel("Event energy (MeV)",fontsize=30)
    FigName='Fit_SimEnergy_{0}_{1}.png'.format(energy_plot,particle)
    
    ### GET MEAN SIGMA AND ERRORS FROM FIT
    mean=popt[1]
    std=popt[2]
   

    
    #errors=np.sqrt(np.diag(pcov))
    mean_error=np.sqrt(pcov[1, 1])
    std_error=np.sqrt(pcov[2, 2])
    #print(mean_guess,'   sigma   ', sigma_guess,' actual mean ', mean,  'actual std',std)  
    ### GET THE BIN WITH VALUE WHERE IT LIES mEAN -3SIGMA
    two_sig_threshold=mean-(Sigma_For_leakage*std)
    bin_2sig=np.digitize(two_sig_threshold,bins)
    
    ### GET FRACTION OF lEAKAGE
    num_leak=np.sum(count[0:bin_2sig])
    deno_leak=np.sum(count)
    leak_per=(num_leak/deno_leak)*100
    if leak_per==0:
        leak_per_error=0
    else:    
        leak_per_error=np.sqrt((np.sqrt(num_leak)/num_leak)**2 + (np.sqrt(deno_leak)/deno_leak)**2)*leak_per

    resolution=(std/mean)
    resolution_error=(np.sqrt((std_error/std)**2 + (mean_error/mean)**2))*resolution
        
    #mean=f'{mean:.2f}'
    mean=format(mean,'.2f')
    mean_error='{0:.3f}'.format(mean_error)
    
    std= '{0:.2f}'.format(std)
    std_error= '{0:.3f}'.format( std_error)

    leak_per= '{0:.3f}'.format(leak_per)
    leak_per_error='{0:.4f}'.format(leak_per_error)
    
    resolution = '{0:.2f}'.format(resolution)
    resolution_error ='{0:.4f}'.format(resolution_error)
    
    
    ratio_ene=float(mean)/float(energy_plot)
    ratio_ene='{0:.2f}'.format(ratio_ene)
    ratio_ene=float(ratio_ene)
    ax.text(80,250,"Resolution={0}" .format(resolution))
    ax.text(80,300,r'$\frac{Pred_{E}}{Truth_{E}}$ =' + '{0:.2f}'.format(ratio_ene))
 
    #ax.tick_params('both', length=20, width=2, which='major')
    #ax.tick_params('both', length=10, width=1, which='minor')
    plt.savefig(f"{PathToPlot}{FigName}")
    plt.show()
    return mean, std, mean_error, std_error, leak_per,leak_per_error,resolution,resolution_error




### THIS FUNCTION DRAWS THE HISTOGRAM NO ANY FITS TO IT
def get_histo(good_energy,energy_plot, particle,Sigma_For_leakage):
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    ene_good=good_energy

    
    ene_total = ak.sum(ene_good,axis=-1)

    ene_average = ak.mean(ene_good,axis=-1)
    #mask=ene_total<400

    #ax.hist(ak.flatten(time),bins=100, range=(0,200),color='r', linewidth='3')
    
   
    mean_guess=np.mean(ene_total)
    sigma_guess=np.std(ene_total)
    nbins=300
    count, bins,_= plt.hist(np.array(ene_total),bins=nbins,alpha=0.5,range=(0,60),label='HCAL',color='b',histtype='step',linewidth=8)
    ax.set_title("HCAL Insert Energy = {0} GeV ".format(energy_plot))
    
    #ax.set_title("Energy = {0} GeV, $\eta$=3.7".format(energy_plot))
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.set_xlabel("Event energy (MeV)")
    ax.set_yscale('log')
    FigName='Fit_SimEnergy_{0}_{1}.png'.format(energy_plot,particle)
    plt.show()
   


 ### READS HCAL_INSERT WITH MIXTURE OF TUNGSTEN AND STEEL
def read_rootfile_HCAL_Insert(fileindex,fraction,FilePathReco,ienergy,theta,particle,Time_Threshold,Energy_Threshold):
    FileName="insert_reco_{0}_{1}GeV_theta_{2}{3}.edm4hep.root".format(particle,ienergy,theta,fileindex)
    events=ur.open(f"{FilePathReco}{FileName}:events")
    total_Events=events.num_entries
    event_cut=total_Events/fraction
    print('HELLO JELLO', total_Events)
    #events_cut=
    events.keys()
    arrays = events.arrays(entry_start=0,entry_stop=event_cut)
    ene = Gev_To_MeV*(arrays['HcalEndcapPInsertHitsReco.energy'][:]) # in Mev
    
    time = (arrays['HcalEndcapPInsertHitsReco.time'][:]) # in ns
    #time = (ak.flatten(arrays['HcalEndcapPInsertHitsReco.time'][:])) # in ns
    PosRecoX = (arrays['HcalEndcapPInsertHitsReco.position.x'])/10.0
    PosRecoY = (arrays['HcalEndcapPInsertHitsReco.position.y'])/10.0
    PosRecoZ= (arrays['HcalEndcapPInsertHitsReco.position.z'])/10.0

    
    cut_primary = arrays["MCParticles.generatorStatus"]==1
    px = arrays['MCParticles.momentum.x'][cut_primary]
    py = arrays['MCParticles.momentum.y'][cut_primary]
    pz = arrays['MCParticles.momentum.z'][cut_primary]
    mass = arrays["MCParticles.mass"][cut_primary]
    ID=arrays['MCParticles.PDG']#[cut_primary]
    
    #Calculate generated primary particle properties
    mom = np.sqrt(px**2+py**2+pz**2)
    energy_gen = np.sqrt(mom**2+mass**2)
    #fig = plt.figure( figsize=(8, 6))
    phi = np.arctan2(py,px)


    mask=(ene>Energy_Threshold)  & (time<Time_Threshold) & (ene<1e10)
    ene_good=ene[mask]
     
    return ene,time,PosRecoX,PosRecoY,PosRecoZ,mass,mom,energy_gen,phi,ene_good



def print_decimal_pi_update(type,fir_particle,pi_means, pi_means_error, pi_stds,pi_stds_error,pi_leaks_per, pi_leaks_per_error,pi_resolutions,pi_resolution_errors):

    particle=first2(fir_particle)
    print('{0}_means_{1}=['.format(particle,type),end="")
    print(*pi_means,sep=',',end =" ")
    print( ']')
    
    print('{0}_means_error_{1}=['.format(particle,type),end="")
    print(*pi_means_error,sep=',',end =" ")
    print( ']')
    
    print('{0}_stds_{1}=['.format(particle,type),end =" ")
    print(*pi_stds,sep=',',end =" ")
    print( ']')
    
    print('{0}_stds_error_{1}=['.format(particle,type),end =" ")
    print(*pi_stds_error,sep=',',end =" ")
    print( ']')
    print('{0}_leaks_per_{1}=['.format(particle,type),end =" ")
    print(*pi_leaks_per,sep=',',end =" ")
    print( ']')
    
    print('{0}_leaks_per_error_{1}=['.format(particle,type),end =" ")
    print(*pi_leaks_per_error,sep=',',end =" ")
    print( ']')
    print('{0}_resolutions_{1}=['.format(particle,type),end =" ")
    print(*pi_resolutions,sep=',',end =" ")
    print( ']')
    print('{0}_resolutions_errors_{1}=['.format(particle,type),end =" ")
    print(*pi_resolution_errors,sep=',',end =" ") 
    print( ']')

    
def first2(s):
    return s[:-1]

def get_eta(thetas):
    theta_to_rad=math.pi/180.
    minus_theta=180-thetas
    theta_rad_half=np.sin(thetas*theta_to_rad/2.0)
    calc_etas=np.log(theta_rad_half)*-1.0
    return calc_etas
def get_greek_particle(particle):
    if particle=='pi-':
        greek_particle='$\pi^{-}$'
    elif particle=='e-':
        greek_particle='$e^-$'
    else:
        print("You forgot to pick the particle")
    return greek_particle



### THIS IS THE SUM WITH THE WEIGHT SUM OF HCAL AND HCALI
def get_resolution_hcalall_weighted(wt,good_energy_hcal,good_energy_hinsert,energy_plot, particle,Sigma_For_leakage):
    if wt=='on':
        sampling_fraction_hcali=0.0098*1000 #(GeV-1) old val 0.0092
        sampling_fraction_hcal=0.022*1000  #(GeV-1) old val 0.0215
        max_range=150
        nbins=400
        xlabel="Energy (GeV)"
        total_xdiv=5
    else:
        sampling_fraction_hcali=1 #(GeV-1)
        sampling_fraction_hcal=1  #(GeV-1)
        max_range=1300
        nbins=200
        xlabel="Energy (MeV)"
        total_xdiv=4
    min_range=0
    xdiv=int((max_range-min_range)/total_xdiv)
    if energy_plot<5:
        eta=get_eta(energy_plot)
        xtitle='$\eta*={0:.2f}$'.format(eta)
    elif energy_plot>5:    
         eta=energy_plot
         xtitle='Energy = {0} GeV'.format(eta)
    else:
        print('IF ENERGY IS LESS THAN 5 GeV THAN MAKE SURE THIS TO CHANGE')
    
    #fig = plt.figure( figsize=(6, 4))
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
       
    
    ene_total_hcal_temp = np.sum(good_energy_hcal,axis=-1)
    ene_total_hcal=np.divide(ene_total_hcal_temp,sampling_fraction_hcal)
    
    ene_total_hinsert_temp = np.sum(good_energy_hinsert,axis=-1)
    ene_total_hinsert = np.divide( ene_total_hinsert_temp,sampling_fraction_hcali)
    
    ene_total=np.add(ene_total_hcal,ene_total_hinsert)
    #ene_average = ak.mean(ene_good,axis=-1)
    #ene_nhits = ak.num(ene_good)
    #HCAL_total=HCAL_total[0:90]

    # print(good_energy_hcal,'       ',good_energy_hinsert)
    #print(ene_total_hcal,' insert  ',ene_total_hinsert,' total ',ene_total)
    
    mean_guess=np.mean(ene_total)
    sigma_guess=np.std(ene_total)
    
    count, bins,_= plt.hist(np.array(ene_total),bins=nbins,alpha=0.5,range=(min_range,max_range),label='HCAL',linewidth='3',color='b')
    binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])
    #print (count)
    
    ## CHOOSE THE DATA POINTS WITHIN GIVEN SIGMAS FOR FITTING
    mask=(binscenters>(mean_guess-FIT_SIGMA*sigma_guess)) & (binscenters<(mean_guess+FIT_SIGMA*sigma_guess))
    error_counts=np.sqrt(count)
    error_counts=np.where(error_counts==0,1,error_counts)
    
    # PARAMETER BOUNDS ARE NOT USED FOR NOW
    param_bounds=([-np.inf,-np.inf,-np.inf], [np.inf,np.inf,np.inf])
    popt, pcov = curve_fit(gaussian, binscenters[mask], count[mask],p0=[np.max(count),mean_guess,sigma_guess],bounds=param_bounds)
      
    ax.plot(binscenters[mask], gaussian(binscenters[mask], *popt), color='red', linewidth=2.5, label=r'F')
    #ax.set_title("Energy = {0} GeV ".format(energy_plot))
    ax.set_title(xtitle)
    ax.xaxis.set_major_locator(MultipleLocator(xdiv))
    ax.set_xlabel(xlabel)
    FigName='Fit_SimEnergy_{0}_{1}.png'.format(energy_plot,particle)
    
    ### GET MEAN SIGMA AND ERRORS FROM FIT
    mean=popt[1]
    std=popt[2]
   

    
    #errors=np.sqrt(np.diag(pcov))
    mean_error=np.sqrt(pcov[1, 1])
    std_error=np.sqrt(pcov[2, 2])
    #print(mean_guess,'   sigma   ', sigma_guess,' actual mean ', mean,  'actual std',std)  
    ### GET THE BIN WITH VALUE WHERE IT LIES mEAN -3SIGMA
    two_sig_threshold=mean-(Sigma_For_leakage*std)
    bin_2sig=np.digitize(two_sig_threshold,bins)
    
    ### GET FRACTION OF lEAKAGE
    num_leak=np.sum(count[0:bin_2sig])
    deno_leak=np.sum(count)
    leak_per=(num_leak/deno_leak)*100
    if leak_per==0:
        leak_per_error=0
    else:    
        leak_per_error=np.sqrt((np.sqrt(num_leak)/num_leak)**2 + (np.sqrt(deno_leak)/deno_leak)**2)*leak_per

    resolution=(std/mean)
    resolution_error=(np.sqrt((std_error/std)**2 + (mean_error/mean)**2))*resolution
        
    #mean=f'{mean:.2f}'
    mean=format(mean,'.2f')
    mean_error='{0:.3f}'.format(mean_error)
    
    std= '{0:.2f}'.format(std)
    std_error= '{0:.3f}'.format( std_error)

    leak_per= '{0:.3f}'.format(leak_per)
    leak_per_error='{0:.4f}'.format(leak_per_error)
    
    resolution = '{0:.5f}'.format(resolution)
    resolution_error ='{0:.4f}'.format(resolution_error)
    
    ####### PRINT THE VERTICLE LINE WITH 2 SIGMA ################    
    #ax.vlines([two_sig_threshold,  two_sig_threshold],0, np.max(count),linestyles='dashed', colors='m', linewidth=5)
   
 
    #ax.tick_params('both', length=20, width=2, which='major')
    #ax.tick_params('both', length=10, width=1, which='minor')
    plt.savefig(f"{PathToPlot}{FigName}")
    plt.show()
    return mean, std, mean_error, std_error, leak_per,leak_per_error,resolution,resolution_error




#####################################
def get_resolution_hcal_only(good_energy,energy_plot, particle,Sigma_For_leakage,wt):
    if wt=='on':
        print("I am wt")
        sampling_fraction_hcali=0.0098*1000 #(GeV-1) old val 0.0092
        sampling_fraction_hcal=0.022*1000  #(GeV-1) old val 0.0215
        max_range=150
        xtitle='Energy (GeV)'
        ytitle='Count'
        nbins=75
        steps=20
    else:
        sampling_fraction_hcali=1 #(GeV-1)
        sampling_fraction_hcal=1  #(GeV-1)
        max_range=2500
        xtitle='Energy (GeV)'
        ytitle='Count'
        nbins=250
        steps=200

    
    ## Differenciate between energy or theta/etas on y axis
    greek_particle=get_greek_particle(particle)
    if energy_plot<5:
        eta=get_eta(energy_plot)
        title_head=r'$\eta*$={0:.2f}'.format(eta)
       
    elif energy_plot>5:    
         eta=energy_plot
         title_head='{0}, Energy = {1} GeV'.format(greek_particle,eta)
    else:
        print('IF ENERGY IS LESS THAN 5 GeV THAN MAKE SURE THIS TO CHANGE')
    #print('xxxxxxxxxxxxxxxxxxxxxx',title_head)
    #fig = plt.figure( figsize=(6, 4))
    fig,ax = plt.subplots(1,1, figsize=(16, 12),sharex=True,sharey=True)
    ene_good=good_energy

    
    ene_total_temp = np.sum(ene_good,axis=-1)
    ene_total = np.divide(ene_total_temp,sampling_fraction_hcal)
    
   

    ene_average = ak.mean(ene_good,axis=-1)
    #ene_nhits = ak.num(ene_good)
    #HCAL_total=HCAL_total[0:90]

    mean_guess=np.mean(ene_total)
    sigma_guess=np.std(ene_total)
    
    
   
    count, bins,_= plt.hist(np.array(ene_total),bins=nbins,alpha=0.5,range=(0,max_range),label='HCAL',color='b',linewidth=8)#histtype='step'            
    binscenters = np.array([0.5 * (bins[i] + bins[i+1]) for i in range(len(bins)-1)])
    
    #plt.show()
    #return 1
    #print (count)
    
    ax.set_xlabel(xtitle)
    ax.set_ylabel("Entries")
    ## CHOOSE THE DATA POINTS WITHIN GIVEN SIGMAS FOR FITTING
    mask=(binscenters>(mean_guess-FIT_SIGMA*sigma_guess)) & (binscenters<(mean_guess+FIT_SIGMA*sigma_guess))
    error_counts=np.sqrt(count)
    error_counts=np.where(error_counts==0,1,error_counts)
    
    # PARAMETER BOUNDS ARE NOT USED FOR NOW
    param_bounds=([-np.inf,-np.inf,-np.inf], [np.inf,np.inf,np.inf])
    popt, pcov = curve_fit(gaussian,binscenters[mask],count[mask],p0=[np.max(count),mean_guess,sigma_guess],bounds=param_bounds)
        
    ax.plot(binscenters[mask], gaussian(binscenters[mask], *popt), color='red',linestyle='dashed', linewidth=2.5, label=r'F')
    
    #ax.set_title("Energy = {0} GeV ".format(energy_plot))
    #ax.set_title(title_head)
    
    #ax.set_title("Energy = {0} GeV, $\eta$=3.7".format(energy_plot))
    ax.xaxis.set_major_locator(MultipleLocator(steps))
    ax.set_xlabel(xtitle,fontsize=30)
    ax.set_ylabel("Entries")
    FigName='Fit_SimEnergy_{0}_{1}.png'.format(energy_plot,particle)

    ### GET MEAN SIGMA AND ERRORS FROM FIT
    mean=popt[1]
    std=popt[2]
    
  
    #errors=np.sqrt(np.diag(pcov))
    mean_error=np.sqrt(pcov[1, 1])
    std_error=np.sqrt(pcov[2, 2])
    #print(mean_guess,'   sigma   ', sigma_guess,' actual mean ', mean,  'actual std',std)  
    ### GET THE BIN WITH VALUE WHERE IT LIES mEAN -3SIGMA
    two_sig_threshold=mean-(Sigma_For_leakage*std)
    bin_2sig=np.digitize(two_sig_threshold,bins)
    
    ### GET FRACTION OF lEAKAGE
    num_leak=np.sum(count[0:bin_2sig])
    deno_leak=np.sum(count)
    leak_per=(num_leak/deno_leak)*100
    if leak_per==0:
        leak_per_error=0
    else:    
        leak_per_error=np.sqrt((np.sqrt(num_leak)/num_leak)**2 + (np.sqrt(deno_leak)/deno_leak)**2)*leak_per

    resolution=(std/mean)
    resolution_error=(np.sqrt((std_error/std)**2 + (mean_error/mean)**2))*resolution
        
    #mean=f'{mean:.2f}'
    mean=format(mean,'.2f')
    mean_error='{0:.3f}'.format(mean_error)
    
    std= '{0:.2f}'.format(std)
    std_error= '{0:.3f}'.format( std_error)

    leak_per= '{0:.3f}'.format(leak_per)
    leak_per_error='{0:.4f}'.format(leak_per_error)
    
    resolution = '{0:.2f}'.format(resolution)
    resolution_error ='{0:.4f}'.format(resolution_error)
    
    
    
    ratio_ene=float(mean)/float(energy_plot)
    ratio_ene='{0:.2f}'.format(ratio_ene)
    ratio_ene=float(ratio_ene)
    ax.text(80,250,"Resolution={0}" .format(resolution))
    ax.text(80,300,r'$\frac{Pred_{E}}{Truth_{E}}$ =' + '{0:.2f}'.format(ratio_ene))
    #plt.text(80,300,r"$\frac{Pred_{E}}{Truth_{E}}$= {0:.2f}".format(ratio_ene))
    ####### PRINT THE VERTICLE LINE WITH 2 SIGMA ################    
    #ax.vlines([two_sig_threshold,  two_sig_threshold],0, np.max(count),linestyles='dashed', colors='m', linewidth=5)
   
 
    #ax.tick_params('both', length=20, width=2, which='major')
    #ax.tick_params('both', length=10, width=1, which='minor')
    plt.savefig(f"{PathToPlot}{FigName}")
    
    plt.show()
    return mean, std, mean_error, std_error, leak_per,leak_per_error,resolution,resolution_error
    



    
