"""
    Wraps the Spotify Web Player to play music
    Usage Examples:
        - "Open facebook.com"
        - "Search Neil Degrasse Tyson"
        - "Maximize the browser"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask


VB_PATTERNS = [r'.*\b(?:search(?: for)?|look up|tell me about)\b(.*)',
               r'.*\b(?:go to|open)(.*\.(com|org|net|edu|gov|io|html))\b',
               r'.*\b(?:type)\b(.*)',
               r'.*\b(?:close|shut)(?: the| this)? (tab|page)\b.*',
               r'.*\b(?:close|shut)(?: the| this)? (browser)\b.*',
               r'.*\b(delete|clear the)\b.*',
               r'.*\b(maximize)\b.*',
               r'.*\b(click)\b.*',
               r'.*\b(?:next|switch the) (tab|page)\b.*']


class VoiceBrowseTask(ActiveTask):

    def __init__(self):
        super(VoiceBrowseTask, self).__init__(patterns=VB_PATTERNS)
        self.groups = {1: 'group1'}

    def match(self, text):
        return self.match_and_save_groups(text, self.groups)

    def action(self, text):
        actions = {
            0: 'vb_search',
            1: 'vb_open',
            2: 'vb_type',
            3: 'vb_close_tab',
            4: 'vb_close_browser',
            5: 'vb_clear',
            6: 'vb_maximize',
            7: 'vb_click',
            8: 'vb_switch_tab',
        }
        params = {'group1': self.group1}
        return self.get_json(text,
                             module='voice_browse',
                             action=actions[self.case],
                             parameters=params,
                             response='Executing voice browse action...')


class VoiceBrowse(Module):

    def __init__(self):
        tasks = [VoiceBrowseTask()]
        super(VoiceBrowse, self).__init__('voice_browse', tasks, priority=2)
