Error analysis
==============

### All relations vs. all relations in common

The provided XML file consists of annotated events and relations of events.
Those events and relations got annotated by more than one person and different people annotated different events and relations.

Therefore it was reasonable to check for which case the accuracy of the classification on the test set was higher.
It turned out that there is no noticeable difference in accuracy.


### Different number of trees in the random forest

When using the default value of the RandomForestClassifierer from scikit-learn only 10 trees will be used.
This obviously results in quite different accuracies when running the program several times.
The following graph illustrates that the difference for small amounts of trees can be quite big whereas for bigger amounts the accuracy converges to a certain value.

![](plots/different_number_of_trees.jpg?raw=true "Different number of trees")

### Best combination of features

Since it was not feasible for me to test all 255 different combinations, I just tried out different promising combinations.
This did not provide better results than using all features together or features in isolation.


Evaluation
==========

### Learning rate

The following graph shows how much training data the random forest classifierer needs to produce good results.

![](plots/learning_rate.jpg?raw=true "Learning rate")

With few training data the classifier already got good results. The difference between few training data and all training data was small.


### Importance of distance between events

Events in a temporal relation have different distances to each other.
This raises the question whether the distance is an important factor for the correctness of the classifierer.

The following graph shows the ratio between true positives and false positives for changing distances.

![](plots/distance_importance.jpg?raw=true "Distance importance")

### Comparing different features in isolation

![](plots/best_features.jpg?raw=true "Features in isolation")
