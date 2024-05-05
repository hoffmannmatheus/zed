import asyncio
import logging
import os
import sys
from argparse import ArgumentParser
from typing import get_args

from openai import AsyncOpenAI

from zed.constants import DEFAULT_MODEL, OpenAiModel
from zed.model.cli_prompt.runner import CliPromptInput, Runner
from zed.utils import Console

logging.basicConfig(stream=sys.stdout)
log = logging.getLogger(__name__)


async def main():
    parser = ArgumentParser(
        description="A friendly LLM command line assistant based on LLMs."
    )
    parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="Enables print debug logs.",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=get_args(OpenAiModel),
        default=DEFAULT_MODEL,
        help=f"The specific Open AI model to be used. Default is '{DEFAULT_MODEL}'.",
    )
    parsed, query_params = parser.parse_known_args()

    console = Console()
    console.show_spinner()

    is_debug: bool = parsed.debug
    model: OpenAiModel = parsed.model

    log.setLevel(logging.DEBUG if is_debug else logging.WARNING)
    log.debug(f'arguments: {is_debug = }, {model =}, {query_params}')

    runner = Runner(
        client=AsyncOpenAI(
            api_key=os.environ.get("ZED_OAI_KEY"),
        ),
        model=model,
    )
    cli_prompt_output = await runner.run_prompt(
        CliPromptInput(
            query=" ".join(query_params),
        ),
    )
    console.hide_spinner()
    log.debug(f'Runner result: {cli_prompt_output = }')

    if not cli_prompt_output:
        console.print_retry()
        return sys.exit(-1)

    if cli_prompt_output.answer:
        console.print_answer(cli_prompt_output.answer)
    if not cli_prompt_output.command:
        return sys.exit(0)

    console.print_command(cli_prompt_output.command)
    confirmed = console.await_confirmation()
    if confirmed:
        log.info(f'RUNNING {cli_prompt_output.command}')
        command_result = os.system(cli_prompt_output.command)
        return sys.exit(command_result)
    else:
        console.print_farewell()
        return sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
