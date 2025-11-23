import os
from typing import List
from cmas.shared.models import SourceFile, FileType

def identify_file_type(filename: str) -> FileType:
    if filename.endswith(".py"):
        return FileType.PYTHON
    elif filename.endswith(".tf"):
        return FileType.TERRAFORM
    else:
        return FileType.UNKNOWN

def ingest_directory(directory_path: str) -> List[SourceFile]:
    """
    Recursively reads a directory and returns a list of SourceFile objects
    for supported file types.
    """
    source_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_type = identify_file_type(file)
            if file_type != FileType.UNKNOWN:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r') as f:
                        content = f.read()
                    source_files.append(SourceFile(path=full_path, content=content, file_type=file_type))
                except Exception as e:
                    print(f"Error reading file {full_path}: {e}")
    return source_files
