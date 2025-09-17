"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os
import string
import time
from itertools import groupby
from operator import itemgetter

from toolz.itertoolz import concat


def copy_raw_files_to_input_folder(n):
    """Generate n copies of the raw files in the input folder"""

    create_directory("files/input")

    for file in glob.glob("files/raw/*"):

        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        for i in range(1, n + 1):
            filename = f"{os.path.basename(file).split('.')[0]}_{i}.txt"
            with open(f"files/input/{filename}", "w", encoding="utf-8") as f2:
                f2.write(text)


def load_input(input_directory):
    """Load files into sequence of (filename, line)"""

    sequence = []
    files = glob.glob(f"{input_directory}/*")
    with fileinput.input(files=files) as f:
        for line in f:
            sequence.append((fileinput.filename(), line))
    return sequence


def preprocess_line(x):
    """Preprocess the line x"""
    text = x[1]
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return (x[0], text.strip())


def map_line(x):
    """Map line -> list of (word,1)"""
    _, clean_line = preprocess_line(x)
    return [(w, 1) for w in clean_line.split() if w]


def mapper(sequence):
    """Mapper"""
    return concat(map(map_line, sequence))


def shuffle_and_sort(sequence):
    """Shuffle and Sort by key (word)"""
    sorted_seq = sorted(sequence, key=itemgetter(0))
    return [(key, list(group)) for key, group in groupby(sorted_seq, key=itemgetter(0))]


def compute_sum_by_group(group):
    """Compute sum of counts in group"""
    key, values = group
    total = sum(v for _, v in values)
    return key, total


def reducer(sequence):
    """Reducer"""
    return list(map(compute_sum_by_group, sequence))


def create_directory(directory):
    """Create Output Directory"""

    if os.path.exists(directory):
        for file in glob.glob(f"{directory}/*"):
            os.remove(file)
        os.rmdir(directory)

    os.makedirs(directory)


def save_output(output_directory, sequence):
    """Save Output"""
    output_file = os.path.join(output_directory, "part-00000")
    with open(output_file, "w", encoding="utf-8") as f:
        for word, count in sorted(sequence):
            f.write(f"{word}\t{count}\n")


def create_marker(output_directory):
    """Create Marker"""
    marker_file = os.path.join(output_directory, "_SUCCESS")
    with open(marker_file, "w", encoding="utf-8") as f:
        f.write("Marcador de éxito")


def run_job(input_directory, output_directory):
    """Job"""
    sequence = load_input(input_directory)
    sequence = mapper(sequence)
    sequence = shuffle_and_sort(sequence)
    sequence = reducer(sequence)
    create_directory(output_directory)
    save_output(output_directory, sequence)
    create_marker(output_directory)


if __name__ == "__main__":

    copy_raw_files_to_input_folder(n=1000)

    start_time = time.time()

    run_job(
        "files/input",
        "files/output",
    )

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
