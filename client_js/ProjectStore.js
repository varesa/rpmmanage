var $ = require('jquery');
var React = require('react');

var ReactProject = require('./components/ReactProject');

var ProjectStore = function() {
    this._projects = [];
};

ProjectStore.prototype.fetch = function() {
    var projectStore = this;
    $.get("/projects", function(data) {
        console.log(data);
        var json = JSON.parse(data);
        for(var i = 0; i < json.length; i++) {
            projectStore._projects.push(<ReactProject name={json[i].name} version={json[i].version} />);
            console.log(json[i]);
        }
        dispatcher.dispatch({'event': 'PROJECTS_UPDATED'});
    });
};

ProjectStore.prototype.getAll = function () {
    return this._projects;
};

module.exports = ProjectStore;