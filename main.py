import asyncio
import os
from argparse import ArgumentParser
from typing import get_args

from openai import AsyncOpenAI

from zed.constants import DEFAULT_MODEL, OpenAiModel
from zed.model.cli_prompt.runner import CliPromptInput, Runner
from zed.utils.print import pprint


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
    is_debug: bool = parsed.debug
    model: OpenAiModel = parsed.model

    pprint(is_debug, model, query_params)

    # pprint(parsed_query)
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

    # TODO setup actual pretty print
    # system color for default  / debug text
    # answer text in WHITE
    # command text in CYAN
    # confirm in RED

    pprint(cli_prompt_output)

    # TODO setup command runner
    # gets user confirmation
    # runs commands on cli


if __name__ == "__main__":
    asyncio.run(main())
