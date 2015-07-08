var $ = require('jquery');
var React = require('react');

var ReactProject = require('./components/ReactProject');

var ProjectStore = function() {
    this._projects = [];

    var ps = this;
    dispatcher.register(function(payload) {
        if(payload.name === "PROJECTS_UPDATE_START") {
            ps.fetch();
        }
    })
};

ProjectStore.prototype.fetch = function() {
    var ps = this;
    $.get("/projects", function(data) {
        console.log(data);
        var json = JSON.parse(data);
        ps._projects = [];
        for(var i = 0; i < json.length; i++) {
            ps._projects.push(<ReactProject name={json[i].name} version={json[i].version} />);
            console.log(json[i]);
        }
        dispatcher.dispatch({name: 'PROJECTS_UPDATE_DONE'});
    });
};

ProjectStore.prototype.getAll = function () {
    return this._projects;
};

module.exports = ProjectStore;