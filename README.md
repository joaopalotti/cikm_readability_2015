## Source Code and data used for CIKM Readability 2015 short paper
[TODO: insert here link to paper]

### Dependences

The code used in this work takes advantage of the [ReadabilityCalculator python module](https://github.com/joaopalotti/readability_calculator), that can be downloaded using pip:
```
$ pip install ReadabilityCalculator
```
---------------

### Data:

#### readability_scores*.tar.gz
It contains the readability scores for every document from CLEF eHealth 2014/2015 dataset.

#### distrib.tar.gz
It contains the distribution of words and sentences for each preprocessing variant for the documents in CLEF eHealth 2014/2015 dataset.

#### lucene_html.out
It is the lucene result list based on a default VSM search using the topics from CLEF eHealth 2014.

---------------

### Code:

#### check_num_words.py
Script that creates table 2 from the paper.

#### unpack_dat.py
Script to unpack the original '.dat' files from CLEF and preprocess them using any of the boilerplate removal options.

#### calculate_readability.py
Python script used to create the files in readability_score.tar.gz

#### correlations.py
Calculates the correlations between the ranking list generated by different readability measure for the same Lucene based initial ranked list.

