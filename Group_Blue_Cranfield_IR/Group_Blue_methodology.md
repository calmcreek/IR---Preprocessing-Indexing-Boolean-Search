# Group Blue — Methodology
## Information Retrieval: Programming Assignment I
### Preprocessing, Indexing, and Boolean Search on the Cranfield Collection
---
## 1. Overview

This project implements a Boolean retrieval system over the Cranfield collection
(`cran.all.1400`, 1,400 documents). The pipeline has three stages, each implemented
as a standalone Python module and chained together by a driver script:

| Stage | Script | Input | Output |
|---|---|---|---|
| Preprocessing | `Group_Blue_preprocess.py` | `cran.all.1400`, `stopwords.txt` | `Group_Blue_processed.all` |
| Indexing | `Group_Blue_index.py` | `Group_Blue_processed.all` | `Group_Blue_cran.index` |
| Boolean Search | `Group_Blue_boolean_search.py` | `Group_Blue_cran.index`, `stopwords.txt` | `Group_Blue_query_results.txt` |

`Group_Blue_run_all.py` runs the preprocessing and indexing stages back to back.
Only the `.T` (title) and `.W` (abstract) fields of each document are used;
`.A` (author) and `.B` (affiliation) fields are ignored, per the assignment spec.

---

## 2. Parsing the Cranfield Collection

`cran.all.1400` stores all 1,400 documents in a single file, with each document
delimited by SMART-style tags: `.I` (docid), `.T` (title), `.A` (author),
`.B` (affiliation), and `.W` (abstract).

The parser (`process_collection` in `Group_Blue_preprocess.py`) streams the file
line by line and tracks the current section using a simple state variable:

- On `.I`, the previous document (if any) is finalized and a new docid is read.
- On `.T` / `.A` / `.B` / `.W` / `.X`, the state switches to that section.
- Any other line is appended to the `title` buffer or `abstract` buffer
  depending on the current state (author/affiliation lines are read but
  discarded).

Once a document's boundary is reached, its title and abstract text are
concatenated and passed through the four preprocessing functions described
below to produce its final token list.

---

## 3. Preprocessing

Four separate functions are implemented in the `Preprocessor` class, exactly as
required by the assignment, and are applied in this order:

### 3.1 Tokenization (`tokenize`)

Text is split into tokens using the regular expression:

```
[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?
```

This extracts maximal runs of alphanumeric characters, optionally followed by
an apostrophe-joined suffix (so contractions like `don't` survive as a single
token). All other punctuation and whitespace act as token boundaries.

### 3.2 Stemming (`stemming`)

Each token is lowercased and passed through the classic Porter stemming
algorithm (Vivake Gupta's Python port of Martin Porter's original ANSI C
implementation — permitted by the assignment brief as an external Porter
stemmer). This reduces inflected/derived words to a common stem
(e.g. `experimental`, `experiments` → `experi`), which lets the index match
morphological variants of a query term.

### 3.3 Stop Word Removal (`stopword_removal`)

Stemmed tokens are filtered against the supplied `stopwords.txt` list
(loaded once into a set for O(1) lookups). Any token whose lowercased form
appears in the stop word set is discarded.

### 3.4 Normalization (`normalization`)

The remaining tokens are lowercased again and stripped of any leftover
non-alphanumeric characters (e.g. residual apostrophes from contractions) via
`re.sub(r"[^a-z0-9]", "", token)`. Empty strings produced by this step are
dropped.

### 3.5 Output Format

For every document, the pipeline writes:

```
.I <docid>
.S
<space-separated final tokens>
```

to `Group_Blue_processed.all`, matching the `.I` / `.S` tagging required by
the assignment.

---

## 4. Indexing

`Group_Blue_index.py` reads `Group_Blue_processed.all` and builds an inverted
index:

1. **Parsing** — the same `.I` / `.S` structure is streamed; for each token
   under a document's `.S` section, the current docid is added to that
   token's posting set (`defaultdict(set)` avoids duplicate docids for a
   token that appears multiple times in one document).
