var React = require('react');

var Modal = require('./ReactModal');

var TargetSelectModal = React.createClass({
    post: function() {
        return ""
    },
    render: function () {
        return (
            <Modal modalId="targetSelect" title="Select new target" btnText="select" btnAction={this.post}>
                New target...
            </Modal>
        )
    }
});

module.exports = TargetSelectModal;