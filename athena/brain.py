"""

The "Brain" class handles most of Hey Athena's processing.
To listen for input, use ``brain.inst.run()``

"""
import traceback
import sys

from athena import settings, apis, mods

inst = None


def init():
    global inst
    inst = Brain()


class Brain():

    def __init__(self):
        apis.find_apis()
        apis.list_apis()

        mods.find_mods()
        mods.list_mods()

    def execute_tasks(self, mod, text):
        """ Executes a module's task queue """
        msg = ""
        for task in mod.task_queue:
            msg += str(task.action(text))+'\n'
            if task.greedy:
                break
        return msg

    def execute_mods(self, text):
        """ Executes the modules in prioritized order """
        if len(self.matched_mods) <= 0:
            return settings.NO_MODULES

        self.matched_mods.sort(key=lambda mod: mod.priority, reverse=True)

        return self.execute_tasks(self.matched_mods[0], text)

    def match_mods(self, text):
        """ Attempts to match a modules and their tasks """
        self.matched_mods = []
        for mod in mods.mod_lib:
            if not mod.enabled:
                continue
            """ Find matched tasks and add to module's task queue """
            mod.task_queue = []
            for task in mod.tasks:
                if task.match(text):
                    mod.task_queue.append(task)
                    if task.greedy:
                        break

            """ Add modules with matched tasks to list """
            if len(mod.task_queue):
                self.matched_mods.append(mod)

    def ask(self, text):
        """ Match the modules and respond """
        try:
            self.match_mods(text)
            return self.execute_mods(text)
        except:
            print(traceback.format_exc())
            return settings.ERROR

    def run(self):
        while True:
            text = input('> ')
            if text == "q":
                sys.exit()
            print(self.ask(text))
