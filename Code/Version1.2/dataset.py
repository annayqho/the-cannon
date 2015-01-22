import numpy as np
import matplotlib.pyplot as plt
import triangle

"""Classes and methods for a Dataset of stars.

Provides the ability to initialize the dataset, modify it by adding or
removing spectra, changing label names, adding or removing labels.

Methods
-------
remove_stars

"""

class Dataset(object):
    """A class to represent a Dataset of stellar spectra and labels.
    
    Parameters
    ----------
    IDs: numpy ndarray, list
        Specify the names (or IDs, in whatever format) of the stars.
    lambdas: numpy ndarray
        Wavelength array corresponding to the pixels in the spectrum
    spectra: numpy ndarray
        spectra[:,:,0] = flux (spectrum)
        spectra[:,:,1] = flux error array
    labels: numpy ndarray, list, optional
        Reference labels for reference set, but None for test set
    
    Methods
    -------
    set_IDs
    set_spectra
    set_label_names
    set_label_vals
    choose_labels
    choose_spectra
    label_triangle_plot

    """

    def __init__(self, IDs, SNRs, lambdas, spectra, label_names, label_vals=None):
        self.IDs = IDs
        self.SNRs = SNRs
        self.lambdas = lambdas
        self.spectra = spectra 
        self.label_names = label_names
        self.label_vals = label_vals
  
    def set_IDs(self, IDs):
        self.IDs = IDs

    def set_lambdas(self, lambdas):
        self.lambdas = lambdas

    def set_spectra(self, spectra):
        self.spectra = spectra

    def set_label_names(self, label_names):
        self.label_names = label_names

    def set_label_vals(self, label_vals):
        self.label_vals = label_vals

    def choose_labels(self, cols):
        """Updates the label_names and label_vals properties

        Input: list of column indices corresponding to which to keep
        """
        new_label_names = [self.label_names[i] for i in cols]
        colmask = np.zeros(len(self.label_names), dtype=bool)
        colmask[cols]=1
        new_label_vals = self.label_vals[:,colmask]
        self.set_label_names(new_label_names)
        self.set_label_vals(new_label_vals)

    def choose_spectra(self, mask):
        """Updates the ID, spectra, label_vals properties 

        Input: mask where 1 = keep, 0 = discard
        """
        self.set_IDs(self.IDs[mask])
        self.set_spectra(self.spectra[mask])
        self.set_label_vals(self.label_vals[mask])

    def label_triangle_plot(self, figname):
        """Plots every label against every other label"""
        texlabels = []
        for label in self.label_names:
            texlabels.append(r"$%s$" %label)
        fig = triangle.corner(self.label_vals, labels=texlabels,
                show_titles=True, title_args = {"fontsize":12})
        #fig.gca().annotate("Label Triangle Plot")
        fig.savefig(figname)
        print "Plotting every label against every other"
        print "Saved fig %s" %figname
        plt.close(fig)

def dataset_prediagnostics(reference_set, test_set):
    # Plot SNR distributions
    print "Diagnostic for SNRs of reference and survey stars"
    plt.hist(reference_set.SNRs, alpha=0.5, label="Ref Stars")
    plt.hist(test_set.SNRs, alpha=0.5, label="Survey Stars")
    plt.legend(loc='upper right')
    plt.xscale('log')
    plt.title("SNR Comparison Between Reference & Test Stars")
    plt.xlabel("log(Formal SNR)")
    plt.ylabel("Number of Objects")
    figname = "SNRdist.png"
    plt.savefig(figname)
    plt.close()
    print "Saved fig %s" %figname

    # Plot all reference labels against each other
    figname = "reference_labels_triangle.png"
    reference_set.label_triangle_plot(figname)

def dataset_postdiagnostics(reference_set, test_set):
    # 2-sigma check from reference labels
    label_names = reference_set.label_names
    nlabels = len(label_names)
    reference_labels = reference_set.label_vals
    test_labels = test_set.label_vals
    test_IDs = test_set.IDs
    mean = np.mean(reference_labels, 0)
    stdev = np.std(reference_labels, 0)
    lower = mean - 2 * stdev
    upper = mean + 2 * stdev
    for i in range(nlabels):
        label_name = label_names[i]
        test_vals = test_labels[:,i]
        warning = np.logical_or(test_vals < lower[i], test_vals > upper[i])
        flagged_stars = test_IDs[warning]
        filename = "flagged_stars_%s.txt" %i
        output = open(filename, 'w')
        for star in test_IDs[warning]:
            output.write(star + '\n')
        output.close()
        print "Reference label %s" %label_name
        print "flagged %s stars beyond 2-sig of reference labels" %sum(warning)
        print "Saved list %s" %filename

    # Plot all survey labels against each other
    figname = "survey_labels_triangle.png"
    test_set.label_triangle_plot(figname)

    # 1-1 plots of all labels
    for i in range(nlabels):
        name = label_names[i]
        orig = reference_labels[:,i]
        cannon = test_labels[:,i]
        low = np.minimum(min(orig), min(cannon))
        high = np.maximum(max(orig), max(cannon))
        plt.plot([low, high], [low, high], 'k-', linewidth=2.0, label="x=y")
        plt.scatter(orig, cannon)
        plt.legend()
        plt.xlabel("Reference Value")
        plt.ylabel("Cannon Output Value")
        plt.title("1-1 Plot of Label " + r"$%s$" %name)
        figname = "1to1_label_%s.png" %i
        plt.savefig(figname)
        print "Diagnostic for label output vs. input"
        print "Saved fig %s" %figname
        plt.close()

def remove_stars(dataset, mask):
    """A method to remove a subset of stars from the Dataset. 
    
    Parameters
    ---------
    mask: numpy ndarray of booleans. True means "remove"
    """
    ntokeep = 1-np.sum(mask)
    return Dataset(dataset.IDs[mask], dataset.lambdas[mask], 
            dataset.spectra[mask], dataset.label_names, dataset.label_vals[mask])
    print "New dataset constructed with %s stars included" %ntokeep
