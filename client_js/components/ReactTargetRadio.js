var React = require('react');
var HSpacer = require('./ReactHSpacer');

var TargetRadio = React.createClass({
    render: function () {
        return (
            <span>
                <input type="radio" name={this.props.name} value={this.props.value}/>&nbsp;&nbsp;
                <label>{this.props.value}</label>
                <HSpacer />
           </span>
        )
    }
});

module.exports = TargetRadio;