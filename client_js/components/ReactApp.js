/**
 * Created by esa on 30.6.2015.
 */
var React = require('react');

var AppToolbar = require('./ReactAppToolbar');
var Modal = require('./ReactModal');
var ProjectNewModal = require('./ReactProjectNewModal');
var Project = require('./ReactProject');
var ProjectStore = require('../stores/ReactProjectStore');
var TargetSelectModal = require('./ReactTargetSelectModal');

module.exports = React.createClass({
    updateState: function() {
        this.setState({'projects': projectStore.getAll()});
    },
    getInitialState: function() {
        dispatcher.dispatch({name: "PROJECTS_UPDATE_START"});
        return {'projects': []};    // But return an empty array for now
    },
    componentWillMount: function() {
        reactProjectList = this;
        dispatcher.register(function(payload) {
            if (payload.name === "PROJECTS_UPDATE_DONE") {
                reactProjectList.updateState();
            }
        });
    },
    render: function() {
        return (
            <div className="container">
                <h1>RPM-Manager</h1>

                <AppToolbar />
                <ProjectNewModal />
                <TargetSelectModal />

                { this.state.projects }

            </div>
        );
    }
});