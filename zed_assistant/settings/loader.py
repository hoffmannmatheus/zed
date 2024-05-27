from typing import Dict, Optional

from zed_assistant.model.defs import DEFAULT_MODEL, OpenAiModel
from zed_assistant.settings.defs import (
    CONFIG_SEPARATOR,
    SETTINGS_CONFIG_FILE,
    ZedSettings,
)


def merge_with_local_settings(
    model: Optional[OpenAiModel] = None,
    yoda_mode: Optional[bool] = False,
    is_debug: bool = False,
) -> ZedSettings:
    str_config = _read_local_config()
    local = _config_str_to_dict(str_config=str_config)
    return ZedSettings(
        openai_key=local.get("openai_key"),
        model=model or local.get("model", DEFAULT_MODEL),
        yoda_mode=yoda_mode or local.get("yoda_mode", "").lower() == "true",
        debug=is_debug or local.get("debug", "").lower() == "true",
    )


def _read_local_config() -> str:
    """
    Reads the local settings, saved in ~/.zed/config
    If the file or contents do not exist, the default ZedSettings are written.
    """
    config_file = SETTINGS_CONFIG_FILE
    config_file.parent.mkdir(exist_ok=True)
    if not config_file.exists():
        str_settings = ZedSettings().to_config_file_str()
        config_file.write_text(str_settings)
    else:
        with config_file.open("r") as file:
            str_settings = file.read()
    return str_settings


def _config_str_to_dict(str_config: str) -> Dict[str, str]:
    """
    Parses the given config file string to a dictionary.
    """
    dict_settings = {}
    for line in str_config.splitlines():
        if not line.startswith("#") and CONFIG_SEPARATOR in line:
            sep = line.find(CONFIG_SEPARATOR)
            k, v = line[:sep], line[sep + 1 :]
            dict_settings[k] = v
    return dict_settings
