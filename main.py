import asyncio
import os

from openai import AsyncOpenAI

from zed.model.cli_prompt.runner import CliPromptInput, Runner
from zed.utils.print import pprint


async def main():
    runner = Runner(
        client=AsyncOpenAI(
            api_key=os.environ.get("ZED_OAI_KEY"),
        )
    )

    result = await runner.run_prompt(
        CliPromptInput(query="list changes since yesterday"),
    )

    pprint(result)


if __name__ == "__main__":
    asyncio.run(main())
