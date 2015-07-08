var React = require('react');

var ProjectFilter = require('./ReactProjectFilter');
var ModalToggleButton = require('./ReactModalToggleButton');
var HSpacer = require('./ReactHSpacer');

var AppToolbar = React.createClass({
    render: function() {
        return (
            <div className="panel panel-projecttools">
                <div className="panel-heading">
                    Project tools
                </div>
                <div className="panel-body">
                    <ModalToggleButton modalId="projectNew" text="New Project" /> <HSpacer /> <ProjectFilter />
                </div>
            </div>
        )
    }
});

module.exports = AppToolbar;