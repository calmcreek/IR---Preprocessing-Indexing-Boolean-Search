import subprocess
import sys


def run_program(filename):

    print()
    print("=" * 60)
    print("Running:", filename)
    print("=" * 60)

    result = subprocess.run(
        [
            sys.executable,
            filename
        ]
    )

    if result.returncode != 0:

        print(
            "ERROR:",
            filename,
            "failed."
        )

        sys.exit(
            result.returncode
        )


def main():

    run_program(
        "Group_Blue_preprocess.py"
    )

    run_program(
        "Group_Blue_index.py"
    )

    print()
    print("=" * 60)
    print("PREPROCESSING AND INDEXING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
