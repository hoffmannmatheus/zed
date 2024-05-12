from dataclasses import dataclass
from enum import Enum
from typing import Optional

from zed_assistant.model.defs import PromptTemplateValues


class CliCommandType(str, Enum):
    COMMAND = "COMMAND"
    CONFIRM = "CONFIRM"
    ANSWER = "ANSWER"


class OperatingSystem(str, Enum):
    MAC_OS = "Mac OS"
    UBUNTU = "Ubuntu"
    ARCH = "Arch Linux"


##
# Cli prompt runner input and output
##


@dataclass
class CliPromptInput:
    input: str
    operating_system: OperatingSystem


@dataclass
class CliPromptOutput:
    answer: Optional[str] = None
    command: Optional[str] = None
    needs_confirmation: bool = True


##
# Cli prompt template values
##


@dataclass
class SystemTemplateValues(PromptTemplateValues):
    operating_system: str
    yoda_mode: bool
