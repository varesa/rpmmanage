from flask import Flask, render_template

import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/projects/')
def view_projects():
    return json.dumps([
        {
            'id': 1,
            'name': 'DNSGui',
            'version': '1.0.1',
        },
        {
            'id': 2,
            'name': 'repo_sync',
            'version': '0.1'
        }
    ])

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
