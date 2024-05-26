from dataclasses import dataclass
from enum import Enum

from zed_assistant.model.defs import PromptTemplateValues


class CliCommandType(str, Enum):
    COMMAND = "COMMAND"
    CONFIRM = "CONFIRM"
    ANSWER = "ANSWER"


class OperatingSystem(str, Enum):
    MAC_OS = "Mac OS"
    UBUNTU = "Ubuntu"


@dataclass
class CommandPromptInput:
    input: str
    yoda_mode: bool
    operating_system: OperatingSystem


@dataclass
class SystemTemplateValues(PromptTemplateValues):
    operating_system: str
    yoda_mode: bool
