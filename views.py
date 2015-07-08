from flask import current_app, render_template, request
import json

from dbModels import Project, Target, Build, Task

def create_views(app, database):
    @app.route('/')
    def hello_world():
        return render_template("index.html")

    @app.route('/projects/', methods=['GET'])
    def view_projects_get():
        session = database.get_session()
        projects = session.query(Project).all()
        session.close()
        obj = []
        for project in projects:
            obj.append({'id': project.id, 'name': project.name, 'version': 'abc'})
        return json.dumps(obj)

    @app.route('/projects/', methods=['POST'])
    def view_projects_post():
        name = request.form['name']
        url = request.form['url']

        session = database.get_session()
        session.add(Project(name=name, git_url=url))
        session.commit()
        session.close()

        return "OK"

    @app.route('/targets/', methods=['GET'])
    def view_targets_get():
        session = database.get_session()
        targets = session.query(Target).all()
        session.close()
        obj = []
        for target in targets:
            obj.append({'id': target.id, 'name': target.name})
        return json.dumps(obj)

    @app.route('/targets/', methods=['POST'])
    def view_targets_post():
        name = request.form['name']

        session = database.get_session()
        session.add(Target(name=name))
        session.commit()
        session.close()

        return "OK"
