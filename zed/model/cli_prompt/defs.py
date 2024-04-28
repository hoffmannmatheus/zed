from dataclasses import asdict, dataclass
from typing import Dict, List, Literal


@dataclass
class CliPromptInput:
    query: str


@dataclass
class CliPromptExchange:
    query: str
    response: str
    was_confirmed: bool


@dataclass
class CliPromptContext:
    history: List[CliPromptExchange]
    user: str
    path: str
    files_in_path: List[str]
