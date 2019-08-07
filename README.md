## Negative Selection Algorithm/V-detector in python

Adapted by Kang Min Zhe, this was done during my research stint in iTrust SUTD.

I would like to give thanks to Dr Robert Kooij and Dr. Nandha Kumar for offering their guidance.

## Introduction

Anomaly detection is based upon the Negative Selection Algorithm (NSA), which belongs to the class computational methods called Artificial Immune Systems (AIS). NSA assumes a distinction can be made between a so-called self and non-self states of the system. Here, self refers to states representing normal behavior, while non-self corresponds to anomalies. A crucial element in NSA is the generation of a set of so-called detectors, which covers the non-self region. 

This uses the V-detector algorithm to construct a set of variable sized detectors. Starting point of the algorithm is historical data that corresponds to normal operation states. After normalization and dimension reduction, this data is used to define the self region. 

Next, in the training phase a detector set is generated. In general, NSA aims for a minimum set of detectors given a sufficiently high coverage of the non-self region.

Adapted and re-coded from [Zhou Ji](http://zhouji.net.s3-website-us-east-1.amazonaws.com/vdetector.html) which has an implementation of the algorithm in Java. 

More information about this algorithm can be found [here](https://www.semanticscholar.org/paper/V-detector%3A-An-efficient-negative-selection-with-Ji-Dasgupta/10f6e1740f05268fe3d0cb0aaa312b80dbdaadf8) and info about SWaT data could be found [here](https://itrust.sutd.edu.sg/testbeds/secure-water-treatment-swat/)

## Pre-processing

SWaT test bed data is being used in this example. First step is to clean the data and remove any "noise" or data that are incorrect. One such example would be as observed.
![1](https://i.imgur.com/PTwhLSg.png)
where the value of AIT is set at a particular value at a time, however is not reflected on the actual data set. As a result, this leads to inaccuracy of data and hence must be cleaned via by correction or complete removal of it.
![2](https://i.imgur.com/l2hX9qL.png)

Other methods such as [StandardScaling](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) in `sklearn`
 package is being used to scale the data.

[PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html) is then being used to apply on the data to further reduce the dimensions of the data to 2, such that it is more easily to work with.

Lastly [MinMaxScaling](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html) is being used to normalize the data-set from [0,1].

## Algorithms

Some algorithms used includes:
* Euclidean Distance
* Manhattan Distance
* Monte Carlo Integration

## Visualization of Algorithms

Visualization of the detector generation was done first, each with 60 detectors being generated.

This was done initially with no detectors overlap. The green circles refers to the detectors while the grey circles are the self data which are data that are considered normal. Calculations are done in euclidean distance.

![3](https://i.imgur.com/lDbh510.png)

This was also done with detectors overlap, which resulted a larger coverage area in 2D space and also a faster generation of detector as the algorithm was free to generate detectors.

![4](https://i.imgur.com/r7qPYsL.png)

Visualizations done in 3D space, to get a better feel of the space. The same sample was converted to 3D form such that for the same number of detectors and an addition of axis, we can see the increase in "blank" space available.

![5](https://media.giphy.com/media/Q5chI7vxkBfF9D8IHZ/giphy.gif)

Algorithms such as the monte carlo integration is being applied to calculate the self-space to get a better picture of the volume of the self space in greater dimensions such as 5D or 6D. One such implementation was to estimate the area of the circle, where we can use the ratio of number of blue dots compared to the total number of dots to obtain the area of the space occupied. 

![6](https://i.imgur.com/Jl94TWi.gif)

## Implementation

Source code is available in `python`, however the cleaned data is not available. 

## Discussion

The algorithm was ran a couple of times, however the results produced was fairly poor for the SWaT dataset, with an average of ~1% detection rate. This was mainly due to the Hughes Phenomenon and the Curse of Dimensionality, where as the number of features increases, the classifier’s performance increases as well until we reach the optimal number of features. Adding more features based on the same size as the training set will then degrade the classifier’s performance. This especially applies to calculations which involves distance metrics such as euclidean or manhatten distance. Hence for larger dimensions with little to no correlation, the V-detectors are not a suitable candidate to detect such anomalies.

![7](https://i.imgur.com/o1quWlx.png)

The following shows a basic visualization of how the data looks like when PCA is applied to the data set with 51 dimensions to 2 dimensions. As we can tell, the data is mostly scrambled with the Attacks and Normal. This is evident as the data set had no linear correlation with each other and is also mixed with both categorical and continuous data. Other techniques of dimension reduction such as Multiple Correspondence Analysis should be used for such data. One limitation of this algorithm is that for high-dimensional data, it is generally not suitable to use, and instead Neural Network or Random Forest Classifier is preferred for such data. Moreover, the V-detectors algorithm does not prevent under/overfitting of the data. Hence, a different approach could be used for the V-detectors. 

The Random Forest Classifier, on the other hand, achieved great results, with ~99% ofthe data (400,000+) predicted corrected and only 10 predicted wrongly. The confusion matrix is shown as the following:

![8](https://i.imgur.com/dcojt1W.png)

## Discussion and use case of V-detectors

One other instance of the V-detectors usage was for the EPiC dataset (which was another lab in iTrust). 4 features of having similar linear correlation were picked for this testing and the basic visualization of the data could be seen as below.

![9](https://i.imgur.com/nAoExSL.png)

For such an instance, we can clearly see how the data points are separated from each other, hence making the euclidean metrics a good way of identifying anomalies and has achieved ~100% detection rate with ~0.05% false positive rate  Applying such an algorithm is mostly suitable for smaller scale deployment such as individual PLCs(Programmable Logic Controllers) and could be potentially combined with algorithms such as Random Forest Classification for a more complete detection of anomalies.

## Conclusion

Anomaly detection is often a challenge industries faced and choosing the right model for the right case is imperative to ensuring high detection of the data. Often we are provided with data that are filled with data that might not be useful, hence pre-processing of the data is especially important and is vital for the model to be accurate. Additionally, choosing the suitable machine-learning model is also important; for this case, the Random Forest Classification is better at detecting anomalies with multiple features, however the V-detectors are much more robust in the sense that it can detect anomalies quickly as it is lightweight, albeit it doesnt work with higher-dimensional data.

## Other Algorithms

Source codes for other algorithms used and tested is available.
* Random Forest Classification adapted with numpy
* Multivariate Gaussian Distribution 

## License
MIT
