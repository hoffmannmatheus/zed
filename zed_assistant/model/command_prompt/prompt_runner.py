from logging import Logger
from typing import List, Optional

from jinja2 import Template
from openai import AsyncOpenAI

from zed_assistant.model.defs import (
    ModelSettings,
    OpenAIMessage,
    OpenAiModel,
    ZedAnswer,
)
from zed_assistant.utils.file_utils import read_file_contents

from .defs import CliCommandType, CommandPromptInput, SystemTemplateValues


class CommandPromptRunner:
    def __init__(
        self,
        log: Logger,
        client: AsyncOpenAI,
        model: OpenAiModel,
    ):
        self.log = log
        self.client = client
        self.template_system = read_file_contents(
            folder_path=__file__,
            file_name="template_system.j2",
        )
        self.model_settings = ModelSettings(
            model=model,
            max_tokens=64,
            temperature=0.0,
            stream=False,
        )

    async def run_prompt(self, prompt_input: CommandPromptInput) -> Optional[ZedAnswer]:
        self.log.debug(f"Calling OpenAI with args {self.model_settings.to_dict()}")
        result = await self.client.chat.completions.create(
            **self.model_settings.to_dict(),
            messages=self._build_prompt_messages(prompt_input=prompt_input),
        )

        self.log.debug(f"Full OAI {result = }")
        if result.usage:
            # TODO log usage.prompt_tokens and usage.completition_tokens
            ...
        choices = result.choices
        if not choices or not choices[0].message or not choices[0].message.content:
            self.log.warning(f"Warning: bad OpenAI result: {result}")
            return None

        return self._parse_result(result=result.choices[0].message.content)

    def _build_prompt_messages(
        self, prompt_input: CommandPromptInput
    ) -> List[OpenAIMessage]:
        system_template_values = SystemTemplateValues(
            operating_system=prompt_input.operating_system.value,
            yoda_mode=prompt_input.yoda_mode,
        ).to_dict()
        rendered_system_prompt = Template(self.template_system).render(
            system_template_values
        )
        self.log.debug(f"{system_template_values = } {rendered_system_prompt = }")
        return [
            # TODO add previous assistant and user exchanges for?
            OpenAIMessage(role="system", content=rendered_system_prompt),
            OpenAIMessage(role="user", content=prompt_input.input),
        ]

    def _parse_result(self, result: Optional[str]) -> Optional[ZedAnswer]:
        if not result:
            return None
        result_by_line = result.split("\n")
        self.log.debug(f"_parse_result(): {result_by_line = }")
        answer: Optional[str] = None
        command: Optional[str] = None
        included_confirm = False
        needs_confirmation = False

        for line in result_by_line:
            if line.startswith(CliCommandType.ANSWER):
                answer = line[len(CliCommandType.ANSWER.value) :].strip()
            elif line.startswith(CliCommandType.COMMAND):
                command = line[len(CliCommandType.COMMAND.value) :].strip()
            elif line.startswith(CliCommandType.CONFIRM):
                confirm = line[len(CliCommandType.COMMAND.value) :].strip()
                included_confirm = True
                needs_confirmation = confirm == "yes"

        if not answer and not command:
            return None
        if command and not included_confirm:
            self.log.warning(
                "Error! Answer included a COMMAND, but no CONFIRM instruction"
            )
            return None
        return ZedAnswer(
            answer=answer,
            command=command,
            needs_confirmation=needs_confirmation,
        )
