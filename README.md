# Searching for YSOs in IR databases with Support Vector Machines

NB: this is work in progress. The repo will be updated along the way.

This repo contains the results and analyses of a project that uses a Machine Learning algorithm (SVM) to classify objects as 'Young Stellar Objects' (YSOs) and separates it from known contaminants (background galaxies, planetary nebulae, AGB-stars, etc.) grouped together as 'non-YSOs'. 

## Why?
Our upcoming JWST program will obtain a large amount of data with its MIRI and NIRCam instruments. Because of several time-critical aspects of our program, an automatic classification scheme is necessary to filter out sources-of-interests, which will then be followed-up with the NIRSpec multi-shutter array. 

## Conclusions
A simple SVM classifier based on 4-dimensional data ([8.0] micron magnitude, [4.5 - 8.0] color, [8.0 - 24] color, and dust surface density) obtains excellent results. It uses a linear kernel, a 10-fold stratisfied cross-validation + a grid search for model selection, and reaches an average precision and recall of 0.94. The model also does an excellent job classifying objects that occupy the same area in color-color and color-magnitude space (i.e., 'confused' data) with an average accuracy and recall of 0.85. This means the addition of the feature based on the dust surface density is very powerful in separating the classes.

See the IPython Notebook svm.ipynb for the analysis and data exploration. Additional relevant features and kernels are currently being explored.

## Analysis

### Feature selection
YSOs populate a specific area in color-magnitude and color-color space. Often the [4.5 - 8.0] and [8.0 - 24] color is used for classification (e.g., Whitney et al. 2008, AJ, 136, 18). However, there is no area color–magnitude space that can unambiguously separate YSOs from background contaminants (Gruendl et al. 2009, ApJS, 184, 172). Thus, additional features are needed.

Since YSOs are likely located within molecular clouds, we add information on the surrounding dust surface density taken from Gordon et al., 2014, ApJ, 797, 85. Map is available on Karl Gordon's website:

http://www.stsci.edu/~kgordon/magclouds_results/gordon2014.html

### Choice of algorithm, model selection, and model evaluation
I start of with a binary classification using a SVM. For classification purposes, one can choose from a variety of learning algorithms. The SVM is a good choice with high-dimensional data (which the final training sample will be, as relevant features are added) and relatively small training samples, provided that a suitable softening parameter is chosen (through cross-validation).

To train the SVM, I use the spectroscopically classifed catalog from the SAGE-spec legacy program, containing ~800 sources (Jones et al. 2017, MNRAS, 470, 3). From this, 337 are YSOs in various stages or HII regions, which I group together as 'YSO'. All other classes are designated 'non-YSO' (see features_traindata.py). 

I then split the data into a training and test sets (70%/30%), and perform model selection + evaluation using a grid search (changing the 'softening' parameter C) and 10-fold cross-validation. I use stratification to ensure the training and test sets remain well-balanced. This gives me a list models (with different parameter C) and respective performance estimates.

To test the SVM, we take the best performing model and feed it the test data it hasn't seen yet. The model performs extremely well with a precision and recall of 0.94 (!!!), which is good enough for now. 

With the evaluated, well-perfoming model, there is no reason to hold back part of the original data. I continue and train the model with the full dataset (i.e., no split in train/test data).  

### Extra 'stress-test' of the fully-trained model
For a more challenging test, I use the catalog from Gruendl et al. 2009, ApJS, 184, 172. This catalog contains thousands of objects of a variety of classes, but occupying the same area in color space. How well does the model separate out the YSOs in a 'confused' color space? 

Running the model on this data gives me a precision and recall of 0.85. This means that even when sources are overlapping in color space, the model separates YSOs/non-YSOs very successfully.

NB: the 'definite YSO' class of the Gruendl catalog is estimated to be ~99% correct (Jones et al. 2017, MNRAS, 470, 3), which is my 'YSO' test data. The other sources in this catalog (background galaxies, AGB stars, planetary nebula) are labelled as 'non-YSO'. The total length of the test data is ~2500 sources, splitted in ~850 YSOs and ~1650 non-YSOs (see features_testdata.py).
