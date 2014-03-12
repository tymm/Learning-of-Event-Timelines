Learning-of-Event-Timelines
===========================

This is a university project about supervised learning of event timelines.

The goal of this project was to build a system capable of identifying temporal links between given events.

The data set given for this project contained annotated events and temporal links between those events.  
The data set can be found in this repository under fables-100-temporal-dependency.xml or here: http://www.cis.uab.edu/bethard/data/fables-100-temporal-dependency.xml

The task included the extraction of events and temporal links from the given data, deriving useful features from those events and temporal links to then train and test a random forest classifier on the extracted data.

There are several different annotated time relations between events in the data set. The task however was to only train the classifier on three specific temporal links: BEFORE, IS_INCLUDED and INCLUDES.


train.py
--------

Parses the dataset, divides it into training and test set and executes the classification with the best settings I could figure out.


evaluation.py
-------------

This was used to do the evaluation and error analysis.


test.py
-------

Runs tests on text processing methods needed for feature extraction and other feature related methods like tense and aspect guessing.


parser.py
---------

Parses the relations and events from the XML file into memory and into a convenient data structure.
