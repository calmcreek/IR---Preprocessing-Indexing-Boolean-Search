import re

from Group_Blue_porter_stemmer import PorterStemmer


INDEX_FILE = "Group_Blue_cran.index"
STOPWORD_FILE = "stopwords.txt"
OUTPUT_FILE = "Group_Blue_query_results.txt"


class BooleanSearcher:

    def __init__(
        self,
        index_file,
        stopword_file
    ):

        self.index = {}

        self.stopwords = (
            self.load_stopwords(
                stopword_file
            )
        )

        self.stemmer = PorterStemmer()

        self.vocabulary_size = 0
        self.maximum_docid = 0

        self.load_index(index_file)

    # =========================================================
    # LOAD STOP WORDS
    # =========================================================
    def load_stopwords(self, filename):

        stopwords = set()

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as f:

            for line in f:

                word = line.strip().lower()

                if word:
                    stopwords.add(word)

        return stopwords

    # =========================================================
    # LOAD INDEX
    # =========================================================
    def load_index(self, filename):

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as f:

            first_line = f.readline().strip()

            if not first_line:
                return

            header = first_line.split()

            self.vocabulary_size = int(
                header[0]
            )

            self.maximum_docid = int(
                header[1]
            )

            for line in f:

                line = line.strip()

                if not line:
                    continue

                parts = line.split(
                    maxsplit=1
                )

                if len(parts) != 2:
                    continue

                term = parts[0]

                posting_string = parts[1]

                postings = []

                for docid in posting_string.split(","):

                    docid = docid.strip()

                    if docid:
                        postings.append(
                            int(docid)
                        )

                self.index[term] = postings

    # =========================================================
    # NORMALIZATION
    # =========================================================
    def normalize(self, word):

        word = word.lower()

        word = word.replace(
            "'",
            ""
        )

        word = re.sub(
            r"[^a-z0-9]",
            "",
            word
        )

        return word

    # =========================================================
    # QUERY TERM PREPROCESSING
    # =========================================================
    def preprocess_query_term(self, term):

        term = self.normalize(term)

        if not term:
            return None

        if term in self.stopwords:
            return None

        term = self.stemmer.stem(
            term
        )

        return term

    # =========================================================
    # GET POSTINGS
    # =========================================================
    def get_postings(self, term):

        term = self.preprocess_query_term(
            term
        )

        if term is None:
            return []

        return self.index.get(
            term,
            []
        )

    # =========================================================
    # AND
    # =========================================================
    def intersection(
        self,
        list1,
        list2
    ):

        result = []

        i = 0
        j = 0

        while (
            i < len(list1)
            and j < len(list2)
        ):

            if list1[i] == list2[j]:

                result.append(
                    list1[i]
                )

                i += 1
                j += 1

            elif list1[i] < list2[j]:

                i += 1

            else:

                j += 1

        return result

    # =========================================================
    # OR
    # =========================================================
    def union(
        self,
        list1,
        list2
    ):

        result = []

        i = 0
        j = 0

        while (
            i < len(list1)
            and j < len(list2)
        ):

            if list1[i] == list2[j]:

                result.append(
                    list1[i]
                )

                i += 1
                j += 1

            elif list1[i] < list2[j]:

                result.append(
                    list1[i]
                )

                i += 1

            else:

                result.append(
                    list2[j]
                )

                j += 1

        while i < len(list1):

            result.append(
                list1[i]
            )

            i += 1

        while j < len(list2):

            result.append(
                list2[j]
            )

            j += 1

        return result

    # =========================================================
    # SEARCH
    # =========================================================
    def search(self, query):

        pattern = (
            r"^\s*(\S+)\s+"
            r"(AND|OR)\s+"
            r"(\S+)\s*$"
        )

        match = re.match(
            pattern,
            query,
            re.IGNORECASE
        )

        if not match:

            raise ValueError(
                "Query must have the form: "
                "word AND word "
                "or "
                "word OR word"
            )

        word1 = match.group(1)

        operator = match.group(2).upper()

        word2 = match.group(3)

        postings1 = self.get_postings(
            word1
        )

        postings2 = self.get_postings(
            word2
        )

        if operator == "AND":

            return self.intersection(
                postings1,
                postings2
            )

        return self.union(
            postings1,
            postings2
        )

    # =========================================================
    # INTERACTIVE SEARCH
    # =========================================================
    def interactive(self):

        print()
        print("========================================")
        print("GROUP BLUE BOOLEAN SEARCH")
        print("========================================")
        print(
            "Vocabulary size:",
            self.vocabulary_size
        )
        print(
            "Maximum docid:",
            self.maximum_docid
        )
        print()
        print("Examples:")
        print("  aerodynamic AND experimental")
        print("  aerodynamic OR experimental")
        print()
        print("Type EXIT to stop.")
        print()

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as out:

            while True:

                query = input(
                    "Query: "
                ).strip()

                if query.upper() == "EXIT":
                    break

                try:

                    results = self.search(
                        query
                    )

                    print(
                        "Result:",
                        results
                    )

                    out.write(
                        f"Query: {query}\n"
                    )

                    out.write(
                        "DocIDs: "
                        + ",".join(
                            map(
                                str,
                                results
                            )
                        )
                        + "\n\n"
                    )

                except ValueError as error:

                    print(
                        "ERROR:",
                        error
                    )


def main():

    searcher = BooleanSearcher(
        INDEX_FILE,
        STOPWORD_FILE
    )

    searcher.interactive()


if __name__ == "__main__":
    main()
