var React = require('react');

module.exports = React.createClass({
    render: function() {
        return (
            <div className="panel panel-projectfilter">
                <div className="panel-heading">
                    Filter:
                </div>
                <div className="panel-body">
                    Project name: <input/>
                </div>
            </div>
        )
    }
})