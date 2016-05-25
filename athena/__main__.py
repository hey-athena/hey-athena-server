""" Hey Athena start script """
import sys

from flask import Flask, request
from os.path import dirname, realpath
sys.path.append(dirname(dirname(realpath(__file__))))

from athena import brain
brain.init()
brain.inst.run()

app = Flask(__name__)


@app.route('/api/')
def smart():
    query = request.args.get('q')
    if not query:
        return "Syntax: https://heyathena.com/api?q=hello"
    return brain.inst.ask(query)

if __name__ == '__main__':
    app.run(debug=True)
