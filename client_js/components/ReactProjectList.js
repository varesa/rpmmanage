/**
 * Created by esa on 30.6.2015.
 */
var React = require('react');

var ProjectFilter = require('./ReactProjectFilter');
var Project = require('./ReactProject');
var ProjectStore = require('./../ProjectStore');

module.exports = React.createClass({
    updateState: function() {
        this.setState({'projects': projectStore.getAll()});
    },
    getInitialState: function() {
        projectStore.fetch();       // Start a reftesh
        return {'projects': []};    // But return an empty array for now
    },
    componentDidMount: function() {
        reactProjectList = this;
        dispatcher.register(function() {
            reactProjectList.updateState();
        });
    },
    render: function() {
        return (
            <div className="container">
                <h1>RPM-Manager</h1>

                <ProjectFilter />

                { this.state.projects }

            </div>
        );
    }
});