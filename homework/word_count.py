"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os.path
import time
from itertools import groupby

from toolz.itertoolz import concat, pluck


def copy_raw_files_to_input_folder(n: int):
    """Generate n copies of the raw files in the input folder"""
    raw_folder = "files/raw"
    input_folder = "files/input"

    # Crear la carpeta input si no existe
    os.makedirs(input_folder, exist_ok=True)

    # Recorrer cada archivo en la carpeta raw
    for filename in os.listdir(raw_folder):
        file_path = os.path.join(raw_folder, filename)

        if os.path.isfile(file_path):
            # Crear n copias
            for i in range(n):
                # Generar un nombre de archivo con sufijo copy{i}
                new_filename = f"{os.path.splitext(filename)[0]}_copy{i}{os.path.splitext(filename)[1]}"
                new_file_path = os.path.join(input_folder, new_filename)

                # Copiar el archivo
                shutil.copy(file_path, new_file_path)
    # Crear carpeta destino si no existe
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)

    raw_files = glob.glob(os.path.join(raw_dir, "*.txt"))

    if not raw_files:
        print("No se encontraron archivos en", raw_dir)
        return

    for i in range(n):
        for file in raw_files:
            filename = os.path.basename(file)
            name, ext = os.path.splitext(filename)

            # Ejemplo: file1_copy0.txt, file1_copy1.txt...
            new_filename = f"{name}_copy{i}{ext}"
            new_path = os.path.join(input_dir, new_filename)

            shutil.copy(file, new_path)
            print(f"Copiado: {file} -> {new_path}")

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
