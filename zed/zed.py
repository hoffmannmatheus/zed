from logging import Logger
import os

from openai import AsyncOpenAI

from .constants import OpenAiModel
from .model.cli_prompt import Runner, CliPromptInput
from .utils import Console


async def run(log: Logger, oai_key: str, model: OpenAiModel, user_query: str) -> bool:
    """
    Main Zed executor.
    """
    console = Console()
    console.show_spinner()

    runner = Runner(
        log=log,
        client=AsyncOpenAI(api_key=oai_key),
        model=model,
    )
    cli_prompt_output = await runner.run_prompt(
        CliPromptInput(
            query=user_query,
        ),
    )
    console.hide_spinner()
    log.debug(f'Runner result: {cli_prompt_output = }')

    if not cli_prompt_output:
        console.print_retry()
        return False

    if cli_prompt_output.answer:
        console.print_answer(cli_prompt_output.answer)
    if not cli_prompt_output.command:
        return True

    console.print_command(cli_prompt_output.command)
    confirmed = console.await_confirmation()
    if confirmed:
        log.info(f'RUNNING {cli_prompt_output.command}')
        command_result = os.system(cli_prompt_output.command)
        return command_result == 0
    else:
        console.print_farewell()
        return True
