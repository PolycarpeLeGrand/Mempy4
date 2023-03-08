Mempy 4
=======

The project is split into two subpackages:

* mempy4 contains all project specific files
* mempyapi contains higher level scripts meant to be reusable on similar projects

This design is meant to both help keep the code base cleaner and improve reusability. The API part is, as the name 
suggests, meant to be usable as a project agnostic interface to run different types of analysis. So far, the following 
analysis are supported (see the 'mempyapi package' section for more details): 

* Document filtering [`docfilter`]: Helps filtering documents based an arbitrary number of custom conditions, to create 
    a list of allowed documents from a corpus. Multiple filters can be created and saved in order to be reusable.
* Tag Counts [`tagcounts`]: Count occurrences in a list of tags (typically word-pos-lemma). Tracks both the total number 
    of occurrences across the corpus and the number of documents with at least an instance of each value. Can be set to 
    work on any of the tag attributes and keep track of a secondary attribute (e.g. Track individual words and keep 
    track of their different POS values or track lemmas and track the different words associated with each lemma).
* Document Term [`docterm`]: Tool to build document-terms matrices from the corpus.
* Lexical Categories [`lexcats`]: Builds matrices similar to document-terms, but based on a specified lexicon. Groups 
    values of words belogning to the same lexical group.
* LDA topic modeling [`ldatopics`]: Wraps scikitlearn's LDA implementation to make it easier to track parameters and 
    reuse models.
* Cooccurrences [`coocs`]: Handles cooccurrence analysis. From a given list of words, can both track cooccurrence 
    statistics for each one, as well as the text references for cooccurrences between words of the list.

The mempy4 package handles the project-specific stuff, both the preprocessing and the analysis. The base structure 
across the project are DocModel objects, which contain all document-specific data, from the raw XML to the metadata and 
tagged text. DocModels are stored as pickle files and iterated through with generators (this would probably be better 
handled by a database, but here we are ¯\_(ツ)_/¯).

Different scripts handle the running of each analysis. The workflow is meant to be modular, with data saved at different 
points during the pipeline. Analysis can thus be tweaked and run again with minimal preprocessing overhead. The goal is 
to reduce processing time at the expense of storage space. Final results are typically presented as pandas DataFrame, 
but the raw data is always available. 

mempy4 package
--------------

Built around docmodels, stored as pickles.

#### Project structure

Data storage

Running

#### Running analysis

execs: run models, counters, etc. Store the models or objects themselves, not the representations.
results: produce and format result files (dataframes, etc.)


mempyapi package
----------------

Project-agnostic api implementing various nlp algorithms. Does not rely on the DocModel structure used by the mempy4 
project; all inputs are standard data types.

Was only tested with Treetagger, but other similar libraries should work fine (with some minor tweaks).

