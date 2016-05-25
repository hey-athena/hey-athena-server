"""
    Handles most general questions (including math!)

    Requires:
        - WolframAlpha API key

    Usage Examples:
        - "How tall is Mount Everest?"
        - "What is the derivative of y = 2x?"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask


class AnswerTask(ActiveTask):

    def match(self, text):
        return True

    def action(self, text):
        return self.get_json(text,
                             module='wolfram',
                             action='answer_task',
                             response='Answering with wolfram...')


class Wolfram(Module):

    def __init__(self):
        tasks = [AnswerTask()]
        super().__init__('wolfram', tasks, priority=0)
