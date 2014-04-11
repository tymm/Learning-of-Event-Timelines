Learning-of-Event-Timelines
===========================

This is a university project about supervised learning of event timelines.

## Task
The goal of this project was to build a system capable of identifying temporal links between given events.

The task included the extraction of events and temporal links from a given data, deriving useful features from those events and temporal links to then train and test a random forest classifier on the extracted data.

I worked on this project between mid-november 2013 until the 11th of april 2014 with interrupts.

## Papers
There are a lot of scientific papers on the topic of temporal relation identification in texts.
I mainly used the following papers to learn about the topic:
- Bethard, Steven. 2013. Cleartk-timeml: A minimalist approach to tempeval 2013
- Bethard, Steven, Kolomiyets, Oleksandr, Moens, Marie-Francine. 2012. Annotating story timelines as temporal dependency structures.
- Chambers, Naathanael. 2013. Navytime: Event and time ordering from raw text.
- UzZaman, Naushad, Llorens, Hector, Allen, James, Derczynski, Leon, Verhagen, Marc, Pustejovsky, James. 2013. Tempeval-3: Evaluating events, time expressions, and temporal relations.

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

### Used features
- Aspect (None, Progressive, Perfect, Perfect Progressive)
- Tense (None, Present, Past, Future)
- Distance between events (in words)
- Wordnet similarity of events (NLTK's WordNet)
- Grammatical polarity
- Grammatical modality
- Word stem
- Part of Speech (event and one word before and after event)

### Problems I encountered
- There was not enough data to get good results for all four temporal relations
- It was not feasible for me to produce plots with averaged results since it just would take too much time to produce these results on my computer. Also the whole evaluation was quite time consuming in general because of that.
- Due to a bug which resulted in loading the same results over and over regardless of the configuration, the first version of the evaluation was useless.

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


### overview.py

I used overview.py to get an overview of the sentences and their temporal relations as well as the resulting features.  
This was useful to check if the feature extraction was working the way it should work.

### test.py

Runs tests on text processing methods needed for feature extraction and other feature related methods like tense and aspect guessing.


### parser.py

Parses the relations and events from the XML file into memory and into a convenient data structure.
