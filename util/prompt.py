from noneprompt import ListPrompt, InputPrompt, Choice
from typing import Any,Dict


def list(text: str, choices: Dict[str,Any], need_name: bool = False) -> Any:
    """
    创建一个列表选择器，并返回用户选择的选项数据。

    Args:
        text: 选择器的提示文本
        choices: 选择项的字典，键为选项名称，值为选项数据

    Returns:
        用户选择的选项数据
    """
    choices_list = [Choice(name, data=value) for name, value in choices.items()]
    choice = ListPrompt(text, choices=choices_list).prompt()
    data = choice.data
    name = choice.name
    if need_name:
        return [name, data]
    else:
        return data


def input(text: str) -> str:
    """
    创建一个输入框，并返回用户输入的文本。

    Args:
        text: 输入框的提示文本

    Returns:
        用户输入的文本
    """
    return InputPrompt(text).prompt()
