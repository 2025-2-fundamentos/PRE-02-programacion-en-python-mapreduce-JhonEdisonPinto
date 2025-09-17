"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os.path
import time
import shutil

from itertools import groupby

from itertools import chain
from operator import itemgetter

concat = chain.from_iterable
pluck = lambda i, seq: map(itemgetter(i), seq)


def copy_raw_files_to_input_folder(n=1000, input_folder="files/input", raw_folder="files/raw"):
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    raw_files = os.listdir(raw_folder)[:n]
    for file_name in raw_files:
        file_path = os.path.join(raw_folder, file_name)
        new_file_path = os.path.join(input_folder, file_name)
        shutil.copy(file_path, new_file_path)

def load_input(input_directory):
    """Funcion load_input"""

    lines = []
    for filename in os.listdir(input_directory):
        if filename.endswith(".txt"):
            with open(os.path.join(input_directory, filename), "r", encoding="utf-8") as f:
                    lines.extend(f.readlines())
    return lines
def preprocess_line(x):
    """Preprocess the line x"""
    x = x.lower()
    x = re.sub(r"[^a-záéíóúüñ0-9\s]", "", x)
    return x.strip()

def map_line(x):
    """pass"""
    words = x.split()
    return [(w, 1) for w in words]
def mapper(sequence):
    """Mapper"""
    return list(concat(map(map_line, sequence)))

def shuffle_and_sort(sequence):
    """Shuffle and Sort"""

    sequence = sorted(sequence, key=lambda x: x[0])
    grouped = groupby(sequence, key=lambda x: x[0])
    return [(word, list(pluck(1, group))) for word, group in grouped]

def compute_sum_by_group(group):
    """pass"""
    word, values = group
    return (word, sum(values))
def reducer(sequence):
    """Reducer"""

    return [compute_sum_by_group(g) for g in sequence]

def create_directory(directory):
    """Create Output Directory"""

    if not os.path.exists(directory):
        os.makedirs(directory)
def save_output(output_directory, sequence):
    """Save Output"""
    output_file = os.path.join(output_directory, "word_count.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        for word, count in sequence:
         f.write(f"{word}: {count}\n")
    print(f"Resultados guardados en {output_file}")

def create_marker(output_directory):
    """Create Marker"""
    marker_file = os.path.join(output_directory, "_SUCCESS")
    with open(marker_file, "w", encoding="utf-8") as f:
        f.write("Job completed successfully\n")
    print(f"Marcador creado en {marker_file}")

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
