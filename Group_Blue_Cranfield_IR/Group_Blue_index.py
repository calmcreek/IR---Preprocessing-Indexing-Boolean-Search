from collections import defaultdict


INPUT_FILE = "Group_Blue_processed.all"
OUTPUT_FILE = "Group_Blue_cran.index"


def read_processed_collection(filename):

    index = defaultdict(set)

    current_docid = None
    reading_tokens = False

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            # ---------------------------------------------
            # Document ID
            # ---------------------------------------------
            if line.startswith(".I"):

                parts = line.split()

                current_docid = int(parts[1])

                reading_tokens = False

            # ---------------------------------------------
            # Token section
            # ---------------------------------------------
            elif line == ".S":

                reading_tokens = True

            # ---------------------------------------------
            # Token line
            # ---------------------------------------------
            elif reading_tokens:

                tokens = line.split()

                for token in tokens:

                    index[token].add(
                        current_docid
                    )

    return index


def create_index(
    input_file,
    output_file
):

    index = read_processed_collection(
        input_file
    )

    vocabulary = sorted(
        index.keys()
    )

    if vocabulary:

        maximum_docid = max(
            max(postings)
            for postings in index.values()
        )

    else:

        maximum_docid = 0

    vocabulary_size = len(vocabulary)

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as out:

        # First line:
        # vocabulary size + maximum docid
        out.write(
            f"{vocabulary_size} {maximum_docid}\n"
        )

        # Vocabulary in lexicographical order
        for token in vocabulary:

            postings = sorted(
                index[token]
            )

            posting_list = ",".join(
                str(docid)
                for docid in postings
            )

            out.write(
                f"{token} {posting_list}\n"
            )

    print("========================================")
    print("INDEXING COMPLETE")
    print("========================================")
    print(
        "Vocabulary size:",
        vocabulary_size
    )
    print(
        "Maximum document ID:",
        maximum_docid
    )
    print(
        "Output file:",
        output_file
    )


def main():

    create_index(
        INPUT_FILE,
        OUTPUT_FILE
    )


if __name__ == "__main__":
    main()
