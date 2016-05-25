"""

The "Task" class represents an action to be performed

The "ActiveTask" class uses the "match" method to trigger an action.
Generally regex patterns are supplied to do the input matching.
The "match" method can be overriden with "return match_any(text)" to
trigger an action upon matching any given regex pattern.

Example Response:
{
    "timestamp": "2016-05-22T16:06:16.048Z",
    "result": {
        "query": "turn on the lights",
        "module": "house_control",
        "action": "power_on_lights",
        "parameters": {
            "appliance": "lights",
            "powerAction": "turn on"
        },
        "contexts": [],
        "response": "Turning on the Lights"
        "score": 1
    },
    "status": {
        "code": 200,
        "errorType": "success"
    }
}

"""

import json
import re
import time

from athena import settings


class Task(object):

    def get_json(self,
                 query,
                 module="(unknown)",
                 action="(unknown)",
                 parameters={},
                 response=settings.NO_MODULES):
        """ Formats a JSON response string """
        json_response = {}
        json_response['timestamp'] = time.time()

        result = {}
        result['query'] = query
        result['module'] = module
        result['action'] = action
        result['parameters'] = parameters
        result['response'] = response

        # Not implemented yet
        result['contexts'] = []
        result['score'] = 1

        json_response['result'] = result

        status = {
            "code": 200,
            "errorType": "success"
        }
        json_response['status'] = status

        return json.dumps(json_response)

    def action(self, text):
        """ Execute the task action """
        return ""


class ActiveTask(Task):
    def __init__(self,
                 patterns=None,
                 words=None,
                 priority=0,
                 greedy=True,
                 regex_precompile=True,
                 regex_ignore_case=True):
        if patterns is None:
            patterns = []
        if words is None:
            words = []

        if words:
            p = r'.*\b('
            p += str(words)[1:-1].replace('\'', '').replace(', ', '|')
            p += r')\b.*'
            patterns.append(p)

        if regex_precompile:
            if regex_ignore_case:
                self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
            else:
                self.patterns = [re.compile(p) for p in patterns]
        else:
            self.patterns = patterns

        """ Tasks are matched/sorted with priority in modules """
        self.priority = priority

        """ If task is matched, stop module from matching proceeding tasks """
        self.greedy = greedy

    def match(self, text):
        """ Check if the task input criteria is met """
        return self.match_any(text)

    def match_any(self, text):
        """ Check if any patterns match """
        for p in self.patterns:
            if p.match(text):
                return True
        return False

    def match_and_save_groups(self, text, group_key_dict):
        """
            Check if any patterns match,
            If so, save the match groups to self.(key name)
        """
        for case, p in enumerate(self.patterns):
            m = p.match(text)
            if m is not None:
                self.case = case
                for group_num, attribute_name in group_key_dict.items():
                    setattr(self, attribute_name, m.group(group_num).strip())
                return True
        return False
