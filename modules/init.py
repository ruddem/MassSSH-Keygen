from pathlib import Path


def make_dirs(generated_files_location):
    Path(generated_files_location).mkdir(parents=True, exist_ok=True)