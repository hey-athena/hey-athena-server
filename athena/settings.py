"""

Global settings are stored here

"""

from os import mkdir, path
from athena import api_library
from athena.modules import active as active_mods

#####################
#    DIRECTORIES    #
#####################
CLIENT_DIR =    path.dirname(path.abspath(__file__))
BASE_DIR =      path.dirname(CLIENT_DIR)
DATA_DIR =      path.join(CLIENT_DIR, 'data')
LOGS_DIR =      path.join(DATA_DIR,   'logs')

DIRS = [LOGS_DIR]

for d in DIRS:
    if not path.exists(d):
        mkdir(d)

API_DIRS = [
    # Add your custom api directory strings here (e.g. - "C:/myapis")
]
API_DIRS.extend(api_library.__path__)
MOD_DIRS = [

]
MOD_DIRS.extend(active_mods.__path__)

#####################
#     RESPONSES     #
#####################
ERROR = "Something went wrong while I tried to find a response."
NO_MODULES = "I'm not sure how to respond to that yet."
