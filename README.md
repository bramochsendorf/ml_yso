# Searching for YSOs in IR databases with Support Vector Machines

NB: this is work in progress. The repo will be updated along the way.

This repo contains the results and analyses of a project that uses a Machine Learning algorithm (SVM) to classify objects as 'Young Stellar Objects' (YSOs) and separates it from known contaminants (background galaxies, planetary nebulae, AGB-stars, etc.) grouped together as 'non-YSOs'. 

## Why?
Our upcoming JWST program will obtain a large amount of data with its MIRI and NIRCam instruments. Because of several time-critical aspects of our program, an automatic classification scheme is necessary to filter out sources-of-interests, which can then be followed-up with the NIRSpec multi-shutter array. 

## Feature selection
YSOs populate a specific area in color-magnitude and color-color space. Often the [4.5 - 8.0] and [8.0 - 24] color is used for classification (e.g., Whitney et al. 2008, AJ, 136, 18). However, there is no area color–magnitude space that can unambiguously separate YSOs from background contaminants (Gruendl et al. 2009, ApJS, 184, 172). Thus, additional features are needed.

Since YSOs are likely located within molecular clouds, we add information on the surrounding dust surface density taken from Gordon et al., 2014, ApJ, 797, 85. Map is available on Karl Gordon's website:

http://www.stsci.edu/~kgordon/magclouds_results/gordon2014.html

## Choice of algorithm, training data, and test data
I start of with a binary classification using a SVM. For classification purposes, one can choose from a variety of learning algorithms. The SVM is a good choice with high-dimensional data (which the final training sample will be, as relevant features are added) and relatively small training samples, provided that a suitable softening parameter is chosen (through cross-validation).

To train the SVM, I use the spectroscopically classifed catalog from the SAGE-spec legacy program, containing ~800 sources (Jones et al. 2017, MNRAS, 470, 3). Of this, 337 are YSOs in various stages or HII regions, which I group together as 'YSO'. All other classes are designated 'non-YSO'. This constitutes my training set (see features_traindata.py)

To test the SVM, I use the catalog from Gruendl et al. 2009, ApJS, 184, 172. The 'definite YSO' subgroup here is estimated to be ~99% correct (Jones et al. 2017, MNRAS, 470, 3), which is my 'YSO' test data. The other sources in this catalog (background galaxies, AGB stars, planetary nebula) are used as the 'non-YSO' test data. The total length of the test data is ~2500 sources, splitted in ~850 YSOs and ~1650 non-YSOs (see features_testdata.py).

## First results
A simple SVM classifier based on 4-dimensional data ([8.0] micron magnitude, [4.5 - 8.0] color, [8.0 - 24] color, and dust surface density) obtains excellent results. It uses a linear kernel, is cross-validated with a grid search, and reaches an average precision and recall of 0.87. See the IPython Notebook svm.ipynb for the analysis and data exploration. Additional relevant features and kernels (polynomial) are currently being explored.
