from abc import ABC
from dataclasses import asdict, dataclass
from typing import Dict, Literal, Optional

OpenAiModel = Literal["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
DEFAULT_MODEL = "gpt-4o"
"""
The default OpenAI model used by Zed.
"""


@dataclass
class ModelSettings:
    model: str
    max_tokens: int
    temperature: float
    stream: float

    def to_dict(self):
        return asdict(self)


class OpenAIMessage(Dict):
    role: Literal["system", "assistant", "user"]
    content: str


@dataclass
class PromptTemplateValues(ABC):
    def to_dict(self):
        return {k: v for k, v in asdict(self).items()}


@dataclass
class ZedAnswer:
    answer: Optional[str] = None
    command: Optional[str] = None
    needs_confirmation: bool = True
