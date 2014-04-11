Learning-of-Event-Timelines
===========================

This is a university project about supervised learning of event timelines.

## Task
The goal of this project was to build a system capable of identifying temporal links between given events.

The task included the extraction of events and temporal links from a given data, deriving useful features from those events and temporal links to then train and test a random forest classifier on the extracted data.

## Dataset
The dataset given for this project contained annotated events and temporal links between those events.  
The dataset can be found in this repository under fables-100-temporal-dependency.xml or here: http://www.cis.uab.edu/bethard/data/fables-100-temporal-dependency.xml

There are several different annotated temporal relations between events in the dataset nameley SAME_AS, OVERLAP, BEFORE, AFTER, INCLUDES, CONTAINS, IS_INCLUDED, IS_CONTAINED_IN, NO_RELATIONS.  
The task however was to only train the classifier on three specific temporal links: BEFORE, IS_INCLUDED and INCLUDES.  

### Distribution of temporal relations in dataset (looking only at relations annotators had in common)
- All: 720
- SAME_AS: 14
- OVERLAP: 26
- AFTER: 27
- IS_CONTAINED_IN: 2
- BEFORE :514
- CONTAINS: 9
- INCLUDES: 102
- IS_INCLUDED: 26
- NO_RELATIONS: 0

### Distribution of temporal relations in dataset (looking at all relations)
- All: 1463
- SAME_AS: 47
- OVERLAP: 18
- AFTER: 71
- IS_CONTAINED_IN: 24
- BEFORE : 880
- CONTAINS: 47
- INCLUDES: 270
- IS_INCLUDED: 105
- NO_RELATIONS: 1

I used the AFTER relation as an inversed BEFORE, the CONTAINS relation as an inversed INCLUDES and the IS_CONTAINED_IN as a reversed IS_INCLUDED relation.
This resulted in more data  and a better result for the BEFORE and INCLUDES classes.  
The performance of the IS_INCLUDED class stayed about the same. The results for the NONE class became worse which makes sense since IS_CONTAINED_IN, CONTAINS and AFTER were not named as NONE anymore which resulted in less NONE data.

## Basic overview of code
### main.py

Used to test out different settings.  
Also prints out the predicted and true y values.  
Should be called like this _./main.py --reload_ when the features were changed.


### train.py

Provides functions to parse the dataset, divide it into training and test set and to execute the classification with the best settings I could figure out.


### evaluation.py

This was used to do the evaluation and error analysis.
All plots were generated directly from evaluation.py.


## overview.py

I used overview.py to get an overview of the sentences and their temporal relations as well as the resulting features.  
This was useful to check if the feature extraction was working the way it should work.

### test.py

Runs tests on text processing methods needed for feature extraction and other feature related methods like tense and aspect guessing.


### parser.py

Parses the relations and events from the XML file into memory and into a convenient data structure.