2. **Sorting** — the vocabulary (dictionary keys) is sorted lexicographically,
   and each token's posting set is sorted in ascending docid order before
   being written out.
3. **Header line** — the first line of `Group_Blue_cran.index` records
   `<vocabulary_size> <maximum_docid>`, as required.
4. **Postings lines** — every subsequent line has the form
   `<token> <docid1>,<docid2>,...,<docidN>`, e.g.:

   ```
   1400 1400
   aerodynamic 1,10,11
   experiment 1,7,9,21,27
   slipstream 1,532
   ```

This gives an O(1)-per-token-occurrence build (amortized dictionary/set
insertion) and an O(V log V) sort at the end, where V is vocabulary size.

---

## 5. Boolean Search

`Group_Blue_boolean_search.py` loads the index file into an in-memory
dictionary (`term → sorted postings list`) once at startup.

### 5.1 Query Normalization

Query terms are put through the *same* normalization + stop word + stemming
pipeline used at index time (`preprocess_query_term`): lowercase, strip
non-alphanumeric characters, drop it if it's a stop word, then stem it. This
guarantees a query term maps to the same vocabulary form used to build the
index — e.g. a query for `experiments` is stemmed to `experi` before lookup,
matching how the corpus was indexed.

### 5.2 Query Format

The parser accepts exactly two terms joined by `AND` or `OR`
(case-insensitive), via the regex:

```
^\s*(\S+)\s+(AND|OR)\s+(\S+)\s*$
```

Malformed queries raise a `ValueError` with a usage message rather than
failing silently.

### 5.3 Efficient Set Operations (bonus)

Because postings lists are stored sorted in the index file, Boolean `AND`
and `OR` are implemented as a **merge-based intersection/union** rather than
a naive nested loop or Python `set()` intersection:

- **`intersection`** — two pointers walk both sorted lists; on a match, the
  docid is emitted and both pointers advance; otherwise the pointer at the
  smaller value advances. This is O(len(list1) + len(list2)) time.
- **`union`** — the same two-pointer merge, emitting the smaller (or equal)
  element at each step and appending any remaining tail from either list.
  Also O(len(list1) + len(list2)).

This avoids the O(n·m) cost of a naive intersection and avoids the overhead
of converting lists to hash sets, while still guaranteeing sorted, duplicate-free
output.

### 5.4 Interactive Mode

Running the script starts an interactive prompt (`Query: `) that accepts
queries until `EXIT` is typed. Each query's result — including empty results
— is written to `Group_Blue_query_results.txt` as:

```
Query: <original query>
DocIDs: <comma-separated sorted docids>
```

---

## 6. Test Queries

`Group_Blue_test_queries.txt` contains the following sample queries, covering
both operators and a mix of common/rarer terms:

```
aerodynamic AND experimental
aerodynamic OR experimental
wing AND flow
pressure AND velocity
turbulence OR boundary
```

Results for the executed queries are recorded in
`Group_Blue_query_results.txt`.

---

## 7. How to Run

```bash
# 1. Preprocess + build the index in one step
python Group_Blue_run_all.py

# 2. Run Boolean search interactively
python Group_Blue_boolean_search.py
# Query: aerodynamic AND experimental
# Query: EXIT
```

Requires Python 3.8+ (see `requirements.txt`). No third-party IR library or
package is used anywhere in the pipeline; the only external code reused is
the Porter stemmer implementation, as explicitly permitted by the assignment.

---

## 8. File Naming

All deliverables are prefixed with `Group_Blue_`, as required:

- `Group_Blue_preprocess.py`, `Group_Blue_porter_stemmer.py`,
  `Group_Blue_index.py`, `Group_Blue_boolean_search.py`,
  `Group_Blue_run_all.py`
- `Group_Blue_processed.all` (preprocessed collection)
- `Group_Blue_cran.index` (index file)
- `Group_Blue_test_queries.txt`, `Group_Blue_query_results.txt`
- `Group_Blue_README.md`, `Group_Blue_methodology.md` (this document)
