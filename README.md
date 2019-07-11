## Negative Selection Algorithm/V-detector in python

Adapted by Kang Min Zhe, this was done during my research stint in iTrust SUTD.

## Introduction

Anomaly detection is based upon the Negative Selection Algorithm (NSA), which belongs to the class computational methods called Artificial Immune Systems (AIS). NSA assumes a distinction can be made between a so-called self and non-self states of the system. Here, self refers to states representing normal behavior, while non-self corresponds to anomalies. A crucial element in NSA is the generation of a set of so-called detectors, which covers the non-self region. 

This uses the V-detector algorithm to construct a set of variable sized detectors. Starting point of the algorithm is historical data that corresponds to normal operation states. After normalization and dimension reduction, this data is used to define the self region. 

Next, in the training phase a detector set is generated. In general, NSA aims for a minimum set of detectors given a sufficiently high coverage of the non-self region.

Adapted and re-coded from [Zhou Ji](http://zhouji.net.s3-website-us-east-1.amazonaws.com/vdetector.html) which has an implementation of the algorithm in Java. 

More information about this algorithm can be found [here](https://www.semanticscholar.org/paper/V-detector%3A-An-efficient-negative-selection-with-Ji-Dasgupta/10f6e1740f05268fe3d0cb0aaa312b80dbdaadf8)

## Pre-processing

SWaT test bed data is being used in this example. First step is to clean the data and remove any "noise" or data that are incorrect. One such example would be as observed.
![1](https://i.imgur.com/PTwhLSg.png)
where the value of AIT is set at a particular value at a time, however is not reflected on the actual data set. As a result, this leads to inaccuracy of data and hence must be cleaned.
![2](https://i.imgur.com/l2hX9qL.png)

Next, other methods such as [StandardScaling](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) in `sklearn`
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

Done initially with no detectors overlap(green circles).

![3](https://i.imgur.com/lDbh510.png)

Done with detectors overlap, which resulted a larger coverage in 2D space.

![4](https://i.imgur.com/r7qPYsL.png)

Visualizations done in 3D space, to get a better feel of the space.

![5](https://media.giphy.com/media/Q5chI7vxkBfF9D8IHZ/giphy.gif)

Algorithms such as the monte carlo integration is being applied to calculate the self-space to get a better picture of the volume of the self space in greater dimensions such as 5 or 6. One such implementation was to estimate the area of the circle.

![6](https://i.imgur.com/Jl94TWi.gif)

## Implementation

Source is available in `python`, however the cleaned data is not available.

## License
MIT
