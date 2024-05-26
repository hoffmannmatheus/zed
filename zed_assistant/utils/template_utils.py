import os
from typing import Dict

from jinja2 import Template


def load_template(origin_path: str, template_name: str) -> str:
    folder = os.path.dirname(origin_path)
    path = os.path.join(folder, template_name + ".j2")
    with open(path, "r") as file:
        return file.read()


def render_data(template: str, data: Dict) -> str:
    jinja_template = Template(template)
    return jinja_template.render(data)
