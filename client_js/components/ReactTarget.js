var React = require('react');

module.exports = React.createClass({
    propTypes: {
        name: React.PropTypes.string,
        srpm: React.PropTypes.string,
        rpm: React.PropTypes.string,
        state: React.PropTypes.string
    },

    getInitialState: function() {
        return {
            'name': 'el6-x86_64',
            'srpm': 'a',
            'rpm': 'b',
            'publish': 'c'
        }
    },

    render: function() {
        return (
            <tr>
                <td>{this.state.name}</td>
                <td>{this.state.srpm}</td>
                <td>{this.state.rpm}</td>
                <td>{this.state.publish}</td>
            </tr>
        )
    }
});