from typing import Literal

ENV_VARIABLE_OAI_KEY = "ZED_OAI_KEY"
ENV_VARIABLE_YODA_MODE = "ZED_YODA_MODE"

OpenAiModel = Literal["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]

DEFAULT_MODEL = "gpt-4-turbo"
"""
The default OpenAI model used by Zed.
"""
