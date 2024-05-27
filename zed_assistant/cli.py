import asyncio
import logging
import sys
from argparse import ArgumentParser
from typing import Tuple, get_args

from zed_assistant import __version__
from zed_assistant.model.defs import DEFAULT_MODEL, OpenAiModel
from zed_assistant.settings.defs import ZedSettings
from zed_assistant.settings.loader import merge_with_local_settings
from zed_assistant.zed import Zed

logging.basicConfig(stream=sys.stdout)
log = logging.getLogger(__name__)

zed_ascii = rf"""
     ______ ___________
    |___  /|  ___|  _  \
       / / | |__ | | | |
      / /  |  __|| | | |
    ./ /___| |___| |/ /
    \_____/\____/|___/  v{__version__}
"""


def main() -> None:
    parser = ArgumentParser(
        description="zed is a LLM-based CLI assistant built with python and Chat GPT",
    )
    user_query, settings = parse_arguments(parser)

    log.setLevel(logging.DEBUG if settings.debug else logging.WARNING)
    log.debug(f" {settings=} {user_query=}")

    if not user_query:
        log.debug(" No question or command provided to zed.")
        print(zed_ascii)
        parser.print_help()
        sys.exit(0)
    if not settings.openai_key:
        log.error(
            " Open AI key is not configured. Please set the 'openai_key' "
            "in ~/.zed/config"
        )
        sys.exit(-1)

    zed = Zed(settings=settings, log=log)
    success = asyncio.run(zed.run(user_query=user_query))
    sys.exit(0 if success else -1)


def parse_arguments(parser: ArgumentParser) -> Tuple[str, ZedSettings]:
    parser.add_argument(
        "--version",
        action="version",
        version=f"zed-assistant {__version__}",
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
        help=f"The specific Open AI model to be used. Default is '{DEFAULT_MODEL}'",
    )
    parser.add_argument(
        "--yoda-mode",
        action="store_true",
        default=False,
        help=f"Enables Master Yoda mode.",
    )
    parsed, user_query = parser.parse_known_args()
    formatted_query = " ".join(user_query)
    settings = merge_with_local_settings(
        model=parsed.model,
        is_debug=parsed.debug,
        yoda_mode=parsed.yoda_mode,
    )
    return formatted_query, settings


if __name__ == "__main__":
    main()
