#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import some things, maybe some more things

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import random
import lmfit
from lmfit import Model
# Creating some data in a way you can optimize or change yourself

# Define some functions
def make_mock_data(num_samples, rng=None):

    # Set up RNG with a seed to have reproducable results
    if rng is None:
        rng = np.random.default_rng(50347765562343433420)

    freq = np.linspace(0, 3000, num_samples)
    noise = 0.5 * rng.uniform(0,2)
    data = (freq/1500) ** (4.4) + noise
    data_err = data * 0.05 * rng.uniform(0,2)

    return freq, data, data_err


def powerlaw(xdata, alpha, constant):
    return constant * (xdata/1500)**alpha    


def get_uncert_from_cov_matrix(cov):
    return np.sqrt(np.diag(cov))


def lmfit_powerlaw(xdata, ydata, yerr, p0):
    plmodel = Model(powerlaw)
    emcee_kws = dict(steps=3000, burn=500, thin=20, is_weighted=False,
                 progress=False)
    result = plmodel.fit(ydata, xdata=xdata, method='emcee',**p0, fit_kws=emcee_kws)

    return result


def get_index(xdata=None, ydata=None, yerrdata=None, Plot=True, Filename=None):
        
    popt, pcov = curve_fit(powerlaw, xdata, ydata)#, sigma=yerrdata)
    
    index = popt[0]
    perr = get_uncert_from_cov_matrix(pcov)
    index_err = perr[0]


    # Try a 'different' fitting
    p0 = {"alpha": 4, "constant": 1}
    result = lmfit_powerlaw(xdata, ydata, yerrdata, p0)
    alpha = result.params['alpha'].value
    alpha_err = result.params['alpha'].stderr
    constant = result.params['constant'].value
    
    if Plot:
        plt.scatter(xdata, ydata)
        plt.errorbar(xdata, ydata, yerr=yerrdata, fmt=' ', alpha=0.3)
        plt.plot(xdata, powerlaw(xdata, *popt), 'r-',
                 label=r'fit: $\alpha$=%5.3f, C=%5.3f' % tuple(popt))

        plt.plot(xdata, result.best_fit, "k:", label=f"lmfit: {alpha:.3f}, C={constant:.3f}", linewidth=2)

        print(result.params.items())

        plt.ylabel(r"Scintillation Bandwidth, $\Delta\nu_D$ (MHz)")
        plt.xlabel("Observational Frequency (MHz)")
        plt.legend()
        if Filename:
            plt.savefig(f'{filename}.png')
        plt.show()
        plt.close()
    
    return index, index_err


if __name__ == "__main__":
    # Call the functions and print/save results
    freq, data, data_err = make_mock_data(num_samples=1000)
    index, index_err = get_index(xdata=freq, ydata=data, yerrdata=data_err, Plot=True, Filename=None)
    print(f"The relationship between observational frequency and scintilation bandwidth, alpha, was found to be: alpha= {index:.4f} +/- {index_err:.5f}")
