import logging
from typing import Optional
from unittest.mock import Mock

import pytest
from openai import AsyncOpenAI
from zed_assistant.model.command_prompt import CliPromptOutput, CommandPromptRunner


@pytest.fixture
def runner() -> CommandPromptRunner:
    return CommandPromptRunner(
        log=logging.getLogger(__name__),
        client=Mock(AsyncOpenAI),
        model="gpt-4",
    )


@pytest.mark.parametrize(
    "result,expected_output",
    [
        (
            "ANSWER this is fine",
            CliPromptOutput(answer="this is fine", needs_confirmation=False),
        ),
        (
            "COMMAND ls -lha\nCONFIRM no",
            CliPromptOutput(command="ls -lha", needs_confirmation=False),
        ),
        (
            "ANSWER To install the best code editor, run the following\nCOMMAND brew install vim\nCONFIRM yes",
            CliPromptOutput(
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
def test_parse_prompt_result(
    result: str,
    expected_output: Optional[CliPromptOutput],
    runner: CommandPromptRunner,
) -> None:
    output = runner._parse_result(result=result)
    assert output == expected_output
