from flask import current_app, render_template
import json

@current_app.route('/')
def hello_world():
    return render_template("index.html")

@current_app.route('/projects/')
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