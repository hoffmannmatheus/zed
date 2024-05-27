
# Overview 
A helpful command line assistant, based on ChatGPT.

## Getting started
Install Zed by running: 
```bash
pip install zed-assistant
```
Note that Zed requires Python 3.8+.

You'll need your own OpenAI key to be able to use Zed. See "Configure" below to know how.

## Usage
Run `zed` with no arguments to get the help menu:
```
~ zed
     ______ ___________
    |___  /|  ___|  _  \
       / / | |__ | | | |
      / /  |  __|| | | |
    ./ /___| |___| |/ /
    \_____/\____/|___/  v0.0.4

usage: zed [-h] [--version] [--debug] [--model {gpt-4o,gpt-4-turbo,gpt-3.5-turbo}] [--yoda-mode]

zed is a LLM-based CLI assistant.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --debug               Enables print debug logs.
  --model {gpt-4o,gpt-4-turbo,gpt-3.5-turbo}
                        The specific Open AI model to be used. Default is 'gpt-4o'
  --yoda-mode           Enables Master Yoda mode.
```

## Configure
After you run `zed` for the first time, a default configuration file is created. To include your Open AI key, or 
change other settings, edit the `~/.zed/config` file:
```bash
openai_key=<YOUR_OPEN_AI_KEY>
model=gpt-4-turbo
debug=False
yoda_mode=False
```



# Contributing 
## Install dependencies
Setup the project locally:
```bash
git clone https://github.com/hoffmannmatheus/zed/ && cd zed
poetry install
```

## Run tests
```bash
poetry run pytest
```

## Run zed locally
First, setup your local OpenAI API in the `~/.zed/config` file. 
Then, run locally with:
```bash
poetry run zed
```

## Publishing a new version
```bash
poetry publish --build
```
