Error analysis
==============

### All relations vs. all relations in common

The provided XML file consists of annotated events and relations of events.
Those events and relations got annotated by more than one annotator and different people annotated different events and relations.

Therefore it was reasonable to check for which case the accuracy of the classification on the test set was higher.
It turned out that there is no noticeable difference in accuracy.


### Different number of trees in the random forest

When using the default value of the RandomForestClassifierer from scikit-learn only 10 trees will be used.
This obviously results in quite different accuracies when running the program several times.
The following graph shows how the number of trees on average have an influence on the accuracy.


We can see that there are big differences for small amounts of trees which then converge to a certain accuracy value for larger numbers of trees.

### Best combination of features

Since it was not feasible for me to test all 255 different combinations, I just tried out to use the two best performing features (tense and aspect, see 'Comparing the different features in isolation') together.
This did not provide better results than using all features together or features in isolation.

Evaluation
==========

### Learning rate

The following graph shows how much training data the random forest classifierer needs to produce good results.


With few training data we already get good results. The difference between few training data and all training data is just 0.025.


### Importance of distance between events

Events in a temporal relation have different distances to each other.
This raises the question whether the distance is an important factor for the correctness of the classifierer.

The following graph shows the ratio between true positives and false positives for changing distances.

![](plots/distance_importance.jpg?raw=true "Distance importance")

### Comparing the different features in isolation
