from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

from zed_assistant.model.defs import OpenAiModel, ZedAnswer

SETTINGS_FOLDER = config_path = Path.home() / ".zed"
SETTINGS_CONFIG_FILE = SETTINGS_FOLDER / "config"
CONFIG_SEPARATOR = "="


@dataclass
class ZedSettings:
    openai_key: str = ""
    model: OpenAiModel = "gpt-4-turbo"
    debug: bool = False
    yoda_mode: bool = False

    def to_config_file_str(self) -> str:
        return "\n".join([f"{k}{CONFIG_SEPARATOR}{v}" for k, v in asdict(self).items()])


@dataclass
class ZedHistory:
    turn_history: List["ZedTurn"]


@dataclass
class ZedTurn:
    user_query: str
    zed_answer: ZedAnswer
    did_run_command: bool
