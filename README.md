# Searching for YSOs in IR databases with Support Vector Machines

NB: this is work in progress. The repo will be updated along the way.

This repo contains the results and analyses of a project that uses a Machine Learning algorithm (SVM) to classify objects as 'Young Stellar Objects' (YSOs) and separates it from known contaminants (background galaxies, planetary nebulae, AGB-stars, etc.) grouped together as 'non-YSOs'. 

## Why?
Our upcoming GTO program with the James Webb Space Telescope will observe millions of sources with its MIRI and NIRCam instruments. Because of several time-critical aspects of the program, an automatic classification scheme is necessary to filter out sources-of-interests, which will then be followed-up with the NIRSpec multi-shutter array. 

## Conclusions
A simple binary classification based on 4-dimensional data ([8.0] micron magnitude, [4.5 - 8.0] color, [8.0 - 24] color, and dust surface density) obtains excellent results. After establishing a baseline result with Naive Bayes (which obtains 0.92 recall/precision), I use a Support Vector Machine to try and improve my results.

It uses an RBF kernel (the data is linearly unseparable), a 10-fold stratisfied cross-validation + grid search for model selection and evaluation, and reaches an average precision and recall of 0.94. The model also does an excellent job classifying objects that occupy the same area in color-color and color-magnitude space (i.e., 'confused' data) with an average accuracy and recall of 0.85. This means the feature based on dust surface density is very powerful in separating the classes.

See the IPython Notebook svm.ipynb for the full analysis and data exploration. Additional relevant features (clustering) and algorithms (e.g., Random Forest) are currently being explored and implemented.

## Analysis

### Feature selection
YSOs populate a specific area in color-magnitude and color-color space. Often the [4.5 - 8.0] and [8.0 - 24] color are used for classification (e.g., Whitney et al. 2008, AJ, 136, 18). Nonetheless, there is no area color–magnitude space that can unambiguously separate YSOs from background contaminants (Gruendl et al. 2009, ApJS, 184, 172). Thus, additional features are needed.

Since YSOs are likely located within molecular clouds, I add information on the surrounding dust surface density taken from Gordon et al., 2014, ApJ, 797, 85. The dust map is available on Karl Gordon's website:

http://www.stsci.edu/~kgordon/magclouds_results/gordon2014.html

### Choice of algorithm, model selection, and model evaluation
I start of with a binary classification using Naive Bayes (NB), which is a good starting point for classification problems. Simple and sweet, it provides me with a result that can be considered a baseline for more complicated, discriminative models. I then move on Support Vector Machine (SVM). For classification purposes, one can choose from a variety of learning algorithms. However, The SVM is a good choice for high-dimensional data (which the final training sample will be, as relevant features are added) and relatively small training samples, provided that a suitable softening parameter is chosen through cross-validation.

To train the NB/SVM models, I use the spectroscopically classifed catalog from the SAGE-spec legacy program, containing ~800 sources (Jones et al. 2017, MNRAS, 470, 3). From this, 337 are YSOs in various evolutionary stages or HII regions, which I group together as 'YSO'. All other classes are designated 'non-YSO' (see features_traindata.py). 

I then split the data into training and test sets (70%/30%), and perform model selection + evaluation using a grid search (in the case of SVM; changing the hyperparameter C) with 10-fold stratisfied and repeated (10 times) cross-validation. I use stratification to ensure the training and test sets remain well-balanced, and the repeat to try and lower the variance in my cross-validation results. This gives me a list of models with different hyperparameter C and their respective performance estimates.

To test the NB and SVM models, we take the best performing model and feed it the test data it hasn't seen yet. The model performs extremely well with a precision and recall of 0.92 and 0.94 for the NB and SVM models!

With the model performing very well, there is no reason to hold back part of the original data in the form of test data. I put the train and test data back togther and train the best-performing model with the full dataset.

### Extra 'stress-test' of the fully-trained model
For a more challenging test, I use the source catalog from Gruendl et al. 2009, ApJS, 184, 172. This catalog contains thousands of objects of a variety of classes, occupying the same area in color space. How well does the model in separating out YSOs from a 'confused' color space? 

The 'definite YSO' class from the Gruendl catalog is estimated to be ~99% correct (Jones et al. 2017, MNRAS, 470, 3), which I therfore label as 'YSO'. The other sources in this catalog (background galaxies, AGB stars, planetary nebula) are labelled as 'non-YSO'. The total length of the test data is ~2500 sources, splitted in ~850 YSOs and ~1650 non-YSOs (see features_testdata.py).

Running the SVM model on this data gives me a precision and recall of 0.86. This means that even when sources are overlapping in color space, the model separates YSOs/non-YSOs very successfully! 
