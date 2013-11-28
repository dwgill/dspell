dspell
======

dspell is a rudimentary spell checker written in python as an 
educational exercise in natural language processing. It's only 
dependency is the [nltk][]. It can be run by executing any of 
the following from the dspell/ directory:

    ./sp_correct.py str "your string to correct"
    ./sp_correct.py file /path/to/your/file
    ./sp_correct.py dir /path/to/your/dir

Due to the slow speed of the algorithm, running dspell on data 
of size beyond single sentences is not recommended.

[nltk]: http://nltk.org/
