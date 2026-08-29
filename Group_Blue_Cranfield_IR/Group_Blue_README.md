# Group Blue - Cranfield Boolean Information Retrieval System
Run it: cd Group_Blue_Cranfield_IR 
        python3 Group_Blue_porter_stemmer.py  (words being converted to stems)
        python3 Group_Blue_preprocess.py ( Expected: 1400)
        python3 Group_Blue_index.py
        python3 Group_Blue_boolean_search.py
        or
        python3 Group_Blue_run_all.py
        python3 Group_Blue_boolean_search.py


# 1. Assignment

Cranfield Collection Preprocessing, Indexing and Boolean Retrieval

# 2. Group

Group Blue

# 3. Programming Language

Python 3

# 4. Objective

The objective of this project is to implement a basic Boolean information retrieval system for the Cranfield collection containing 1400 scientific documents.

# The system performs:

Tokenization
Stemming
Stop-word removal
Normalization
Inverted index construction
Boolean retrieval using AND and OR

The implementation does not use an information retrieval library. The indexing and Boolean retrieval algorithms are implemented from scratch.

# 5. Input Collection

The input collection is:

cran.all

The Cranfield collection contains document identifiers, titles, author information and abstracts.

Only the following fields are processed:

.T - title
.W - abstract

The author and affiliation fields are ignored.

# 6. Preprocessing

The preprocessing program contains four separate functions:

Tokenization

The document text is divided into individual token strings.

Stemming

Tokens are converted to word stems using the Porter stemming algorithm.

Stop-word Removal

Common English stop words are removed using:

stopwords.txt

Normalization

Tokens are converted to lowercase and punctuation/non-alphanumeric characters are removed.

The same preprocessing logic is applied to Boolean query terms.

# 7. Porter Stemmer

A standalone Python implementation of the Porter stemming algorithm is included in:

Group_Blue_porter_stemmer.py

The assignment explicitly permits the use of a Porter stemmer from an external source.

The implementation is based on the standard Porter stemming algorithm originally described by Martin Porter.

Source:

Martin Porter, "An algorithm for suffix stripping", Program, Vol. 14, No. 3, 1980.

The Porter implementation used in this project is acknowledged rather than claimed as original group code.

# 8. Processed Collection

The preprocessing program creates:

Group_Blue_processed.all

The output uses:

.I

for document identifiers and:

.S

for processed tokens.

Example:

.I 1
.S
aerodynam flow pressur calcul

# 9. Inverted Index

The indexing program creates:

Group_Blue_cran.index

The first line contains:

vocabulary_size maximum_docid


For example:

588 1400


Each subsequent line contains a token and its posting list.

Example:

aerodynam 1,10,11
experiment 1,7,9,21,27
slipstream 1,532


The vocabulary is sorted lexicographically.

Posting lists are sorted by ascending document ID.

# 10. Boolean Search

The Boolean search program supports queries containing two query words and one logical operator.

Supported operators:

AND
OR

Examples:

aerodynamic AND experimental


and:

aerodynamic OR experimental


The query words are normalized and stemmed before the corresponding posting lists are retrieved.

# 11. Efficient Searching

For AND queries, a two-pointer intersection algorithm is used.

For OR queries, a two-pointer merge algorithm is used.

Because posting lists are sorted, the algorithms avoid scanning all 1400 documents for every query.

For posting lists A and B, the operations take:

O(|A| + |B|)


time.

# 12. Program Files
File	Description
cran.all	Original Cranfield collection
stopwords.txt	English stop-word list
Group_Blue_porter_stemmer.py	Porter stemming implementation
Group_Blue_preprocess.py	Document preprocessing
Group_Blue_index.py	Inverted index construction
Group_Blue_boolean_search.py	Boolean retrieval
Group_Blue_run_all.py	Runs preprocessing and indexing
Group_Blue_processed.all	Preprocessed collection
Group_Blue_cran.index	Final inverted index
Group_Blue_test_queries.txt	Test Boolean queries
Group_Blue_query_results.txt	Query results
Group_Blue_methodology.md	Methodology/write-up
requirements.txt	Environment information
# 13. Execution

From the project directory:

python3 Group_Blue_preprocess.py


Then:

python3 Group_Blue_index.py


Then:

python3 Group_Blue_boolean_search.py


Alternatively:

python3 Group_Blue_run_all.py


runs preprocessing and indexing.

# 14. Boolean Search Output

The Boolean search program writes results to:

Group_Blue_query_results.txt

Each query is followed by its matching document IDs.

# 15. Restrictions

No information retrieval library is used.

The inverted index is constructed manually.

Boolean AND and OR operations are implemented manually.

The Porter stemming algorithm is used as permitted by the assignment.

# 16. Testing

The system should be tested using Boolean queries supplied by the instructor.

The output document IDs should be checked to ensure that:

AND returns documents containing both terms.
OR returns documents containing either term.
Document IDs are sorted.
Query terms undergo the required preprocessing.
Searching is performed using the index rather than directly scanning the collection.


