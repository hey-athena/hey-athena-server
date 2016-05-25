"""
    A simple module for playing music

    Usage Examples:
        - "Play some music"
        - "Turn up!"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask


class PlaySongTask(ActiveTask):

    def __init__(self):
        super().__init__(patterns=[r'.*\b(play.*music)\b.*'])

    def action(self, text):
        return ('play_music', 'Playing music...')


class PauseSongTask(ActiveTask):

    def __init__(self):
        super().__init__(patterns=[r'.*\b((pause|stop).*music)\b.*'])

    def action(self, text):
        return ('pause_music', 'Music paused.')


class Music(Module):

    def __init__(self):
        tasks = [PlaySongTask(), PauseSongTask()]
        super().__init__('music', tasks, priority=2)
