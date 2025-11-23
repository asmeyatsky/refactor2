from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class CloudProvider(Enum):
    AWS = "AWS"
    GCP = "GCP"

class FileType(Enum):
    PYTHON = "python"
    TERRAFORM = "terraform"
    UNKNOWN = "unknown"

@dataclass
class SourceFile:
    path: str
    content: str
    file_type: FileType

@dataclass
class RefactoringResult:
    original_file: SourceFile
    refactored_content: str
    changes_made: List[str]
    confidence_score: float
