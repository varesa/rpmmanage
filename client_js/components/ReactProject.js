var React = require('react');

var Target = require("./ReactTarget");

module.exports = React.createClass({
    propTypes: {
        'name': React.PropTypes.string,
        'version': React.PropTypes.string
    },
    getInitialState: function() {
        return {'name': "Uninitialized"}
    },
    render: function() {
        return (
            <div className="panel panel-project">
                <div className="panel-heading">
                    <h4>Project {this.props.name}. Current version {this.props.version}</h4>
                </div>
                <div className="panel-body">
                    <div className="panel">
                        <table className="table">
                            <tr>
                                <td>Targets:&nbsp;&nbsp;&nbsp;</td>
                                <td>SRPM&nbsp;&nbsp;&nbsp;</td>
                                <td>RPM&nbsp;&nbsp;&nbsp;</td>
                                <td>Publish&nbsp;&nbsp;&nbsp;</td>
                            </tr>
                            <Target />
                            <Target />
                        </table>
                    </div>
                </div>
            </div>
        )
    }
});