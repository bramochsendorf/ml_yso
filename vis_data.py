import matplotlib.pyplot as plt
import numpy as np

def visdata(index,x80,x45_80,x80_24,dust,color,set):

    fig = plt.figure(figsize=(16,5))
    font = {'size':9}
    plt.rc('font', **font)

    plt.subplot(131)
    plt.scatter(x45_80,x80,c=color)
    plt.xlabel('[8.0]')
    plt.ylabel('[4.5-8.0]')

    plt.subplot(132)
    plt.scatter(x80_24,x80,c=color)
    plt.xlabel('[8.0]')
    plt.ylabel('[8.0-24]')

    plt.subplot(133)
    plt.scatter(np.random.choice(index,len(index),replace=False),dust,c=color)
    plt.xlabel('Source index')
    plt.ylabel(r'Log[$\Sigma_\mathrm{dust}$ $M_\mathrm{\odot}$ pc$^{-2}$]')
    
    plt.savefig('output/visualize_features_'+set+'.pdf', dpi=150, bbox_inches='tight', pad_inches=0.2)
    
    return fig
