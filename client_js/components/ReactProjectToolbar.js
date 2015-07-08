var React = require('react');

var ModalToggleButton = require('./ReactModalToggleButton');
var HSpacer = require('./ReactHSpacer');


var ProjectToolbar = React.createClass({
    render: function() {
        return (
            <ModalToggleButton modalId="targetSelect" text="Add new target" />
        );
    }
});

module.exports = ProjectToolbar;