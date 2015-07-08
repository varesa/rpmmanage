var React = require('react');

var ModalToggleButton = React.createClass({
    onClick: function(event) {
        dispatcher.dispatch({name: 'MODAL_TOGGLE', data: this.props.modalId});
    },
    render: function() {
        return (
            <div style={{ "display": "inline"}}>
                <button className="btn" onClick={this.onClick}>{this.props.text}</button>
            </div>
        )
    }
});

module.exports = ModalToggleButton;