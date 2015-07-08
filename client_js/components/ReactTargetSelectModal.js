var React = require('react');

var Modal = require('./ReactModal');
var TargetRadio = require('./ReactTargetRadio');

var TargetSelectModal = React.createClass({
    updateState: function() {
        var targetRadios = [];
        targetStore.getAll().forEach(function(target) {
            targetRadios.push(<TargetRadio name="target" value={target.name} />);
        });
        this.setState({targetRadios: targetRadios});
    },
    componentWillMount: function() {
        var tsm = this;
        dispatcher.register(function(payload) {
            if(payload.name === "TARGETS_UPDATE_DONE") {
                tsm.updateState();
            }
        });
    },
    getInitialState: function() {
        dispatcher.dispatch({name: "TARGETS_UPDATE_START"});
        return {targetRadios: []};
    },
    post: function() {
        return ""
    },
    render: function () {
        return (
            <Modal modalId="targetSelect" title="Select new target" btnText="select" btnAction={this.post}>
                <form>
                    {this.state.targetRadios}
                    <br />
                    <input type="radio" name="target" value="_new_" />&nbsp;&nbsp;<input type="text" />
                </form>
            </Modal>
        )
    }
});

module.exports = TargetSelectModal;