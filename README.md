
# Overview 
A helpful command line assistant, based on ChatGPT.

# Installation
```bash
pip install zed_cli
```

# Usage
```bash
zed --help
```

## Examples
```bash
zed zip my-folder/
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
First, setup your local OpenAI API key: 
```bash
export ZED_OAI_KEY="your-openai-key"
```
Then, run locally with:
```bash
poetry run zed
```

## Publishing a new version
```bash
poetry publish --build
```
