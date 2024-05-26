import logging
from typing import List, Optional
from unittest.mock import Mock

import pytest
from openai import AsyncOpenAI

from zed_assistant.model import OpenAIMessage
from zed_assistant.model.command_prompt import (CommandPromptInput,
                                                CommandPromptRunner,
                                                OperatingSystem)
from zed_assistant.model.defs import ZedAnswer

TEST_SYSTEM_TEMPLATE = "OS={{ operating_system }}, yoda_mode={{ yoda_mode }}"


@pytest.fixture
def prompt_runner() -> CommandPromptRunner:
    runner = CommandPromptRunner(
        log=logging.getLogger(__name__),
        client=Mock(AsyncOpenAI),
        model="gpt-4",
    )
    runner.template_system = TEST_SYSTEM_TEMPLATE
    return runner


@pytest.mark.parametrize(
    "prompt_input, expected_messages",
    [
        (
            CommandPromptInput(
                input="ls hidden files",
                operating_system=OperatingSystem.UBUNTU,
                yoda_mode=False,
            ),
            [
                OpenAIMessage(role="system", content="OS=Ubuntu, yoda_mode=False"),
                OpenAIMessage(role="user", content="ls hidden files"),
            ],
        ),
        (
            CommandPromptInput(
                input="write 'zed' in ascii art",
                operating_system=OperatingSystem.MAC_OS,
                yoda_mode=True,
            ),
            [
                OpenAIMessage(role="system", content="OS=Mac OS, yoda_mode=True"),
                OpenAIMessage(role="user", content="write 'zed' in ascii art"),
            ],
        ),
    ],
)
def test_build_messages(
    prompt_input: CommandPromptInput,
    expected_messages: List[OpenAIMessage],
    prompt_runner: CommandPromptRunner,
) -> None:
    messages = prompt_runner._build_prompt_messages(prompt_input=prompt_input)
    assert messages == expected_messages


@pytest.mark.parametrize(
    "result,expected_output",
    [
        (
            "ANSWER this is fine",
            ZedAnswer(answer="this is fine", needs_confirmation=False),
        ),
        (
            "COMMAND ls -lha\nCONFIRM no",
            ZedAnswer(command="ls -lha", needs_confirmation=False),
        ),
        (
            "ANSWER To install the best code editor, run the following\nCOMMAND brew install vim\nCONFIRM yes",
            ZedAnswer(
                answer="To install the best code editor, run the following",
                command="brew install vim",
                needs_confirmation=True,
            ),
        ),
        ("COMMAND missing confirm", None),
        ("ANSWER\nCOMMAND\nCONFIRM", None),
        ("CONFIRM", None),
        ("SOMETHING ELSE", None),
        ("", None),
    ],
)
def test_parse_result(
    result: str,
    expected_output: Optional[ZedAnswer],
    prompt_runner: CommandPromptRunner,
) -> None:
    output = prompt_runner._parse_result(result=result)
    assert output == expected_output
